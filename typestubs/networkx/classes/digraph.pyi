# Stubs for networkx.classes.digraph (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from networkx.classes.graph import Graph
from typing import Any, Optional

class DiGraph(Graph):
    node_dict_factory: Any = ...
    adjlist_outer_dict_factory: Any = ...
    adjlist_inner_dict_factory: Any = ...
    edge_attr_dict_factory: Any = ...
    graph: Any = ...
    def __init__(self, incoming_graph_data: Optional[Any] = ..., **attr: Any) -> None: ...
    @property
    def adj(self): ...
    @property
    def succ(self): ...
    @property
    def pred(self): ...
    def add_node(self, node_for_adding: Any, **attr: Any) -> None: ...
    def add_nodes_from(self, nodes_for_adding: Any, **attr: Any) -> None: ...
    def remove_node(self, n: Any) -> None: ...
    def remove_nodes_from(self, nodes: Any) -> None: ...
    def add_edge(self, u_of_edge: Any, v_of_edge: Any, **attr: Any) -> None: ...
    def add_edges_from(self, ebunch_to_add: Any, **attr: Any) -> None: ...
    def remove_edge(self, u: Any, v: Any) -> None: ...
    def remove_edges_from(self, ebunch: Any) -> None: ...
    def has_successor(self, u: Any, v: Any): ...
    def has_predecessor(self, u: Any, v: Any): ...
    def successors(self, n: Any): ...
    neighbors: Any = ...
    def predecessors(self, n: Any): ...
    @property
    def edges(self): ...
    out_edges: Any = ...
    @property
    def in_edges(self): ...
    @property
    def degree(self): ...
    @property
    def in_degree(self): ...
    @property
    def out_degree(self): ...
    def clear(self) -> None: ...
    def is_multigraph(self): ...
    def is_directed(self): ...
    def to_undirected(self, reciprocal: bool = ..., as_view: bool = ...): ... # type: ignore
    def reverse(self, copy: bool = ...): ...
