
import pithy.meta as meta
import muck
import re

from pithy import *
from pithy.ansi import *


entities_map = muck.source('websters-entities-map.json')
entity_choices = '|'.join(re.escape(e) for e in entities_map)
entities_re = re.compile('({})'.format(entity_choices))

def lex_leaf(text):
  return entities_re.sub(lambda m: entities_map[m.group()], text).split()


class Tree(tuple):
  'base class for parse tree nodes.'
  start = ''
  end = ''

  def __repr__(self):
    return type(self).__name__ + super().__repr__()

  def __str__(self):
    return '{}{}{}'.format(self.start, ' '.join(str(el) for el in self), self.end)

  def colored_name(self):
    n = type(self).__name__
    if isinstance(self, UnexpectedEnd): return TXT_R + n + RST_TXT
    if isinstance(self, MissingEnd): return TXT_M + n + RST_TXT
    if isinstance(self, Flawed): return TXT_Y + n + RST_TXT
    return n

  def desc(self, _depth=0):
    'multiline indented description. _depth is a private recursive parameter.'

    strings = [self.colored_name(), '(']
    if all(isinstance(el, str) for el in self):
      strings.append(repr(' '.join(self)))
    else:
      d = _depth + 1
      for el in self:
        strings.append('\n')
        strings.append('  ' * d)
        if isinstance(el, str): strings.append(el)
        else: strings.extend(el.desc(d))
    strings.append(')')
    return strings if _depth else ''.join(strings)


class Flawed(): pass

class MissingEnd(Flawed): pass

class UnexpectedEnd(Flawed): pass


@memoize()
def mk_tree_type(_start, _end):
  class TreeType(Tree):
    start = _start
    end = _end
  return meta.rename(TreeType, 'Tag_' + re.sub(r'[^a-zA-Z0-9]', '_', _start))

# rename these more appropriately.
Parens    = meta.rename(mk_tree_type('(', ')'), 'Parens')
Brackets  = meta.rename(mk_tree_type('[', ']'), 'Brackets')
Braces    = meta.rename(mk_tree_type('{', '}'), 'Braces')

Tag_hw = mk_tree_type('<hw>', '</hw>')


@memoize()
def mk_flawed_type(base_type, *flaws):
  if not flaws: return base_type
  class TreeFlawedType(base_type, *flaws): pass
  return meta.rename(TreeFlawedType, base_type.__name__ + '_' + '_'.join(f.__name__ for f in flaws))


start_choices = (r'(\()', r'(\[)', r'(\{)', r'<([^/>]*)>')
end_choices   = (r'(\))', r'(\])', r'(\})', r'</([^>]*)>')
end_formats = (')', ']', '}', '</$>')

assert len(start_choices) == len(end_choices)

lexer_pattern = '|'.join(start_choices + end_choices)
lexer = re.compile(lexer_pattern)

choices_count = len(start_choices)


def _parse_tree(text, match_stream, pos, depth, parent_end_index, end_index, tree_type):
  subs = []
  unexpected_end = False
  missing_end = False
  def res():
    flaws = ()
    if unexpected_end:
      flaws += (UnexpectedEnd,)
    if missing_end:
      flaws += (MissingEnd,)
    if any(isinstance(sub, Flawed) for sub in subs):
      flaws += (Flawed,)
    return mk_flawed_type(tree_type, *flaws)(subs)

  for match in match_stream:
    start_index = match.start()
    subs.extend(lex_leaf(text[pos:match.start()])) # leaf tokens.
    match_index = match.lastindex
    assert match_index is not None # all choices in the regex must be a paren group.
    value = match.group(match_index)
    pos = match.end()
    if match_index == end_index:
      return res(), pos
    elif match_index <= choices_count: # found a start token (groups are 1-indexed).
      start_str = match.group()
      end_str = end_formats[match_index - 1].replace('$', value)
      sub_type = mk_tree_type(start_str, end_str)
      sub, pos = _parse_tree(text, match_stream, pos, depth + 1, parent_end_index=end_index,
        end_index=(match_index + choices_count), tree_type=sub_type)
      subs.append(sub)
    elif end_index > 0 and match_index == parent_end_index: # parent end; missing end token.
      match_stream.push(match) # put the parent end token back into the stream.
      missing_end = True
      return res(), pos
    else: # unexpected end token.
      has_unexpected_end = True
      subs.append(match.group())
  # end.
  if end_index > 0: # not the root; missing end token.
    missing_end = True
  subs.extend(lex_leaf(text[pos:])) # leaf tokens.
  return res(), len(text)


def parse_tree(text):
  match_stream = IterBuffer(lexer.finditer(text))
  res, pos = _parse_tree(text, match_stream, pos=0, depth=0, parent_end_index=0, end_index=0, tree_type=Tree)
  return res


__all__ = ['parse_tree', 'Flawed', 'MissingEnd', 'UnexpectedEnd']
