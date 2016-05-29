
import muck
import re

from pithy import *


records = muck.source('websters-scan.json')


punctuation_escape_re = re.compile(r' \(([][()/.,; ])')
dangling_paren_re = re.compile(r'(\([^][();,-]+)(\]|$)')

remove_various_re = re.compile(r'''(?x)
  [{}] # manually reviewed; braces occur in only a few places and serve no useful purpose.
| \(;\ 48\) # some weird escape pattern.
| ;\ 48\)   # same, but without leading paren.
| ;\ 48,\ 61\) # single occurrence for DISADVANTAGE.
''')


tech_issues = 0
def fix_tech(tech):
  'apply various fixes to the technical line.'
  tech = punctuation_escape_re.sub(lambda m: m.group(1), tech)
  tech = tech.rstrip(' (') # lots of trailing open-parens.
  tech = dangling_paren_re.sub(lambda m: m.group(1) + ')]', tech)
  tech = remove_various_re.sub('', tech)
  return tech


def fix_defn(defn):
  defn = remove_various_re.sub('', defn)
  return defn


def fix_record(record):
  name, tech, defns = record
  return (name, fix_tech(tech), [fix_defn(d) for d in defns])


out_json(fix_record(r) for r in records)

errFL('tech issues: {}', tech_issues)
