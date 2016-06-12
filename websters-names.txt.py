import muck
import re

from parsing import *
from pithy import *


names = set()

for record in err_progress(muck.source('websters-scan.jsons')):
  for para in record:
    tree = parse_tree(para, leaf_replacements=entity_replacements)
    for hw in tree.walk(lambda el: isinstance(el, Tree) and el[0] == '<hw>'):
      assert hw[-1] == '</hw>'
      punctuated_name = str(hw[1:-1])
      name = re.sub(r'["*`|/]', '', punctuated_name)
      if re.search(r"[^-'.,() \w]", name):
        errFL('\nweird name: {}\n{}', name, para)
      names.add(name)

for name in sorted(names):
  outL(name)
