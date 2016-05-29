#!/usr/bin/env python3

import json
import muck
import re

from pithy import *

from parsing import *

records = muck.source('websters-scan.json')


tech_issues = 0
defn_issues = 0


def check_record(name, tech, defns):

  tech_tree = parse_nest(tech)

  def warn_tech(fmt, *items):
    global tech_issues
    tech_issues += 1
    errFL('\ntech: {}:\n  {}\n  {}\n  ' + fmt, name, tech, tech_tree, *items)

  if not tech_tree:
    warn_tech('empty')

  # there appears to be a character escaping scheme of the form ' (…'.
  # this check caught the most obvious ones; the fix is applied in fix_tech().
  # some others exist, but have too many false positives, and so have been patched by hand:
  # - ' (-' collides with legitimate parenthetical pronunciatian hints.
  # - ' (n' and some other letters appear to be a sort of quotation.
  m = re.search(r' \(([^-=#`"0-9a-zA-Zäéêôü])', tech)
  if m: warn_tech('paren punctuation: {!r}', m.group(1))

  if re.search('[{}]', tech): warn_tech('braces')

  m = re.search(r'; (\d+\)?)', tech)
  if m: warn_tech('escape sequence: {!r}', m.group(1))

  if is_tree_flawed(tech_tree): warn_tech('flawed tech tree')

  if not defns:
    warn_tech('empty defns')

  for defn in defns:
    def warn_defn(fmt, *items):
      global defn_issues
      defn_issues += 1
      errFL('\ndefn: {}:\n  {!r}\n  ' + fmt, name, defn, *items)
    for c in defn:
      if c in '{}':
        warn_defn('braces')
        break
  
for r in records:
  check_record(*r)

outFL('\nrecords: {}; tech issues: {}; defn issues: {}',
  len(records), tech_issues, defn_issues)

exit(any((tech_issues, defn_issues)))
