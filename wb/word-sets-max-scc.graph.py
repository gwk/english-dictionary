# Find the largest strongly connected component.

import re

from networkx import strongly_connected_components as calc_sccs

from graphs import out_graph, subgraph
from pithy.io import *
from pithy.json import out_jsonl
from pithy.loader import load


graph = load('wb/word-sets.graph')
errL(f'word-sets: nodes: {graph.number_of_nodes()}; edges: {graph.number_of_edges()}')

sccs = list(calc_sccs(graph))

errL(f'sccs: {len(sccs)}')

max_scc_nodes = max(sccs, key=len)
max_scc = subgraph(graph, max_scc_nodes, include_outgoing=False)
errL(f'max scc: nodes: {max_scc.number_of_nodes()}; edges: {max_scc.number_of_edges()}')

out_graph(max_scc)
