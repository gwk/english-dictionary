#!/usr/bin/env python3

import re
import muck
import json

from pithy import *

from parsing import *


scanned = muck.source('websters-scanned.json')


lex_re = re.compile(r'[][{}().,;="\s]+')
def lex(text):
  'lex as if both lex_leaf and lex_body were applied, without the structural parsing.'
  return [t for t in lex_re.split(text) if t]


name_words = set()
def_words = set()

def parse_entry(name_caps, tech, defns):
  names = lex(name_caps.lower())
  name_words.update(names)
  for defn in defns:
    words = lex(defn.lower())
    def_words.update(words)

for record in scanned:
  parse_entry(*record)

all_words = name_words.union(def_words)
int_words = name_words.intersection(def_words)
undef_words = def_words.difference(name_words)

errFL('name words: {}; def words: {}; all words: {}; intersection: {}',
  len(name_words), len(def_words), len(all_words), len(int_words))

#json.dump(refined, sys.stdout, indent=2 )
