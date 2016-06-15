# basic analysis of words and their definitions.

import muck
import re

from parsing import *
from pithy import *


WordDefns = namedtuple('WordDefns', 'base words defns')

# words and definitions have a many-to-many relationship.
# for multiple words sharing a definition, the first is treated as the canonical 'base' word.
# this dict maps each word to its base, which may be itself.
word_bases = {}

bases = DefaultByKeyDict(lambda base: WordDefns(base, set(), set()))


def clean_hw_word(tree):
  tokens = [el for el in tree.walk_contents() if clean_word_token_re.fullmatch(el)]
  return ''.join(tokens).strip()

def clean_defn_words(tree):
  return [el for el in tree.walk_contents() if re.fullmatch(word_pattern, el)]


for record in err_progress(muck.source('websters-scan.jsons')):
  words = []
  defns = set()
  other = set()

  def digest_tree(tree):
    if is_str(tree):
      other.add(tree)
      return
    tag = tree[0]
    if tag == '<hw>':
      words.append(clean_hw_word(tree))
    elif tag == '<def>':
      defns.update(clean_defn_words(tree))
    else:
      for el in tree.contents:
        digest_tree(el)

  for para in record:
    tree = parse_tree(para, leaf_replacements=entity_replacements)
    digest_tree(tree)

  assert words
  # the first word is the base, unless a base already exists from a previous record.
  base = word_bases.setdefault(words[0], words[0])
  word_defns = bases[base]
  word_defns.words.update(words)
  word_defns.defns.update(defns)

out_json(bases)
