
nest_pairs = {
  '(' : ')',
  '[' : ']',
  '{' : '}'
}

def lex_leaf(text):
  return text.split()

def parse_nest(text, pos=0, depth=0, opener=None, closer=None):
  res = [opener] if depth > 0 else []
  start = pos
  
  def flush():
    nonlocal start
    if start < pos:
      res.extend(lex_leaf(text[start:pos]))
    start = pos

  while pos < len(text):
    c = text[pos]
    if c == closer:
      flush()
      res.append(c)
      return tuple(res), (pos + 1)
    try:
      sub_closer = nest_pairs[c]
    except KeyError: # regular character; simply advance.
      pos += 1
      continue
    else: # found opener
      flush()
      sub_res, pos = parse_nest(text, pos=pos+1, depth=depth+1, opener=c, closer=sub_closer)
      res.append(sub_res)
      start = pos
  assert pos == len(text)
  flush()
  if depth > 0: # missing closer. auto-repair at the top level only.
    res.append(closer if (depth == 1) else 'ø')
  return tuple(res), pos

