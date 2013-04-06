#
# This is the same problem as "Distance Oracle I" except that instead of
# only having to deal with binary trees, the assignment asks you to
# create labels for all tree graphs.
#
# In the shortest-path oracle described in Andrew Goldberg's
# interview, each node has a label, which is a list of some other
# nodes in the network and their distance to these nodes.  These lists
# have the property that
#
#  (1) for any pair of nodes (x,y) in the network, their lists will
#  have at least one node z in common
#
#  (2) the shortest path from x to y will go through z.
#
# Given a graph G that is a tree, preprocess the graph to
# create such labels for each node.  Note that the size of the list in
# each label should not be larger than log n for a graph of size n.
#

#
# create_labels takes in a tree and returns a dictionary, mapping each
# node to its label
#
# a label is a dictionary mapping another node and the distance to
# that node
#

def average_distance_in_hops(G, node):
    distances = {}
    unvisited = [(node, 0)]

    while unvisited:
        (node, num_hops) = unvisited[0]
        del unvisited[0]
        distances[node] = num_hops

        for adjacent_node in G[node]:
            if adjacent_node not in distances:
                unvisited.append((adjacent_node, num_hops + 1))

    num_distances = len(distances)
    if num_distances == 0:
        average_num_hops = 0
    else:
        total_distances = sum(distances.itervalues())
        average_num_hops = total_distances / num_distances

    return average_num_hops

def add_label_to(G, labels, root):
    unvisited = [(root, 0)]
    visited = set()

    while unvisited:
        (node, path_weight) = unvisited[0]
        del unvisited[0]
        visited.add(node)

        for (adjacent_node, adjacent_edge_weight) in G[node].iteritems():
            if adjacent_node not in visited:
                new_path_weight = path_weight + adjacent_edge_weight
                adjacent_node_label = labels[adjacent_node]
                adjacent_node_label[root] = new_path_weight
                unvisited.append((adjacent_node, new_path_weight))

def create_labels(treeG):
    # special case: if the graph is empty, return an empty graph;
    # this avoid having to check for an empty graph over and over again below
    if len(treeG) == 0:
        return {}

    labels = {}

    # add a label for each node to itself
    for node in treeG:
        labels[node] = {node: 0}

    # find the node with the shortest average distance (in number of hops, not
    # edge weights) to all other nodes
    middle_node = min(treeG, key=lambda x: average_distance_in_hops(treeG, x))

    # add the middle node to the labels of all other nodes in the graph
    add_label_to(treeG, labels, middle_node)

    return labels

#######
# Testing
#


def get_distances(G, labels):
    # labels = {a:{b: distance from a to b,
    #              c: distance from a to c}}
    # create a mapping of all distances for
    # all nodes
    distances = {}
    for start in G:
        # get all the labels for my starting node
        label_node = labels[start]
        s_distances = {}
        for destination in G:
            shortest = float('inf')
            # get all the labels for the destination node
            label_dest = labels[destination]
            # and then merge them together, saving the
            # shortest distance
            for intermediate_node, dist in label_node.iteritems():
                # see if intermediate_node is our destination
                # if it is we can stop - we know that is
                # the shortest path
                if intermediate_node == destination:
                    shortest = dist
                    break
                other_dist = label_dest.get(intermediate_node)
                if other_dist is None:
                    continue
                if other_dist + dist < shortest:
                    shortest = other_dist + dist
            s_distances[destination] = shortest
        distances[start] = s_distances
    return distances

def make_link(G, node1, node2, weight=1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G

import math
import unittest

class ProvidedTests(unittest.TestCase):

    def process_graph(self):
        edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7),
                 (4, 8), (4, 9), (5, 10), (5, 11), (6, 12), (6, 13)]
        tree = {}
        for n1, n2 in edges:
            make_link(tree, n1, n2)
        labels = create_labels(tree)
        distances = get_distances(tree, labels)
        return distances

    @unittest.expectedFailure
    def test1(self):
        distances = self.process_graph()
        self.assertEqual(distances[1][2], 1)

    @unittest.expectedFailure
    def test2(self):
        distances = self.process_graph()
        self.assertEqual(distances[1][4], 2)

class DistanceOracle2TestCase(unittest.TestCase):

    def create_graph(self):
        raise NotImplementedError()

    def calculate_distances(self):
        G = self.create_graph()
        labels = create_labels(G)

        # make sure that the size of each label is less than log(n)
        max_label_size = math.log(len(G), 2)
        max_label_size = int(math.ceil(max_label_size))
        for (node, label) in labels.iteritems():
            label_size = len(label)
            self.assertLessEqual(label_size, max_label_size,
                "label for node {} has size {}, which is greater than the "
                "maximum, log(n={})={}".format(node, label_size, len(G),
                max_label_size))

        return get_distances(G, labels)

    def assert_distance(self, node1, node2, expected_distance):
        distances = self.calculate_distances()
        actual_distance = distances[node1][node2]
        self.assertEqual(actual_distance, expected_distance)

class Test_OneNodeGraph(unittest.TestCase):

    def test(self):
        G = {1: {}}
        labels = create_labels(G)
        self.assertDictEqual(labels, {1: {1: 0}})

class Test_3NodeChain(DistanceOracle2TestCase):

    def create_graph(self):
        G = {}
        make_link(G, 1, 2, 10)
        make_link(G, 2, 3, 20)
        return G

    def test_1to1(self):
        self.assert_distance(1, 1, 0)

    def test_1to2(self):
        self.assert_distance(1, 2, 10)

    def test_1to3(self):
        self.assert_distance(1, 3, 30)

    def test_2to1(self):
        self.assert_distance(2, 1, 10)

    def test_2to2(self):
        self.assert_distance(2, 2, 0)

    def test_2to3(self):
        self.assert_distance(2, 3, 20)

    def test_3to1(self):
        self.assert_distance(3, 1, 30)

    def test_3to2(self):
        self.assert_distance(3, 2, 20)

    def test_3to3(self):
        self.assert_distance(3, 3, 0)

