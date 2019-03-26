# Find all '&…;' entity sequences in the text and output a list.
# The micra text used SGML/ISO-8879 encodings, plus many nonstandard ones.

# However the webfont.txt document also states:
# | Note that the symbols used here are in some cases abbreviations
# | (for compactness) of the ISO 8879 recommended symbols.

# webfont.txt also states that an escape syntax '<xx/' is used.
# While these appear in the PG 29765.utf8 text,
# this syntax is not present in the 0.50 texts, as shown by the assertion;
# presumably they were converted to entity syntax.

import re

from pithy.io import outL
from pithy.loader import load


text = load('wb/raw-lines.txt')

entities = set()

for i, line in enumerate(text):
  if re.search(r'<[^/>]+/', line): exit(f'weird escape syntax: {line!r}')
  for m in re.finditer(r'&([^;\s]*);', line):
    e = m.group(1)
    entities.add(e)

for e in sorted(entities):
  outL(e)
