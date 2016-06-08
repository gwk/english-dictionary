# parse the paragraph lines into records.
# this step groups multiple '<p>' tag lines of text by looking for the '<hw>' tag.

import re
import muck

from pithy import *


lines = muck.source('websters-para-lines.txt')

buffer = []

for line_raw in err_progress(lines, 'lines'):
  line = line_raw.rstrip()
  if line.find('<hw>') != -1: # head line.
    if buffer:
      out_json(buffer)
      del buffer[:]
    checkF(line.find('</hw>') != -1, 'head is missing /hw tag: {!r}', line)
  else: # tail line.
    checkF(line.find('</hw>') == -1, 'tail contains /hw tag: {!r}', line)
  buffer.append(line)

assert buffer
out_json(buffer) # flush final record.
