# Analyze the largest strongly connected component.

from collections import defaultdict

from networkx.classes.digraph import DiGraph
from networkx import hits as calc_hits

from graphs import *  # Registers .graph loader.
from pithy.io import *
from pithy.loader import load
from typing import DefaultDict, Set


max_scc = load('wb/word-sets-max-scc.graph')

outL(f'max_scc nodes: {max_scc.number_of_nodes()}; edges: {max_scc.number_of_edges()}')

def node_degree_ranks(degrees:Iterable[KVP]) -> Dict[str,int]:
  degs_to_nodes:DefaultDict[str,Set[str]] = defaultdict(set)
  for node, deg in items_by_score(degrees):
    degs_to_nodes[deg].add(node)
  node_ranks:Dict[str,int] = {}
  for rank, (deg, nodes) in enumerate(sorted(degs_to_nodes.items(), reverse=True)):
    node_ranks.update((node, rank) for node in nodes)
  return node_ranks


out_degs = max_scc.out_degree()
in_degs = max_scc.in_degree()

out_deg_ranks = node_degree_ranks(out_degs)
in_deg_ranks = node_degree_ranks(in_degs)


def out_nodes(g, label, nodes) -> None:
  outL(label, ':\n')
  for node in nodes:
    outL(f'{node!r}: out: {out_degs[node]} (#{out_deg_ranks.get(node)}); in: {in_degs[node]} (#{in_deg_ranks.get(node)})')
    outSL(*sorted(g[node]))
    outL()
  outL()


out_nodes(max_scc, 'OUTS', nodes_by_score(out_degs)[:8])
out_nodes(max_scc, 'INS', nodes_by_score(in_degs)[:8])

hubs, auths = calc_hits(max_scc)

out_nodes(max_scc, 'HUBS', nodes_by_score(hubs.items())[:8])
out_nodes(max_scc, 'AUTHS', nodes_by_score(auths.items())[:8])
