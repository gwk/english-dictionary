# Generate basic data mapping defined words to defining word sets.

import muck

from pithy.io import *
from pithy.json_utils import out_jsonl

word_sets = muck.load('wb/word-sets.jsonl')

for record in word_sets:
  base, words, defns = record
  out_jsonl([base] + defns)
  # for now, simply link additional words to base.
  for word in words:
    if word != base:
      out_jsonl((word, base))
