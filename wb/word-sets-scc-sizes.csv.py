# Analyze the largest strongly connected component.

from collections import Counter
from operator import itemgetter
from os import environ

from networkx import strongly_connected_components as calc_sccs

import graphs  # Registers '.graph' loader.
from pithy.csv import out_csv
from pithy.io import errL, errSL
from pithy.loader import load


graph = load('wb/word-sets.graph')

sccs = list(calc_sccs(graph))
errL(f'sccs: {len(sccs)}')

hist = Counter(len(scc) for scc in sccs)

out_csv(header=('SCC Size', 'Count'), rows=sorted(hist.items(), reverse=True))
