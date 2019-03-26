# Check that all parse trees have no flaws (they should all be fixed in the patches).
# Additionally, make sure that the trees are really lossless representations of source strings.

import re

from parsing import TagTree, parser
from pithy.io import err_progress
from pithy.loader import load


tag_start_re = re.compile(r'[[({]|<([^/>]*)>')
tag_end_re = re.compile(r'[])}]|</([^>]*)>')


for record in err_progress(load('wb/scan.jsons')):
  for para in record:
    tree = parser.parse(para)
    assert isinstance(tree, TagTree)

    def checkF(cond:bool, msg:str) -> None:
      if not cond:
        exit(f'{msg}\n{para}\n\n{tree.structured_desc()}') # type: ignore

    checkF(not tree.is_flawed, 'flawed paragraph:')

    # the remaining checks are meant to validate the implementation of tag_tree.

    s = str(tree)
    checkF(s == para, f'bad tree str:\n{s}')

    for leaf in tree.walk_contents():
      checkF(not tag_start_re.search(leaf), f'leaf token looks like tag start: {leaf}')
      checkF(not tag_end_re.search(leaf), f'leaf token looks like tag end: {leaf}')
