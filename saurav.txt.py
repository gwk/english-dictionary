import muck
from collections import defaultdict
import json
import operator
#import networkx as nx

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

#g = nx.Graph()
node_list = []
edge_list = []
for item in dictionary:
	node_list.append(item)
	defns = dictionary[item]['defns']
	for defn in defns:
		edge_list.append((item, defn))

print(len(node_list))
#print(edge_list)
print(top5)
#print(freq_dict)
