# Stubs for networkx.generators.random_graphs (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

def fast_gnp_random_graph(n: Any, p: Any, seed: Optional[Any] = ..., directed: bool = ...): ...
def gnp_random_graph(n: Any, p: Any, seed: Optional[Any] = ..., directed: bool = ...): ...
binomial_graph = gnp_random_graph
erdos_renyi_graph = gnp_random_graph

def dense_gnm_random_graph(n: Any, m: Any, seed: Optional[Any] = ...): ...
def gnm_random_graph(n: Any, m: Any, seed: Optional[Any] = ..., directed: bool = ...): ...
def newman_watts_strogatz_graph(n: Any, k: Any, p: Any, seed: Optional[Any] = ...): ...
def watts_strogatz_graph(n: Any, k: Any, p: Any, seed: Optional[Any] = ...): ...
def connected_watts_strogatz_graph(n: Any, k: Any, p: Any, tries: int = ..., seed: Optional[Any] = ...): ...
def random_regular_graph(d: Any, n: Any, seed: Optional[Any] = ...): ...
def barabasi_albert_graph(n: Any, m: Any, seed: Optional[Any] = ...): ...
def extended_barabasi_albert_graph(n: Any, m: Any, p: Any, q: Any, seed: Optional[Any] = ...): ...
def powerlaw_cluster_graph(n: Any, m: Any, p: Any, seed: Optional[Any] = ...): ...
def random_lobster(n: Any, p1: Any, p2: Any, seed: Optional[Any] = ...): ...
def random_shell_graph(constructor: Any, seed: Optional[Any] = ...): ...
def random_powerlaw_tree(n: Any, gamma: int = ..., seed: Optional[Any] = ..., tries: int = ...): ...
def random_powerlaw_tree_sequence(n: Any, gamma: int = ..., seed: Optional[Any] = ..., tries: int = ...): ...
def random_kernel_graph(n: Any, kernel_integral: Any, kernel_root: Optional[Any] = ..., seed: Optional[Any] = ...): ...
