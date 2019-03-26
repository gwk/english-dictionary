# Stubs for networkx.utils.mapped_queue (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class MappedQueue:
    h: Any = ...
    d: Any = ...
    def __init__(self, data: Any = ...) -> None: ...
    def __len__(self) -> int: ...
    def push(self, elt: Any): ...
    def pop(self): ...
    def update(self, elt: Any, new: Any) -> None: ...
    def remove(self, elt: Any) -> None: ...