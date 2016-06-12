# parse the paragraph lines into records.
# this step groups multiple '<p>' tag lines of text by looking for the '<hw>' tag.

import re
import muck

from pithy import *


lines = muck.source('websters-para-lines.txt')

buffer = []

for line_raw in err_progress(lines, 'lines'):
  line = line_raw.rstrip()
  if re.match(r'(\{\s*)?<hw>', line): # head line.
    if buffer:
      out_json(buffer)
      del buffer[:]
    checkF(line.find('</hw>') != -1, 'head is missing /hw tag: {!r}', line)
  else: # tail line.
    if line.find('<hw>') != -1:
      errFL('\nnon-head line contains hw tag:\n{}', line)
  buffer.append(line)

assert buffer
out_json(buffer) # flush final record.
