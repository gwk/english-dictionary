# Graph utilities..

import muck
from operator import itemgetter
from pithy.json_utils import load_jsonl, out_jsonl
from networkx import DiGraph


def load_graph(file):
  graph = DiGraph()
  for adj in load_jsonl(file):
    src = adj[0]
    graph.add_node(src)
    for dst in adj[1:]:
      graph.add_edge(src, dst)
  return graph

muck.add_loader('.graph', load_graph)


def out_graph(graph):
  for src, dst_seq in graph.adjacency_iter():
    out_jsonl([src] + list(dst_seq))


def subgraph(graph, nodes, include_outgoing=True):
  sg = DiGraph()
  for src, dst_seq in graph.adjacency_iter():
    sg.add_edges_from((src, dst) for dst in dst_seq if src in nodes and include_outgoing or dst in nodes)
  return sg


def items_by_score(d, reverse=True):
  return sorted(d.items(), key=itemgetter(1), reverse=reverse)

def nodes_by_score(d, reverse=True):
  return [node for node, score in items_by_score(d, reverse)]

