# parse the paragraph lines into records.
# this step converts multiple lines of text into discrete Record objects.

import re
import muck
import json

from pithy import *
from Record import Record


text = muck.source('websters-para-lines.txt')


# parser state.
name = None
tech = None
defns = []

def flush_record():
  global name
  global tech
  global record_count
  assert name
  out_json(Record(name, tech, tuple(defns)))
  name = None # cleared here just for clarity of the state machine.
  tech = None # " ".
  del defns[:]

def add_defns(line):
  defns.append(line)


for line_num, line_raw in err_progress(enumerate(text, 1), 'lines'):
  line = line_raw.rstrip()

  if line.startswith('<hw>'):
    if line_num != 1:
      flush_record()

    # find name.
    m = re.match(r'<hw>(.+)</hw>', line)
    assert m
    name = m.group(1)
    rest = line[m.end():]
    assert not re.search(r'</?hw>', rest)

    # find end of tech.
    m = re.search(r'<def>', rest)
    if not m: # tech line was not smushed with definitions.
      tech = rest
    else:
      i = m.start()
      tech = rest[:i]
      add_defns(rest[i:])

  else:
    add_defns(line)

flush_record() # flush final record.
