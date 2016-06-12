# fix up the patched aggregate text, producing the final raw lines.

import muck
import re

from pithy import *


with Transformer(muck.source('websters-p-misc.txt'), log_stem=argv[1]) as t:

  @t.drop
  def alphabet_headers(line):
    return re.fullmatch(r'<p><point26>\w\.</point26></p>\n', line)

  @t.drop
  def page_num_paragraphs(line):
    return re.fullmatch(r'<p><![^>]*></p>\n', line)

  @t.edit
  def page_num_inlines(line):
    return re.sub(r'<![^>]*>', '', line)

  @t.conv
  def br_tags(line):
    return re.sub(r'<BR>', '&NewLine;', line)

  t.put(outZ)
