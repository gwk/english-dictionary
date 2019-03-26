# Word sets graph with obvious per-record cycles removed.

from pithy.io import *
from pithy.json import out_jsonl
from pithy.loader import load


word_sets = load('wb/word-sets.jsonl')

for record in word_sets:
  base, words, all_defns = record
  defns = set(all_defns) - {base} - set(words)
  out_jsonl([base] + sorted(defns))
  # for now, simply link additional words to base.
  for word in words:
    if word != base:
      out_jsonl((word, base))
