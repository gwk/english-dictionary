# Generate list of nodes sorted by in degree.

import muck

from pithy.json_utils import out_jsonl
from graphs import items_by_score


graph = muck.load('wb/word-sets-graph.graph')

in_degs = graph.in_degree()

for p in items_by_score(in_degs):
  out_jsonl(p)
