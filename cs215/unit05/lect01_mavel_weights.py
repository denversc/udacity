# Created on Feb 12, 2013
#
# Write a program to read the Marvel graph and put a strength valu eon each link.
# The "strength" is the number of books in which the characters co-appear.
# Which link has the highest strength value?

import collections
import csv
import pprint

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G

def read_graph(path):
    # Read an undirected graph in CSV format. Each line is an edge
    G = {}
    characters = set()
    with open(path, "rb") as f:
        tsv = csv.reader(f, delimiter='\t')
        for (node1, node2) in tsv:
            make_link(G, node1, node2)
            characters.add(node1)
    return (G, characters)

def get_weights(graph):
    (G, characters) = graph
    weights = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
    for character1 in characters:
        comics = G[character1].iterkeys()
        for comic in comics:
            for character2 in G[comic]:
                if character1 != character2:
                    character1_weights = weights[character1]
                    character1_weights[character2] += 1
    return weights

def get_max_weight(weights):
    max_weight = 0
    max_item = None
    for (character, other_characters) in weights.iteritems():
        for (other_character, weight) in other_characters.iteritems():
            if weight > max_weight:
                max_weight = weight
                max_item = "{} / {}: {}".format(character, other_character, weight)
    return max_item

if __name__ == "__main__":
    graph = read_graph("marvel_characters.txt")
    weights = get_weights(graph)
    max_weight = get_max_weight(weights)
    print("max_weight: {}".format(max_weight))








