# Generate list of nodes sorted by in degree.

from graphs import items_by_score
from pithy.json import out_jsonl
from pithy.loader import load


graph = load('wb/word-sets-graph.graph')

out_degs = graph.out_degree()

for p in items_by_score(out_degs):
  out_jsonl(p)
