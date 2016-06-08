# create a translation table for the entities found in the text.

# the webfont.txt document provides a translation table,
# but my effort to use it programmatically proved useless;
# of the nonstandard entities found, the table provided now helpful translations.
# it does however offer insight into what characters they stand for;
# this script constructs replacements as needed.


import html.entities as std_entities
import muck
import unicodedata

from pithy import *


# this dictionary was transcribed from the micra webfont.txt documentation file.
# it served as the hints with which some entities below were created by hand.
micra_webfont_entity_descriptions = { k.strip(' *</') : v for (k, v) in \
  muck.source('micra-webfont-entities.json').items() }

# all the found entities.
entities = [line.strip() for line in muck.source('websters-entities.txt')]

# the html5 entities dictionary has some keys without semicolons;
# ignore these (overly loose / modern for our purposes),
# and create a new dictionary that omits the semicolons.
ent_html5 = { k[:-1] : v for k, v in std_entities.html5.items() if k.endswith(';') }

# just for curiosity's sake, also check if entities are in the xhtml table;
# this is interesting only because the micra text is much older than html5,
# so perhaps these are SGML or nonstandard codes that got added.
ent_xhtml = std_entities.entitydefs


manual = {
  '?'       : '(?)',

  'CHI'     : 'Χ', # GREEK CAPITAL LETTER CHI.
  'DELTA'   : 'Δ', # GREEK CAPITAL LETTER DELTA.
  'GAMMA'   : 'Ɣ', # LATIN CAPITAL LETTER GAMMA.
  'LAMBDA'  : 'Λ', # GREEK CAPITAL LETTER LAMDA.
  'OMEGA'   : 'Ω', # GREEK CAPITAL LETTER OMEGA.
  'OMICRON' : 'Ο', # GREEK CAPITAL LETTER OMICRON.
  'PI'      : 'Π', # GREEK CAPITAL LETTER PI.
  'SIGMA'   : 'Σ', # GREEK CAPITAL LETTER SIGMA.
  'TAU'     : 'Τ', # GREEK CAPITAL LETTER TAU.
  'THETA'   : 'Θ', # GREEK CAPITAL LETTER THETA.
  'UPSILON' : 'Υ', # GREEK CAPITAL LETTER UPSILON.

  'Aquarius'    : '(Aquarius)',
  'Aries'       : '(Aries)',
  'Cancer'      : '(Cancer)',
  'Capricorn'   : '(Capricorn)',
  'Jupiter'     : '(Jupiter)',
  'Leo'         : '(Leo)',
  'Libra'       : '(Libra)',
  'Pisces'      : '(Pisces)',
  'Sagittarius' : '(Sagittarius)',
  'Scorpio'     : '(Scorpio)',
  'Sun'         : '(Sun)',
  'Taurus'      : '(Taurus)',
  'Virgo'       : '(Virgo)',

  'libra'       : '(Libra)',
  'mercury'     : '(Mercury)',
  'sagittarius' : '(Sagittarius)',
  'scorpio'     : '(Scorpio)',
  'taurus'      : '(Taurus)',
  'pisces'      : '(Pisces)',
  
  'asterism'  : '⁂', # ASTERISM.
  'cuberoot'  : '∛', # CUBE ROOT.
  'umlaut'    : '¨', # DIAERESIS.
  'yogh'      : 'ȝ', # LATIN SMALL LETTER YOGH.
  'til'       : '~', # guess.
  'oomac'     : 'ꝏ\u0304', # LATIN SMALL LETTER OO, COMBINING MACRON. guess.
  '/amacr'    : 'a\u0304', # COMBINING MACRON. looks like slash is just a typo.
  
  'frac00'        : '0/0',
  'frac1000x1434' : '1000/1434',
  'frac12x13'     : '12/13',
  'frac17'        : '⅐', # VULGAR FRACTION ONE SEVENTH.
  'frac17x175'    : '17/175',
  'frac19'        : '⅑', # VULGAR FRACTION ONE NINTH.
  'frac1x10'      : '⅒', # VULGAR FRACTION ONE TENTH.
  'frac1x10000'   : '1/1000',
  'frac1x108719'  : '1/108719',
  'frac1x12'      : '1/12',
  'frac1x20'      : '1/20',
  'frac1x216000'  : '1/21600',
  'frac1x24'      : '1/24',
  'frac1x2500'    : '1/2500',
  'frac1x29966'   : '1/29966',
  'frac1x3600'    : '1/3600',
  'frac1x50000'   : '1/50000',
  'frac1x60'      : '1/60',
  'frac1x6000'    : '1/6000',
  'frac1x8000'    : '1/8000',
  'frac2x10'      : '2/10',
  'frac32'        : '3/2',
  'frac36'        : '3/6',
  'frac3x16'      : '3/16',
  'frac43'        : '4/3',
  'frac59'        : '5/9',
  'frac925x1000'  : '925/1000',
  'frac95'        : '9/5',
  'fract25x100'   : '25/100',
}

guess_pairs = [
  ('breve', '\u0306'),  # COMBINING BREVE.
  ('dot',   '\u0307'),  # COMBINING DOT ABOVE. micra: 'dot above'.
  ('macr',  '\u0304'),  # COMBINING MACRON. guess.
  ('sl',    '\u0304\u030D'), # COMBINING MACRON, COMBINING VERTICAL LINE ABOVE. micra: 'semilong'.
  ('sd',    '\u0323'),  # COMBINING DOT BELOW. guess that this is shorthand for 'sdot'.
  ('sdot',  '\u0323'),  # COMBINING DOT BELOW. micra: 'r with a dot below'; 'Sanskrit/Tamil d/n/t dot'.
  ('sm',    '\u0331'),  # COMBINING MACRON BELOW. micra: 'sub-macron'.
  ('smac',  '\u0331'),  # COMBINING MACRON BELOW. guess.
  ('til', '\u0303'),    # COMBINING TILDE. guess.
  ('tilde', '\u0303'),  # COMBINING TILDE.

  # micra: vowels with a double dot *underneath*,
  # e.g. a (as in all) have no representation in this character set,
  # and, where explicitly entered in the dictionary,
  # are represented by <xdd/ where "x" is the letter, as in "<add/".
  ('dd', '\u0324'), # COMBINING DIAERESIS BELOW.
]

known_multichars = {
  'oe' : 'œ', # LATIN SMALL LIGATURE OE.
  'ae' : 'æ', # LATIN SMALL LETTER AE.
  'oo' : 'ꝏ' # LATIN SMALL LETTER OO. unfortunately this appears to be a double-width character.
}

def guess_trans(e):
  for suffix, combiners in guess_pairs:
    try:
      a = clip_suffix(e, suffix)
    except ValueError: continue
    if len(a) != 1:
      try:
        a = known_multichars[a]
      except KeyError: continue
    t = a + combiners
    #errSL('guessed:', e, '->', t) # note: this outputs the decomposed characters.
    return t
  return None


def get_trans(e):
  if e in manual:
    return manual[e]

  c = ent_html5.get(e)
  if c:
    #errFL('html5: {} -> {}{}', e, c, '' if e in ent_xhtml else '  (not xhtml)')
    return c

  c =guess_trans(e)
  if c: return c

  errFL('unknown entity: {}', e)
  d = micra_webfont_entity_descriptions.get(e)
  if d: errFL('micra webfont note: {}', d)

  return '({}?)'.format(e)

# prefer composed characters over combining sequences.
trans = { '&{};'.format(e) : unicodedata.normalize('NFC', get_trans(e)) for e in entities }

out_json(trans)

