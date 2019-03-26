# SGML parser using TagParser.
# It lexes entities and whitespace while preserving the original data exactly.

import re
from itertools import chain, islice

from pithy.ansi import RST_TXT, TXT_M, TXT_R
from pithy.buffer import Buffer
from pithy.loader import load
from pithy.tag_parse import TagParser, TagRule, TagTree


entity_replacements = load('wb/entities.json')

space_pattern = r'\s+'
word_pattern = r"[-'\w]+"
pronunciation_pattern = r'["*`|/]+'
entity_pattern = r'&[^;\s]*;' # note: this is equivalent to that in wb/entities.txt.py.

# this regex matches tokens for 'clean' words, omitting the pronunciation punctuation.
clean_word_token_re = re.compile('|'.join((space_pattern, word_pattern)))

word_re = re.compile(word_pattern)

parser = TagParser(
  leaf_patterns=[space_pattern, word_pattern, pronunciation_pattern, entity_pattern],
  tag_rules=[
    TagRule(r'\(', r'\)'),
    TagRule(r'\[', r'\]'),
    TagRule(r'\{', r'\}'),
    TagRule(r'<[^/][^>]*>', r'</[^>]*>', lambda o, c: c[2:] == o[1:]),
  ])
