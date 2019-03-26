# Parse the paragraph lines into records.
# This step groups multiple '<p>' tag lines of text by looking for the '<hw>' tag.

import re

from pithy.io import *
from pithy.json import out_json
from pithy.loader import load


lines = load('wb/para-lines.txt')

buffer = []

for line_raw in err_progress(lines, 'lines'):
  line = line_raw.rstrip()
  if re.match(r'(\{\s*)?<hw>', line): # head line.
    if buffer:
      out_json(buffer)
      del buffer[:]
    if line.find('</hw>') == -1: exit('head is missing /hw tag: {!r}', line)
  else: # tail line.
    if line.find('<hw>') != -1:
      errL(f'\nnon-head line contains hw tag:\n{line}')
  buffer.append(line)

assert buffer
out_json(buffer) # flush final record.
