import muck
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

for ebook_num, suffix in sources:
  url = 'http://www.gutenberg.org/files/{}/old/pgw050{}.txt'.format(ebook_num, suffix)
  file = muck.source_url(url, delay=1, encoding='latin_1')

  # skip the header.
  for i, line in enumerate(file):
    if line == '!>\n':
      errFL('{}: skipped {} lines.', suffix, i)
      break

  for line in err_progress_iter(file, suffix):
    outZ(line)
