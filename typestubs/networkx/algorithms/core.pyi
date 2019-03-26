# Stubs for networkx.algorithms.core (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

def core_number(G: Any): ...
find_cores = core_number

def k_core(G: Any, k: Optional[Any] = ..., core_number: Optional[Any] = ...): ...
def k_shell(G: Any, k: Optional[Any] = ..., core_number: Optional[Any] = ...): ...
def k_crust(G: Any, k: Optional[Any] = ..., core_number: Optional[Any] = ...): ...
def k_corona(G: Any, k: Any, core_number: Optional[Any] = ...): ...
