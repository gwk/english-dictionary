# Find the largest strongly connected component.

import muck
import re

from pithy.io import *
from pithy.json_utils import out_jsonl
from networkx import strongly_connected_components as calc_sccs

from graphs import out_graph, subgraph


graph = muck.load('wb/word-sets-graph.graph')
errFL('word-sets-graph: nodes: {}; edges: {}', graph.number_of_nodes(), graph.number_of_edges())

sccs = list(calc_sccs(graph))

errFL('sccs: {}', len(sccs))

max_scc_nodes = max(sccs, key=len)
max_scc = subgraph(graph, max_scc_nodes, include_outgoing=False)
errFL('max scc: nodes: {}; edges: {}', max_scc.number_of_nodes(), max_scc.number_of_edges())

out_graph(max_scc)
