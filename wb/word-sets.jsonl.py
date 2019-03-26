# Generate basic data mapping defined words to defining word sets.

import re
from collections import namedtuple

from parsing import clean_word_token_re, entity_replacements, parser, word_re
from pithy.dict import DefaultByKeyDict
from pithy.io import *
from pithy.json import out_jsonl
from pithy.loader import load
from stopwords import stopwords


scans = load('wb/scan.jsons')



# Words and definitions have a many-to-many relationship.
# One word can be defined multiple times;
# Multiple words can be defined in a single record.
# A single 'word' being defined might be multiple tokens.
# For multiple words sharing a definition, the first is treated as the canonical 'base' word.
WordDefns = namedtuple('WordDefns', 'base words defns')

word_bases = {} # Maps each word to its base, which may be itself.

base_worddefns = DefaultByKeyDict(lambda base: WordDefns(base, set(), set()))


space_re = re.compile(r'\s+')

def clean_hw_word(tree):
  'Join together word tokens after omitting the pronunciation tokens.'
  tokens = [el for el in tree.walk_contents() if clean_word_token_re.fullmatch(el)]
  s = ''.join(tokens).strip().lower()
  return space_re.sub(' ', s) # regularize multiple spaces just in case.


def clean_defn_words(tree):
  for el in tree.walk_contents():
    el = el.lower()
    if el not in stopwords and word_re.fullmatch(el):
      yield el


multiword_count = 0

for record in err_progress(scans):
  words = []
  defns = set()
  other = set()

  def digest_tree(tree):
    global multiword_count
    if isinstance(tree, str):
      other.add(tree)
      return
    tag = tree[0]
    if tag == '<hw>':
      word = clean_hw_word(tree)
      if ' ' in word: multiword_count += 1
      # TODO: figure out what to do with multiwords, as they will never match individual words in the set.
      words.append(word)
    elif tag == '<def>':
      defns.update(clean_defn_words(tree))
    else:
      for el in tree.contents:
        digest_tree(el)

  for para in record:
    tree = parser.parse(para, leaf_replacements=entity_replacements)
    digest_tree(tree)

  assert words
  # the first word is the base, unless a base already exists from a previous record.
  base = word_bases.setdefault(words[0], words[0])
  word_defns = base_worddefns[base]
  word_defns.words.update(words)
  word_defns.defns.update(defns)

errL(f'bases: {len(base_worddefns)}; words: {len(word_bases)}; multiwords (keys containing spaces): {multiword_count}')

for worddefn in base_worddefns.values():
  out_jsonl(worddefn)
