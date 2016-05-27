#!/usr/bin/env python3

# convert the simplistic records from the previous step into the following structure:
# dict keyed by name strings:
#   lists of grammar `forms`:
#     pronunciation, kind (e.g. noun, adj), etymology, and list of definitions:
#       topic (e.g. botany, music), description.

import sys
import re
import muck
import json

from pithy import *

from parsing import parse_nest


def desc_for_tree(tree):
  if tree is None: return 'ø'
  if not isinstance(tree, tuple): return str(tree)
  return ' '.join(desc_for_tree(el) for el in tree)

def is_bracket_tree(tree):
  return is_tuple(tree) and tree and tree[0] == '['

def is_paren_tree(tree):
  return is_tuple(tree) and tree and tree[0] == '('


tech_issues = 0

def parse_entry(name, tech, defns):
  tech_tree, _ = parse_nest(tech)

  def warn(fmt, *items):
    global tech_issues
    tech_issues += 1
    errFL('{}\n  {}\n  ' + fmt, name, tech, *items)

  if 'ø' in str(tech_tree):
    warn('bad tech tree')



class Entry():

  def __init__(self, name, pre_post, is_etym_labeled):
    pre, post = pre_post
    pron, gram, pre_misc = pre
    etyms, topic, post_misc = post

    self.pron = desc_for_tree(pron)
    self.gram = desc_for_tree(gram)
    self.pre_misc = desc_for_tree(pre_misc)
    self.etyms = desc_for_tree(etyms)
    self.topic = desc_for_tree(topic)
    self.post_misc = desc_for_tree(post_misc)
    self.is_etym_labeled = is_etym_labeled

  def __str__(self):
    return 'Enry: p: {!r}; g: {!r}; pre_m: {!r}; e: {!r} ({}); t: {!r}; post_m: {!r}'.format(
      self.pron, self.gram, self.pre_misc, self.etyms, 'e' if self.is_etym_labeled else 'i',
      self.topic, self.post_misc)



scanned = muck.source('websters-scanned.json')

refined = []
for record in scanned:
  entry = parse_entry(*record)

errFL('tech issues: {}', tech_issues)

json.dump(refined, sys.stdout, indent=2 )
