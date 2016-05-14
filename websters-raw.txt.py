#!/usr/bin/env python3

import sys
import muck


# https currently fails with handshake error; stock py3 3.5.1 ships with 'OpenSSL 0.9.8zh 14 Jan 2016'.
# http works fine.
muck.fetch('http://www.gutenberg.org/ebooks/29765.txt.utf-8', path=sys.argv[1])
