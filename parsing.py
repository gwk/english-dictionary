
import re

from pithy import *
from pithy.ansi import *


class ParseTree(tuple):
  def __repr__(self):
    return type(self).__name__ + super().__repr__()

class Parens(ParseTree):
  def __str__(self):
    return '({})'.format(' '.join(str(el) for el in self))

class Brackets(ParseTree):
  def __str__(self):
    return '[{}]'.format(' '.join(str(el) for el in self))

class Brackets(ParseTree):
  def __str__(self):
    return '{{{}}}'.format(' '.join(str(el) for el in self))


class TagTree(ParseTree):
  def 

def mk_tag_type(tag_name):
  class ParseTree_type(ParseTree):
    def __str__(self):
      return '<{}>{}</{}>'.format(tag_name, ' '.join(str(el) for el in self), tag_name)
  name = 'Tag_' + tag_name.capitalize()
  ParseTree_type.__name__ = name
  ParseTree_type.__qualname__ = name
  return ParseTree_type

def is_tree_flawed(tree):
  if isinstance(tree, str):
    return tree in '])}ø'
  return any(is_tree_flawed(el) for el in tree)


nests = {
  '(' : (')', Parens),
  '[' : (']', Brackets),
  '{' : ('}', Braces),
}

nest_closers = '])'


def lex_leaf(text):
  return text.split()

_lex_choice = '|'.join(re.escape(c) for c in '()[]{}')
_lex_re = re.compile('({})'.format(_lex_choice))

def lex_body(text):
  return [t for t in _lex_re.split(text) if t]    


def parse_nest(text):
  seq = lex_body(text)
  res = []
  pos = 0
  while pos < len(seq):
    t = seq[pos]
    try: # opener?
      closer, nest_class = nests[t]
    except KeyError: # not opener.
      res.extend(lex_leaf(t))
      pos += 1
    else: # opener.
      sub, pos = _parse_nest_sub(seq, pos=pos+1, depth=1, closer=closer)
      res.append(nest_class(sub))
  return Nest(res)

def _parse_nest_sub(seq, pos, depth, closer):
  res = []
  while pos < len(seq):
    t = seq[pos]
    if t == closer:
      return res, (pos + 1)
    if t in nest_closers: # unexpected closer; always a flaw.
      res.append('ø')
      return res, pos
    try:
      sub_closer, nest_class = nests[t]
    except KeyError: # regular token; simply advance.
      res.extend(lex_leaf(t))
      pos += 1
    else: # found opener.
      sub, pos = _parse_nest_sub(seq, pos=pos+1, depth=depth+1, closer=sub_closer)
      res.append(nest_class(sub))
  # missing closer at end of seq. auto-repair at the top level only.
  if depth > 1:
    res.append('ø')
  return res, pos


_magenta_null = BG_M + 'ø' + RST

def _desc_for_tree(tree):
  if is_str(tree):
    if tree in nest_closers: return '{}{}{}'.format(BG_R, tree, RST)
    return tree
  assert len(tree) >= 2
  closer = tree[-1]
  return '{}{}{}'.format(
    tree[0],
    ' '.join(_desc_for_tree(el) for el in tree[1:-1]),
    _magenta_null if closer == 'ø' else closer)


def desc_for_tree(tree):
  assert is_tuple(tree)
  return ' '.join(_desc_for_tree(el) for el in tree)


def is_bracket_tree(tree):
  return is_tuple(tree) and tree and tree[0] == '['

def is_paren_tree(tree):
  return is_tuple(tree) and tree and tree[0] == '('

