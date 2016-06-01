
import muck
import re

from pithy import *
from Record import Record


punctuation_escape_re = re.compile(r' \(([][()/.,; ])')

dangling_paren_re = re.compile(r'(\([^][();,-]+)(\]|$)')

remove_various_re = re.compile(r'''(?x)
  [{}] # manually reviewed; braces occur in only a few places and serve no useful purpose.
| \(;\ 48\) # some weird escape pattern.
| ;\ 48\)   # same, but without leading paren.
| ;\ 48,\ 61\) # single occurrence for DISADVANTAGE.
''')


def transform_tech(record):
  'apply various fixes to the technical line.'
  tech = record.tech
  tech = punctuation_escape_re.sub(lambda m: m.group(1), tech)
  tech = tech.rstrip(' (') # lots of trailing open-parens.
  tech = dangling_paren_re.sub(lambda m: m.group(1) + ')]', tech)
  tech = remove_various_re.sub('', tech)
  return record._replace(tech=tech)


def fix_defn(defn):
  defn = remove_various_re.sub('', defn)
  return defn


#return Record(name, fix_tech(tech), [fix_defn(d) for d in defns])


muck.transform('websters-scan.jsons', record_types=(Record,))
