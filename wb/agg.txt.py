# Download and aggregate the raw text sources.
# Use the original MICRA v0.50 sources hosted at Project Gutenberg;
# The other versions on Project Gutenberg have been post-processed and seem to have lost some fidelity.

from string import ascii_letters, digits, punctuation

from pithy.fetch import load_url
from pithy.io import err_progress, errL, outZ


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
  url = f'http://www.gutenberg.org/files/{ebook_num}/old/pgw050{letters}.txt'
  file = load_url(url, delay=1, encoding='latin_1')

  # skip the header.
  for i, line in enumerate(file):
    if line == '!>\n':
      errL(f'{letters}: lines skipped: {i}')
      break

  for line in err_progress(file, letters + ': lines scanned'):
    if not all(c in clean_chars for c in line):
      exit(f'unclean line: {line!r}')
    outZ(line)
