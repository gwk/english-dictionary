# fix up the patched aggregate text, producing the final raw lines.

import muck
import re

from pithy import *


with muck.transform('websters-p-misc.txt') as t:

  @t.drop
  def alphabet_headers(line):
    return re.fullmatch(r'<p><point26>\w\.</point26></p>\n', line)

  @t.drop
  def page_num_paragraphs(line):
    return re.fullmatch(r'<p><![^>]*></p>\n', line)

  @t.edit
  def page_num_inlines(line):
    return re.sub(r'<![^>]*>', '', line)

  @t.edit
  def bracket_slash_lt_mark(line):
    # this sequence appears in some of the pronunciations,
    # and the bracket breaks parsing.
    return re.sub(r'\]/>', '', line)

  @t.conv
  def br_tags(line):
    # br is the only tag in use that does not have a matching close tag.
    # we do the easy thing, which is to use the modern NewLine entity;
    # alternatively we could add handling for the modern <…/> tag syntax,
    # and fix all of the br tags to use it, or add a special case to the parser.
    # this conversion introduces a large number of changes to the text,
    # but since the tag was presumably inserted by the typists,
    # and the newline entity has equivalent semantic value, this seems like the best choice.
    return re.sub(r'<BR>', '&NewLine;', line)

  t.put(outZ)
