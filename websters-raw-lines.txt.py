# fix up the patched aggregate text, producing the final raw lines.
# we drop the page numbers here because for the inline page nums,
# it is much easier to read the diffs of short raw lines,
# as opposed to the paragraph lines produced next.

import muck
import re

from pithy import *


def drop_page_num_paragraphs(line):
  return re.fullmatch(r'<p><![^>]*></p>\n', line)


def drop_alphabet_headers(line):
  return re.fullmatch(r'<p><point26>\w\.</point26></p>\n', line)


def edit_page_num_inlines(line):
  return re.sub(r'<![^>]*>', '', line)

def edit_br_tags(line):
  return re.sub(r'<BR>', '&NewLine;', line)

muck.transform('websters-agg-pN-misc.txt')
