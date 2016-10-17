import muck
from collections import defaultdict
import json
import operator
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

dictionary = muck.source('websters-basics.json')
#print dictionary['Em']['words']
num_words = len(dictionary.keys())
print(num_words)
#word_list = dictionary.keys()
freq_dict = defaultdict(int)
defn_dict = defaultdict(int)
for item in dictionary:
	freq_dict[len(dictionary[item]['words'])] += 1
	defns = dictionary[item]['defns']
	for defn in defns:
		defn_dict[defn] += 1
top5 = dict(sorted(defn_dict.items(), key = operator.itemgetter(1), reverse = True)[:5])

g = nx.DiGraph()
node_list = []
edge_list = []
for item in dictionary:
	node_list.append(item)
	defns = dictionary[item]['defns']
	for defn in defns:
		edge_list.append((item, defn))
		g.add_path([defn, item])

scc_list = nx.strongly_connected_components(g)
print(scc_list)
scc_size = defaultdict(int)
for scc in scc_list:
	scc_size[len(list(scc))] += 1
	'''
	if len(list(scc)) > 5:
		#print strongly connected components of length > 5
		print(list(scc))
	'''
print(scc_size)
#Print histogram of scc size distribution
X = np.arange(len(scc_size))
plt.bar(X, scc_size.values(),align = 'center', width = 0.5)
plt.xticks(X, scc_size.keys())
max_y = max(scc_size.values()) + 1
plt.ylim(0, max_y)
plt.show()