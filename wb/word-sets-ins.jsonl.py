# Generate list of nodes sorted by in degree.

from graphs import items_by_score
from pithy.json import out_jsonl
from pithy.loader import load


graph = load('wb/word-sets.graph')

in_degs = graph.in_degree()

for p in items_by_score(in_degs):
  out_jsonl(p)
