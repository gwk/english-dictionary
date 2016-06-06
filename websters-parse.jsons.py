# parse record contents:
# - parse and unescape the SGML.
# - unescape additional nonstandard sequences.
# - convert the pronunciation syntax?

import re
import muck
import json

from bs4 import BeautifulSoup
from pithy import *
from Record import Record


def unescape(text):
  return str(BeautifulSoup(text, 'lxml'))


def edit_parse(record):
  n, t, d = record
  return Record(
    name=unescape(n),
    tech=unescape(t),
    defns=tuple(unescape(defn) for defn in d)
  )



muck.transform('websters-scan.jsons', record_types=(Record,), progress_frequency=0.1)
