# SGML parser.
# the custom parser reports mismatched tags.
# it also lexes entities and whitespace while preserving the original data exactly.

import pithy.meta as meta
import muck
import re

from pithy import *
from pithy.ansi import *


entity_replacements = muck.source('websters-entities.json')


space_pattern = r'\s+'
word_pattern = r"[-'\w]+"
pronunciation_pattern = r'["*`|/]+'
entity_pattern = r'&[^;\s]*;' # note: this is equivalent to that in websters-entities.txt.py.

# any characters not matched by these patterns will be lexed together into a leaf token as well.
leaf_choices = [space_pattern, word_pattern, pronunciation_pattern, entity_pattern]

# this regex matches tokens for 'clean' words, omitting the pronunciation punctuation.
clean_word_token_re = re.compile('|'.join((space_pattern, word_pattern)))

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
    return ''.join(self.walk_all())

  def __getitem__(self, key):
    if isinstance(key, slice):
      return type(self)(*super().__getitem__(key))
    return super().__getitem__(key)

  name = 'Tree'
  ansi_color = ''
  ansi_reset = ''

  @property
  def is_flawed(self):
    return isinstance(self, TreeFlawed) or self.has_flawed_els

  @property
  def has_flawed_els(self):
    return any(isinstance(el, Tree) and el.is_flawed for el in self)

  @property
  def contents(self):
    if len(self) < 2: raise ValueError('bad Tree: {!r}'.format(self))
    return islice(self, 1, len(self) - 1) # omit start and end tag.


  def walk_all(self):
    for el in self:
      if is_str(el):
        yield el
      else:
        yield from el.walk_all()


  def walk_contents(self):
    for el in self.contents:
      if is_str(el):
        yield el
      else:
        yield from el.walk_contents()


  def walk_branches(self, should_enter_tag_fn=lambda tag: True):
    for el in self:
      if isinstance(el, Tree):
        yield el
        if should_enter_tag_fn(el[0]):
          yield from el.walk_branches(should_enter_tag_fn=should_enter_tag_fn)


  def _structured_desc(self, res, depth):
    'multiline indented description helper.'
    if self.ansi_color: res.append(self.ansi_color)
    res.append(self.name)
    res.append(':')
    if self.ansi_reset: res.append(self.ansi_reset)
    d = depth + 1
    nest_spacer = '\n' + ('  ' * d)
    spacer = ' ' # the spacer to use for string tokens.
    for el in self:
      if is_str(el):
        if spacer: res.append(spacer)
        res.append(repr(el))
        spacer = ''
      else:
        res.append(nest_spacer)
        el._structured_desc(res, d)
        spacer = nest_spacer

  def structured_desc(self, depth=0):
    res = []
    self._structured_desc(res, depth)
    return ''.join(res)


class TreeRoot(Tree):
  name = 'Root'
  @property
  def contents(self):
    return self # no tags at root level.


class TreeFlawed(Tree):
  'abstract parent of the various flaw types.'
  pass


class TreeUnexpected(TreeFlawed):
  'unexpected trees consist solely of an unpaired closing tag.'

  name = 'Unexpected'
  ansi_color = TXT_R
  ansi_reset = RST_TXT

  def __new__(cls, *args):
    assert len(args) == 1
    return super().__new__(cls, *args)

  @property
  def contents(self):
    assert len(self) == 1
    return ()


class TreeUnterminated(TreeFlawed):
  'unterminated trees are missing a closing tag.'

  name = 'Unterminated'
  ansi_color = TXT_M
  ansi_reset = RST_TXT

  @property
  def contents(self):
    return islice(self, 1, len(self)) # omit the start tag only.


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
      return Tree(*subs), pos
    elif token == parent_end_token: # parent end; missing end token.
      match_stream.push(match) # put the parent end token back into the stream.
      return TreeUnterminated(*subs), pos
    else: # unexpected end token.
      subs.append(TreeUnexpected(token))
  # end.
  flush_leaf(pos, len(text))
  return TreeRoot(*subs) if depth == 0 else TreeUnterminated(*subs), len(text)


def parse_tree(text, leaf_replacements=None):
  match_stream = IterBuffer(lexer.finditer(text))
  res, pos = _parse_tree(leaf_replacements or {}, text, match_stream, pos=0, depth=0,
    subs=[], parent_end_token=None, end_token=None)
  return res

