# Graph utilities.

from operator import itemgetter
from typing import Dict, Iterable, List, TextIO, Tuple, TypeVar

from networkx.classes.digraph import DiGraph

from pithy.json import load_jsonl, out_jsonl
from pithy.loader import FileOrPath, add_loader, load, text_file_for
from pithy.io import errSL


def load_graph(file_or_path:FileOrPath, ext:str=None) -> DiGraph:
  graph = DiGraph()
  for adj in load_jsonl(text_file_for(file_or_path)):
    src = adj[0]
    graph.add_node(src)
    for dst in adj[1:]:
      graph.add_edge(src, dst)
  return graph

add_loader('.graph', load_graph)


def out_graph(graph:DiGraph) -> None:
  for src, dst_seq in graph.adjacency():
    out_jsonl([src] + list(dst_seq))


def subgraph(graph:DiGraph, nodes, include_outgoing=True):
  sg = DiGraph()
  for src, dst_seq in graph.adjacency():
    sg.add_edges_from((src, dst) for dst in dst_seq if src in nodes and include_outgoing or dst in nodes)
  return sg


K = TypeVar('K')
V = TypeVar('V')
KVP = Tuple[K, V]

def items_by_score(items:Iterable[KVP], reverse=True) -> List[KVP]:
  return sorted(items, key=itemgetter(1), reverse=reverse)

def nodes_by_score(items:Iterable[KVP], reverse=True) -> List[K]:
  return [node for node, _ in items_by_score(items, reverse)]
