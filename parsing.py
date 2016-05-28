
import re

from pithy import *

nest_pairs = {
  '(' : ')',
  '[' : ']',
  '{' : '}'
}

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
  res, pos = _parse_nest(seq, pos=0, depth=0, opener=None, closer=None)
  assert pos == len(seq)
  return res

def _parse_nest(seq, pos, depth, opener, closer):
  res = [opener] if depth > 0 else []
  while pos < len(seq):
    t = seq[pos]
    if t == closer:
      res.append(t)
      return tuple(res), (pos + 1)
    try:
      sub_closer = nest_pairs[t]
    except KeyError: # regular token; simply advance.
      res.extend(lex_leaf(t))
      pos += 1
      continue
    else: # found opener.
      sub_res, pos = _parse_nest(seq, pos=pos+1, depth=depth+1, opener=t, closer=sub_closer)
      res.append(sub_res)
  assert pos == len(seq)
  if depth > 0: # missing closer. auto-repair at the top level only.
    res.append(closer if (depth == 1) else 'ø')
  return tuple(res), pos

def is_tree_flawed(tree):
  if is_str(tree):
    return tree == 'ø'
  return any(is_tree_flawed(t) for t in tree)
