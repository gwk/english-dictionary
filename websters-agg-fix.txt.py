import muck
import re

from pithy import *


def drop_page_nums(line):
  return re.fullmatch(r'<p><! p\. \d+ !></p>\n', line)


def drop_alphabet_headers(line):
  return re.fullmatch(r'<p><point26>\w\.</point26></p>\n', line)


muck.transform('websters-agg.txt', progress_frequency=0.1)
