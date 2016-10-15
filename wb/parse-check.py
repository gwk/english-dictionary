# Check that all parse trees have no flaws (they should all be fixed in the patches).
# Additionally, make sure that the trees are really lossless representations of source strings.

import muck
import re

from parsing import parser

from pithy.io import err_progress, checkF, failF


tag_start_re = re.compile(r'[[({]|<([^/>]*)>')
tag_end_re = re.compile(r'[])}]|</([^>]*)>')


for record in err_progress(muck.source('wb/scan.jsons')):
  for para in record:
    tree = parser.parse(para)

    def checkF(cond, fmt, *items):
      if not cond:
        failF(fmt + '\n{}\n\n{}', *items, para, tree.structured_desc())

    checkF(not tree.is_flawed, 'flawed paragraph:')

    # the remaining checks are meant to validate the implementation of tag_tree.

    s = str(tree)
    checkF(s == para, 'bad tree str:\n{}', s)

    for leaf in tree.walk_contents():
      checkF(not tag_start_re.search(leaf), 'leaf token looks like tag start: {}', leaf)
      checkF(not tag_end_re.search(leaf), 'leaf token looks like tag end: {}', leaf)
