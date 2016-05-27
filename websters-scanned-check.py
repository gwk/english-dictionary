#!/usr/bin/env python3

import json
import muck
import re

from pithy import *

records = muck.source('websters-scanned.json')


tech_issues = 0
defn_issues = 0
for name, tech, defns in records:
  def warn(fmt, *items):
    global tech_issues
    tech_issues += 1
    errFL('\n{}:\n  {!r}\n  ' + fmt, name, tech, *items)
  m = re.search(r' \(([^-=#`"0-9a-zA-Zäéêôü])', tech)
  if m: warn('paren punctuation: {!r}', m.group(1))

  for defn in defns:
    def warn(fmt, *items):
      global defn_issues
      defn_issues += 1
      errFL('\n{}:\n  {!r}\n  ' + fmt, name, defn, *items)


outFL('tech issues: {}; defn issues: {}', tech_issues, defn_issues)
exit(any((tech_issues, defn_issues)))
