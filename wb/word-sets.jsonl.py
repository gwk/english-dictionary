# Generate basic data mapping defined words to defining word sets.

import muck
import re

from collections import namedtuple
from pithy.dict_utils import DefaultByKeyDict
from pithy.io import *
from pithy.json_utils import out_jsonl
from pithy.type_util import is_str
from parsing import clean_word_token_re, word_re, entity_replacements, parser


scans = muck.load('wb/scan.jsons')
stopwords = set(muck.load('stopwords.json'))


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
    if is_str(tree):
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

errFL('bases: {}; words: {}; multiwords (keys containing spaces): {}',
  len(base_worddefns), len(word_bases), multiword_count)

for worddefn in base_worddefns.values():
  out_jsonl(worddefn)
