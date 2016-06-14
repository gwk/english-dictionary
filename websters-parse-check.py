# check that all parse trees have no flaws (they should all be fixed in the patches).
# additionally, make sure that the trees are really lossless representations of source strings.

import muck

from parsing import *
from pithy import *


for record in err_progress(muck.source('websters-scan.jsons')):
  for para in record:
    tree = parse_tree(para)
    checkF(not isinstance(tree, TreeFlawed),
      'flawed paragraph:\n{!r}\n{}', para, tree.str_indented())
    s = str(tree)
    checkF(s == para, 'bad tree str:\n  orig: {!r}\n  tree: {!r}', para, s)
