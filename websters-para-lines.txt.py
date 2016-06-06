# parse the aggregated gutenberg text by coalesting top-level <p> blocks into single lines.

import json
import muck
import re

from pithy import *


text = muck.source('websters-raw-lines.txt')


def is_leading_space_ok(line):
  return any(re.fullmatch(p, line) for p in [
    r' +<i>[^<]+</i>(</blockquote>)?', # common for quote attributions.
    r' \. \. \. .+',
  ])


lines = [] # buffer to aggregate raw lines into a single logical line.
in_para = False

for i, line in enumerate(text, 1):

  def checkF(cond, fmt, *items):
    if cond: return
    errF('{:>6}: ' + fmt, i, *items)
    errL('; ', repr(line))

  assert line.endswith('\n')

  if line == '\n':
    checkF(not in_para, 'empty line inside paragraph')
    continue

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
  
  if line:
    #checkF(not line[0].isspace() or is_leading_space_ok(line), 'leading space')
    #checkF(not line[-1].isspace(), 'trailing space')
    lines.append(line.strip())

  if is_closed:
    if lines:
      outL(' '.join(lines))
    del lines [:]
    in_para = False
