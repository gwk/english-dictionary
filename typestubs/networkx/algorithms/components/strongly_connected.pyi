# Stubs for networkx.algorithms.components.strongly_connected (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

def strongly_connected_components(G: Any) -> None: ...
def kosaraju_strongly_connected_components(G: Any, source: Optional[Any] = ...) -> None: ...
def strongly_connected_components_recursive(G: Any) -> None: ...
def strongly_connected_component_subgraphs(G: Any, copy: bool = ...) -> None: ...
def number_strongly_connected_components(G: Any): ...
def is_strongly_connected(G: Any): ...
def condensation(G: Any, scc: Optional[Any] = ...): ...
