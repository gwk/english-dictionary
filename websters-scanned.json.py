#!/usr/bin/env python3

# parse the raw gutenberg text into a json dictionary.
# this step structures the lines of text into discrete elements,
# joining lines where appropriate.
# it does not do much in the way of content analysis;
# the goal is get some structure to the data while preserving the more challenging quirks.

import sys
import re
import muck
import json

from pithy import *


text = muck.source('websters-p2-etym.txt')


# parsing is primarily based on recognizing dictionary entries as capitalized words.
name_re = re.compile(r"[A-Z][- '.;A-Z0-9]*")

# known exceptional cases.
known_excluded_names = {'M.', 'P.', 'X.'}
known_empty_gram = known_excluded_names.union(
  {'B', 'C', 'D', 'E', 'G', 'H', 'I', 'J', 'K', 'L', 'N', 'O', 'Q', 'S', 'U', 'V', 'W', 'Y'})

punctuation_escape_re = re.compile(r' \(([][()/.,; ])')
dangling_paren_re = re.compile(r'(\([^][();,-]+)(\]|$)')

def fix_tech(tech):
  'apply various fixes to the technical line.'
  tech = punctuation_escape_re.sub(lambda m: m.group(1), tech)
  tech = tech.rstrip(' (') # lots of trailing open-parens.
  tech = dangling_paren_re.sub(lambda m: m.group(1) + ')]', tech)
  return tech


# parser is a simple state-machine.
state_names = (
  'none',
  'init',
  'blank',
  'name',
  'gram', # grammar and pronunciation.
  'defn',
)

# use integer states for efficiency.
( s_none,
  s_init,
  s_blank,
  s_name,
  s_gram,
  s_defn) = range(len(state_names))

# mutable, global parser state.
prev_state = s_init
name = None
gram = None
defn_lines = []
defns = []

# records is a list of triples: (name, technical, [definitions]).
records = []

# parsing main loop.
for (line_num, line_raw) in enumerate(text):
  state = s_none
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
    sys.exit(1)

  def flush_defn():
    global defn_lines
    defns.append(' '.join(defn_lines)) # have to be careful not to alias defn_lines anywhere else.
    defn_lines = []

  def flush_record():
    global name
    global gram
    global defns
    if name is None:
      error("empty record")
    if name in known_excluded_names:
      return
    tech = fix_tech(gram) # TODO: rename gram everywhere.
    records.append([name, tech, defns])
    name = None # cleared here just for clarity of the state machine.
    gram = None # " ".
    defns = []

  # end condition.
  if line == "End of Project Gutenberg's Webster's Unabridged Dictionary, by Various":
    break

  # initial transition.
  if prev_state == s_init:
    if line == 'A': # first entry.
      state = s_name
    else:
      continue

  # main state transitions.

  if line == '':
    state = s_blank
    if prev_state == s_blank:
      pass
    elif prev_state == s_name: # missing grammar; happens for some of the letters.
      if name not in known_empty_gram:
        warn('no grammar')
      gram = name
    elif prev_state == s_defn:
      flush_defn()
    else:
      assert(prev_state == s_gram)

  elif prev_state == s_blank:
    if name_re.fullmatch(line) and line.find('  ') == -1:
      # note: the find clause excludes lines from the extended definition for 'MORSE CODE'.
      state = s_name
      flush_record()
    else:
      state = s_defn
      assert(not defn_lines)

  elif prev_state == s_name:
    if re.match(r'\d', line):
      note('missing blank and grammar between name and definition')
      state = s_defn
    else:
      state = s_gram
      gram = line

  elif prev_state == s_gram:
    if re.match(r'\s*\([a-z]\)', line):
      #note('missing blank between grammar and definition')
      state = s_defn
    else:
      state = s_gram
      gram += ' ' + line

  elif prev_state == s_defn:
    if re.match(r'\s*(\([a-z]\)|--)', line):
      flush_defn()
    state = s_defn

  if state == s_none:
    error('bad transition')

  if False:
    errFL('{:6}: {:5} -> {:5}: {}',
      line_num + 1, state_names[prev_state], state_names[state], line)

  # state actions independent of transitions.
  if state == s_name:
    name = line
    gram = ''

  elif state == s_defn:
    defn_lines.append(line)

  prev_state = state

# flush final record.
flush_record()

errFL('writing {} records', len(records))
json.dump(records, sys.stdout, indent=2)
