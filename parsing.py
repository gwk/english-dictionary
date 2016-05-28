
import re

from pithy import *
from pithy.ansi import *


nest_pairs = {
  '(' : ')',
  '[' : ']',
  '{' : '}'
}

nest_closers = frozenset(nest_pairs.values())

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
      closer = nest_pairs[t]
    except KeyError: # not opener.
      res.extend(lex_leaf(t))
      pos += 1
    else: # opener.
      sub, pos = _parse_nest_sub(seq, pos=pos+1, depth=1, opener=t, closer=closer)
      res.append(sub)
  return tuple(res)

def _parse_nest_sub(seq, pos, depth, opener, closer):
  res = [opener]
  while pos < len(seq):
    t = seq[pos]
    if t == closer:
      res.append(t)
      return tuple(res), (pos + 1)
    if t in nest_closers: # unexpected closer; always a flaw.
      res.append('ø')
      return tuple(res), pos
    try:
      sub_closer = nest_pairs[t]
    except KeyError: # regular token; simply advance.
      res.extend(lex_leaf(t))
      pos += 1
    else: # found opener.
      sub, pos = _parse_nest_sub(seq, pos=pos+1, depth=depth+1, opener=t, closer=sub_closer)
      res.append(sub)
  assert pos == len(seq)
  # missing closer at end of seq. auto-repair at the top level only.
  res.append(closer if (depth == 1) else 'ø')
  return tuple(res), pos


def _is_tree_flawed(tree):
  if is_str(tree):
    return tree == 'ø'
  return any(_is_tree_flawed(t) for t in tree)

def is_tree_flawed(tree):
  return any(_is_tree_flawed(el) for el in tree)


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

