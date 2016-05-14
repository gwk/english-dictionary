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
from pithy.nestparser import NestParser

parser = NestParser()

def is_tree_paren(tree):
  return is_tuple(tree) and tree and tree[0] == '('

def is_tree_bracket(tree):
  return is_tuple(tree) and tree and tree[0] == '['

def is_tree_mismatched(tree):
  return isinstance(tree, tuple) and tree[-1] is None

def tree_contains_mismatched(tree):
  return isinstance(tree, tuple) and \
    (tree[-1] is None or any(tree_contains_mismatched(el) for el in tree))

def desc_for_tree(tree):
  if tree is None: return 'ø'
  if not isinstance(tree, tuple): return str(tree)
  return ' '.join(desc_for_tree(el) for el in tree)

def desc_for_tree_contents(tree):
  if tree is None: return None
  return ' '.join(desc_for_tree(el) for el in tree[1:-1])


implied_etym_heads = {'F.'}

class Entry():

  def __init__(self, text):
    cost, tree = parser.parse(text)

    etym = None
    etym_i = None
    topic = None
    pron = []
    is_pron_open = True
    misc = []

    for i, el in enumerate(tree):
      if is_str(el):
        words = el.split()
      else:
        
      if etym is None and el == 'Etym:':
        etym_i = i + 1
        is_pron_open = False

      elif i == etym_i:
        etym = tree[etym_i]
        if not is_tree_bracket(etym):
          failFL('WARNING: malformed etym element following label: {!r}', text)

      elif is_tree_bracket(el) and el and el[0] in implied_etym_heads:
        etym = el
        is_pron_open = False

      elif (topic is None) and is_tree_paren(el):
        topic = el
        is_pron_open = False

      elif is_pron_open:
        pron.append(el)

      else:
        misc.append(el)

    self.is_etym_labeled = (etym_i is not None)

    if etym_i and not etym:
      errFL('WARNING: missing etymology following label: {!r}', text)

    if tree_contains_mismatched(tree):
      errL(text)
      errL('  TREE: ', tree)
      errL('  TREE: ', desc_for_tree(tree))
      #errL('  PRON: ', pron)
      #errL('  MISC: ', misc)

    self.pron = desc_for_tree(pron)
    self.etym = desc_for_tree_contents(etym)
    self.topic = desc_for_tree_contents(topic)
    self.misc = desc_for_tree(misc)

  def __str__(self):
    return 'Enry: p: {!r}; e: {!r} ({}); t: {!r}; m: {!r};'.format(
      entry.pron, entry.etym, 'e' if entry.etym_labeled else 'i', entry.topic, entry.misc)



records = muck.source('websters-scanned.json')

for name, entries in records:
  if name > 'B': break
  assert(entries)
  for entry_str, defn_strings in entries:
    entry = Entry(entry_str)
    if entry.etym and not entry.is_etym_labeled:
      errFL('{}: {!r}; {!r}', name, entry_str, entry.etym)

json.dump({}, sys.stdout)
