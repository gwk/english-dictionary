# find all '<…>' tags in the text and output a list.

import muck
import re

from pithy import *


text = muck.source('websters-para-lines.txt')

tags = Counter()

for i, line in enumerate(text):
  for m in re.finditer(r'</?([^>]*)>', line):
    tag = m.group(1)
    tags[tag] += 1

max_tag_width = max(len(t) for t in tags)

for group in grouped_sorted_seq(tags.most_common(), lambda a, b: a[1] == b[1]):
  for tag, count in sorted(group): # sort same-count tags by name.
    outFL('{:{width}}: {:8}', tag, count, width=max_tag_width)
