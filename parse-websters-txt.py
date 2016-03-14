#!/usr/bin/env python3

import sys
import re

from pprint import pprint

name_re = re.compile(r"[- '.;A-Z0-9]+$")
defn_re = re.compile(r'( |[ \w]+:|Syn\.$|\d+\.)')

src_name = "gutenberg-websters.txt"
f_in = open(src_name)

state_names = (
  'none',
  'blank',
  'name',
  'pron', # pronunciation.
  'defn',
)

( s_none,
  s_blank,
  s_name,
  s_pron,
  s_defn) = range(len(state_names))

prev_state = s_blank
name = None
pron = None
defn_lines = []
defns = []

records = []

for (line_num, line_raw) in enumerate(f_in):
  state = s_none
  line = line_raw.rstrip()

  def note(label, msg):
    print('{}: line {}'.format(label, line_num + 1))
    print('  state: {} -> {}'.format(state_names[prev_state], state_names[state]))
    print('  line: {!r}'.format(line))
    if msg:
      print('  {}'.format(msg))

  def warn(msg):
    note("WARNING", msg)

  def error(msg=None):
    note("ERROR", msg)
    sys.exit(1)

  def flush_defn():
    global defn_lines
    lines = []
    prev_char = ''
    for line in defn_lines:
      if prev_char in '.,;':
        lines.append(' ')
      lines.append(line)
      prev_char = line[-1]
    defns.append(''.join(lines))
    defn_lines = []

  def flush_record():
    global name
    global pron
    global defns
    if name is None:
      print("ignoring empty record")
      return
    record = {
      "name": name,
      "pron": pron,
      "defn": list(defns),
    }
    defns = []
    records.append(record)

  if line == '':
    state = s_blank
    if prev_state == s_blank: # hack for flushing the last record.
      print('flushing final record')
      flush_record()
    elif prev_state == s_name:
      warn("expected pronunciation following name")
    elif prev_state == s_defn:
      flush_defn()
    else:
      assert(prev_state == s_pron)

  elif prev_state == s_blank:
    if name_re.match(line):
      state = s_name
      flush_record()
      name = line
      pron = ''
    else:
      state = s_defn
      assert(len(defn_lines) == 0)
      defn_lines = [line]

  elif prev_state == s_name:
    state = s_pron
    pron = line

  elif prev_state == s_pron:
    state = s_pron
    pron += line

  elif prev_state == s_defn:
    state = s_defn
    defn_lines.append(line)

  if state == s_none:
    error('bad transition')

  if False:
    print('{:6}: {:5} -> {:5}: {}'.format(
      line_num + 1, state_names[prev_state], state_names[state], line))

  prev_state = state

if True:
  for record in records:
    print()
    pprint(record)
