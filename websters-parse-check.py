# check that all parse trees have no flaws (they should all be fixed in the patches).
# additionally, make sure that the trees are really lossless representations of source strings.

import muck

from parsing import *
from pithy import *

tag_start_re = re.compile(r'[[({]|<([^/>]*)>')
tag_end_re = re.compile(r'[])}]|</([^>]*)>')


for record in err_progress(muck.source('websters-scan.jsons')):
  for para in record:
    tree = parse_tree(para)

    def checkF(cond, fmt, *items):
      if not cond:
        failF(fmt + '\n{}\n\n{}', *items, para, tree.structured_desc())

    checkF(not tree.is_flawed, 'flawed paragraph:')

    # the remaining checks are meant to validate the implementation of Tree.

    s = str(tree)
    checkF(s == para, 'bad tree str:\n{}', s)

    for leaf in tree.walk_contents():
      checkF(not tag_start_re.search(leaf), 'leaf token looks like tag start: {}', leaf)
      checkF(not tag_end_re.search(leaf), 'leaf token looks like tag end: {}', leaf)
