# download and aggregate the raw text sources.
# use the original MICRA v0.50 sources hosted at Project Gutenberg;
# the other versions have been processed and seem to have lost some fidelity.

import muck
from string import digits, ascii_letters, punctuation
from pithy import *

sources = [
  (660, 'ab'),
  (661, 'c'),
  (662, 'de'),
  (663, 'fh'),
  (664, 'il'),
  (665, 'mo'),
  (666, 'pq'),
  (667, 'r'),
  (668, 's'),
  (669, 'tw'),
  (670, 'xz'),
]

clean_chars = set(digits + ascii_letters + punctuation + ' \n')

for ebook_num, letters in sources:
  url = 'http://www.gutenberg.org/files/{}/old/pgw050{}.txt'.format(ebook_num, letters)
  file = muck.source_url(url, delay=1, encoding='latin_1')

  # skip the header.
  for i, line in enumerate(file):
    if line == '!>\n':
      errFL('{}: lines skipped: {}', letters, i)
      break

  for line in err_progress(file, letters + ': lines scanned'):
    if not all(c in clean_chars for c in line):
      failFL('unclean line: {!r}', line)
    outZ(line)
