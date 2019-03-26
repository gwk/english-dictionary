from typing import Tuple, NamedTuple

class Record(NamedTuple):
  name: str
  tech: str
  defns: Tuple[str,...]
