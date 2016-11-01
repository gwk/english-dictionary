# Analyze the largest strongly connected component.

import muck

from collections import Counter
from operator import itemgetter
from pithy.io import *
from pithy.csv_utils import write_csv
from networkx import strongly_connected_components as calc_sccs

import graphs # registers .graph loader.

graph = muck.load('wb/word-sets-graph.graph')

sccs = list(calc_sccs(graph))
errFL('sccs: {}', len(sccs))

hist = Counter(len(scc) for scc in sccs)

write_csv(stdout, ('SCC Size', 'Count'), sorted(hist.items(), reverse=True))

