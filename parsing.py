# SGML parser.
# the custom parser reports mismatched tags.
# it also lexes entities and whitespace while preserving the original data exactly.

import pithy.meta as meta
import muck
import re

from pithy import *
from pithy.ansi import *


__all__ = [
  'entity_replacements', 'parse_tree',
  'Tree', 'TreeFlawed', 'TreeUnexpected', 'TreeUnterminated',
]


entity_replacements = muck.source('websters-entities.json')


# note: this entities pattern is equivalent to that in websters-entities.
leaf_choices = [r'\s+', r'&[^;\s]*;']

# start token pattern, end token pattern, end_token_for_start_token function.
branch_rules = (
  (r'\(',       r'\)',        lambda s: ')'),
  (r'\[',       r'\]',        lambda s: ']'),
  (r'\{',       r'\}',        lambda s: '}'),
  (r'<[^/>]*>', r'</[^>]*>',  lambda s: '</{}>'.format(s[1:-1]))
)

# parser works be wrapping each start and end pattern in a group.
# the group itself is not used,
# but the matching group index tells the parser which start or end pattern matched.

num_choices = len(branch_rules)

start_choices = ['({})'.format(r[0]) for r in branch_rules]
end_choices   = ['({})'.format(r[1]) for r in branch_rules]
end_for_start_fns = [r[2] for r in branch_rules]

lexer_pattern = '|'.join(chain(start_choices, end_choices, leaf_choices))
lexer = re.compile(lexer_pattern)


class Tree(tuple):
  '''
  Parse tree node base class.
  The string representation of the node is equal to the original text.
  '''

  def __new__(cls, *args):
    return super().__new__(cls, args)

  def __repr__(self):
    return '{}({})'.format(type(self).__name__, ', '.join(repr(el) for el in self))

  def __str__(self):
    return ''.join(str(el) for el in self)

  def __getitem__(self, key):
    if isinstance(key, slice):
      return type(self)(*super().__getitem__(key))
    return super().__getitem__(key)

  name = 'Tree'
  ansi_color = ''
  ansi_reset = ''

  @property
  def has_flawed_els(self):
    return any(isinstance(el, TreeFlawed) for el in subs)


  def walk(self, predicate=is_str):
    for el in self:
      if predicate(el):
        yield el
      elif isinstance(el, Tree):
        yield from el.walk(predicate=predicate)


  def _str_indented(self, res, depth):
    'multiline indented description helper.'
    if self.ansi_color: res.append(self.ansi_color)
    res.append(self.name)
    res.append(':')
    if self.ansi_reset: res.append(self.ansi_reset)

    if all(isinstance(el, str) for el in self):
      for el in self:
        res.append(' ')
        res.append(repr(el))
    else:
      d = depth + 1
      for el in self:
        res.append('\n')
        res.append('  ' * d)
        if isinstance(el, str): res.append(repr(el))
        else: el._str_indented(res, d)

  def str_indented(self, depth=0):
    res = []
    self._str_indented(res, depth)
    return ''.join(res)


class TreeFlawed(Tree):
  name = 'Flawed'
  ansi_color = TXT_Y
  ansi_reset = RST_TXT

class TreeUnexpected(TreeFlawed):
  name = 'Unexpected'
  ansi_color = TXT_R
  ansi_reset = RST_TXT

class TreeUnterminated(TreeFlawed):
  name = 'Unterminated'
  ansi_color = TXT_M
  ansi_reset = RST_TXT


def _parse_tree(leaf_replacements, text, match_stream, pos, depth, subs, end_token, parent_end_token):

  def append_leaf(leaf):
    subs.append(leaf_replacements.get(leaf, leaf))

  def flush_leaf(pos, end_index):
    leaf_text = text[pos:end_index]
    if leaf_text:
      append_leaf(leaf_text)

  for match in match_stream:
    flush_leaf(pos, match.start())
    pos = match.end()
    token = match.group()
    match_index = match.lastindex # only start and end tokens have a group.
    if match_index is None: # leaf token.
      append_leaf(token)
    elif match_index <= num_choices: # found a start token (groups are 1-indexed).
      sub_end_token = end_for_start_fns[match_index - 1](token)
      sub, pos = _parse_tree(leaf_replacements, text, match_stream, pos, depth + 1,
        subs=[token], parent_end_token=end_token, end_token=sub_end_token)
      subs.append(sub)
    elif token == end_token:
      subs.append(token)
      res = (TreeFlawed(*subs) if any(isinstance(el, TreeFlawed) for el in subs) else Tree(*subs))
      return res, pos
    elif token == parent_end_token: # parent end; missing end token.
      match_stream.push(match) # put the parent end token back into the stream.
      return TreeUnterminated(*subs), pos
    else: # unexpected end token.
      subs.append(TreeUnexpected(token))
  # end.
  flush_leaf(pos, len(text))
  return Tree(*subs) if end_token is None else TreeUnterminated(*subs), len(text)


def parse_tree(text, leaf_replacements=None):
  match_stream = IterBuffer(lexer.finditer(text))
  res, pos = _parse_tree(leaf_replacements or {}, text, match_stream, pos=0, depth=0,
    subs=[], parent_end_token=None, end_token=None)
  return res

