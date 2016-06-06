# find all '<…>' entity sequences in the text and output a list.

import muck
import re

from pithy import *

text = muck.source('websters-para-lines.txt')

entities = set()

for i, line in enumerate(text):
  for m in re.finditer(r'</?([^>]*)>', line):
    e = m.group(1)
    entities.add(e)

for e in sorted(entities):
  outL(e)
