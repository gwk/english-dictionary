#!/usr/bin/env python3

import sys
import muck


# https currently fails with handshake error; stock py3 3.5.1 ships with 'OpenSSL 0.9.8zh 14 Jan 2016'.
# http works fine.
file = muck.source_url('http://www.gutenberg.org/ebooks/29765.txt.utf-8')

# read and then write out to get rid of '\r\n' line endings in the original.
for line in file:
  sys.stdout.write(line)
