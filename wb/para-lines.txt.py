# Parse the aggregated gutenberg text by coalesting top-level <p> blocks into single lines.

import muck
import re

from pithy.io import outL


text = muck.source('wb/raw-lines.txt')


def is_leading_space_ok(line):
  'incomplete attempt to validate leading space.'
  return any(re.fullmatch(p, line) for p in [
    r' +<i>[^<]+</i>(</blockquote>)?', # common for quote attributions.
    r' \. \. \. .+',
  ])


lines = [] # buffer to aggregate raw lines into a single logical line.
in_para = False
ws_re = re.compile(r'\s')

for i, line in enumerate(text, 1):

  def checkF(cond, fmt, *items):
    if cond: return
    errF('{:>6}: ' + fmt, i, *items)
    errL('; ', repr(line))

  assert line.endswith('\n')

  if line == '\n':
    checkF(not in_para, 'empty line inside paragraph')
    continue

  for m in ws_re.finditer(line):
    ws = m.group(0)
    assert ws == ' ' or ws == '\n'

  line = line[:-1] # remove newline.

  if line.startswith('<p>'):
    checkF(not in_para, 'nested <p>')
    in_para = True
    line = line[3:] # strip opening p tag; line might now be empty again.
  else:
    checkF(in_para, 'missing previous <p>')

  is_closed = line.endswith('</p>')
  if is_closed:
    line = line[:-4] # strip closing p tag.

  # both leading and trailing space cases seem legitimate.
  #checkF(not line[0].isspace() or is_leading_space_ok(line), 'leading space')
  #checkF(not line[-1].isspace(), 'trailing space')
  lines.append(line.strip())

  if is_closed:
    joined = ' '.join(l for l in lines if l)
    if joined:
      outL(joined)
    del lines [:]
    in_para = False
