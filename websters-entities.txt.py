# find all '&…;' entity sequences in the text and output a list.
# the micra text used SGML/ISO-8879 encodings, plus many nonstandard ones.

# however the webfont.txt document also states:
# | Note that the symbols used here are in some cases abbreviations
# | (for compactness) of the ISO 8879 recommended symbols.

# webfont.txt also states that an escape syntax '<xx/' is used;
# while these appear in the PG 29765.utf8 text,
# this syntax is not present in the 0.50 texts, as shown by the assertion;
# presumably they were converted to entity syntax.

import muck
import re

from pithy import *

text = muck.source('websters-para-lines.txt')

entities = set()

for i, line in enumerate(text):
  checkF(not re.search(r'<[^/>]+/', line), 'weird escape syntax: {!r}', line)
  for m in re.finditer(r'&([^;\s]*);', line):
    e = m.group(1)
    entities.add(e)

for e in sorted(entities):
  outL(e)
