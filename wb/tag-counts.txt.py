# Count all '<…>' tags in the text and sort by count, then name.

import re

from pithy.io import outL
from pithy.loader import load
from pithy.iterable import group_sorted_by_cmp
from typing import Counter


text = load('wb/para-lines.txt')

tags = Counter[str]()

for i, line in enumerate(text):
  for m in re.finditer(r'</?([^>]*)>', line):
    tag = m.group(1)
    tags[tag] += 1

max_tag_width = max(len(t) for t in tags)

for group in group_sorted_by_cmp(tags.most_common(), lambda a, b: a[1] == b[1]):
  for tag, count in sorted(group): # sort same-count tags by name.
    outL(f'{tag:{width}}: {count:8}')
