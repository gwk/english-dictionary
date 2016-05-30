#!/usr/bin/env python3

# parse the raw gutenberg text into a json dictionary.
# this step structures the lines of text into discrete elements,
# joining lines where appropriate.
# it does not do much in the way of content analysis;
# the goal is get some structure to the data while preserving the more challenging quirks.

import re
import muck
import json

from pithy import *


text = muck.source('websters-p3-misc.txt')


# parsing is primarily based on recognizing dictionary entries as capitalized words.
name_re = re.compile(r"[A-Z][- '.;A-Z0-9]*")

# known exceptional cases.
known_excluded_names = {'M.', 'P.', 'X.'}
known_empty_tech = known_excluded_names.union(
  {'B', 'C', 'D', 'E', 'G', 'H', 'I', 'J', 'K', 'L', 'N', 'O', 'Q', 'S', 'U', 'V', 'W', 'Y'})

# parser is a simple state-machine.
State = Enum('State', [
  'none',
  'init',
  'blank',
  'name',
  'tech', # tecnical line: pronunciation, grammar, etymology, topic.
  'defn',
])

# mutable, global parser state.
prev_state = State.init
name = None
tech = None
defn_lines = []
defns = []

# records is a list of triples: (name, technical, [definitions]).
records = []

# parsing main loop.
for (line_num, line_raw) in enumerate(text):
  state = State.none
  line = line_raw.rstrip()

  def note(msg, label='NOTE'):
    errFL('{}: line {}', label, line_num + 1)
    errFL('  state: {} -> {}; name: {!r}', state_names[prev_state], state_names[state], name)
    errFL('  line: {!r}', line)
    if msg:
      errFL('  {}', msg)

  def warn(msg):
    note(msg, label="WARNING")

  def error(msg=None):
    note(msg, label="ERROR")
    exit(1)

  def flush_defn():
    global defn_lines # have to be careful not to alias defn_lines anywhere else.
    defns.append(' '.join(defn_lines))
    defn_lines = []

  def flush_record():
    global name
    global tech
    global defns
    if name is None: error("empty record")
    if name in known_excluded_names: return
    records.append([name, tech, defns])
    name = None # cleared here just for clarity of the state machine.
    tech = None # " ".
    defns = []

  # end condition.
  if line == "End of Project Gutenberg's Webster's Unabridged Dictionary, by Various":
    break

  # initial transition.
  if prev_state == State.init:
    if line == 'A': # first entry.
      state = State.name
    else:
      continue

  # main state transitions.

  if line == '':
    state = State.blank
    if prev_state == State.blank:
      pass
    elif prev_state == State.name: # missing tech; happens for some of the letters.
      if name not in known_empty_tech:
        warn('no tech')
      tech = name
    elif prev_state == State.defn:
      flush_defn()
    else:
      assert(prev_state == State.tech)

  elif prev_state == State.blank:
    if name_re.fullmatch(line) and line.find('  ') == -1:
      # note: the find clause excludes lines from the extended definition for 'MORSE CODE'.
      state = State.name
      flush_record()
    else:
      state = State.defn
      assert(not defn_lines)

  elif prev_state == State.name:
    if re.match(r'\d', line):
      note('missing blank and technical lines between name and definition')
      state = State.defn
    else:
      state = State.tech
      tech = line

  elif prev_state == State.tech:
    if re.match(r'\s*\([a-z]\)', line):
      #note('missing blank between technical and definition')
      state = State.defn
    else:
      state = State.tech
      tech += ' ' + line

  elif prev_state == State.defn:
    if re.match(r'\s*(\([a-z]\)|--)', line):
      flush_defn()
    state = State.defn

  if state == State.none:
    error('bad transition')

  if False:
    errFL('{:6}: {:5} -> {:5}: {}',
      line_num + 1, state_names[prev_state], state_names[state], line)

  # state actions independent of transitions.
  if state == State.name:
    name = line
    tech = ''

  elif state == State.defn:
    defn_lines.append(line)

  prev_state = state

# flush final record.
flush_record()

errFL('writing {} records', len(records))
out_json(records)
