from typing import Tuple, NamedTuple

Record = NamedTuple('Record', (
  ('name', str),
  ('tech', str),
  ('defns', Tuple[str]),
))
