# Analyze the largest strongly connected component.

import muck
import re

from collections import defaultdict
from operator import itemgetter
from pithy.io import *
from pithy.json_utils import out_jsonl
from networkx import DiGraph, hits as calc_hits

from graphs import load_graph


max_scc = muck.load('wb/word-sets-max-scc.graph')

outFL('max_scc nodes: {}; edges: {}', max_scc.number_of_nodes(), max_scc.number_of_edges())

def items_by_score(d, reverse=True):
  return sorted(d.items(), key=itemgetter(1), reverse=reverse)

def nodes_by_score(d, reverse=True):
  return [node for node, score in items_by_score(d, reverse)]


def node_degree_ranks(degrees):
  degs_to_nodes = defaultdict(set)
  for node, deg in items_by_score(degrees):
    degs_to_nodes[deg].add(node)
  node_ranks = {}
  for rank, (deg, nodes) in enumerate(sorted(degs_to_nodes.items(), reverse=True)):
    node_ranks.update((node, rank) for node in nodes)
  return node_ranks


out_degs = max_scc.out_degree()
in_degs = max_scc.in_degree()

out_deg_ranks = node_degree_ranks(out_degs)
in_deg_ranks = node_degree_ranks(in_degs)


def out_nodes(g, label, nodes):
  outL(label, ':\n')
  for node in nodes:
    outFL('{!r}: out: {} (#{}); in: {} (#{})', node, out_degs[node], out_deg_ranks.get(node), in_degs[node], in_deg_ranks.get(node))
    outSL(*sorted(g[node]))
    outL()
  outL()


out_nodes(max_scc, 'OUTS', nodes_by_score(out_degs)[:8])
out_nodes(max_scc, 'INS', nodes_by_score(in_degs)[:8])

hubs, auths = calc_hits(max_scc)

out_nodes(max_scc, 'HUBS', nodes_by_score(hubs)[:8])
out_nodes(max_scc, 'AUTHS', nodes_by_score(auths)[:8])
