
import muck

from pithy import *
from pithy.nestparser import NestParser

parser = NestParser()

records = muck.source('websters-scanned.json')

for name, entries in records:
  assert(entries)
  for entry_text, defn_strings in entries:
    cost, entry_tree = parser.parse(entry_text)
    
    def warnF(fmt, *items):
      errL(name)
      errL('  ', entry_text)
      errL('  ', entry_tree)
      errFL('  ' + fmt, *items)

    expect_etym = False
    etym = None
    for i, el in enumerate(entry_tree):
      if is_str(el):
        if el in ('[', '('): # dangling tail.
          tail = entry_tree[i + 1:]
          if expect_etym:
            etym = tail
          break
        words = el.split()
        if not words: continue
        if words[-1] == 'Etym:':
          expect_etym = True
        elif 'Etym:' in words:
          errFL('etym label is out of place: {!r}', el)
      else: # el is delimited tuple.
        if expect_etym:
          etym = el[1:-1]
          expect_etym = False
          if el[0] != '[' or el[-1] != ']':
            warnF('weird etym delimiters: {}', etym)

