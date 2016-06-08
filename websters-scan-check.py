import re
import muck

from parsing import *
from pithy import *


for record in err_progress(muck.source('websters-scan.jsons')):
  for para in record:
    tree = parse_tree(para)
    if isinstance(tree, Flawed):
      errLSSL('\nflawed paragraph:', para, tree.desc())
