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
# Given a graph G that is a balanced binary tree, preprocess the graph to
# create such labels for each node.  Note that the size of the list in
# each label should not be larger than log n for a graph of size n.
#

#
# create_labels takes in a balanced binary tree and the root element
# and returns a dictionary, mapping each node to its label
#
# a label is a dictionary mapping another node and the distance to
# that node
#
def create_labels(binarytreeG, root):
    # The label for each node will contain:
    #   1. its left child
    #   2. its right child
    #   3. each parent node up to the root

    root_children = [x for x in binarytreeG[root]]

    # unvisited contains 3-tuples: (node, children, path_to_root)
    # where "node" is the node itself, "children" is a list containing
    # the node's child nodes, and "path_to_root" is a list of nodes that
    # are the path to the root node.
    unvisited = [(root, root_children, [])]
    labels = {}

    while unvisited:
        (node, children, path_to_root) = unvisited[0]
        del unvisited[0]
        label = {node: 0}
        labels[node] = label

        # add the child nodes to the label
        for child in children:
            node_to_child_weight = binarytreeG[node][child]
            label[child] = node_to_child_weight

        # add the path to the root node to the label
        last_node = node
        distance_to_parent = 0
        for parent in path_to_root:
            last_node_to_parent_weight = binarytreeG[last_node][parent]
            distance_to_parent += last_node_to_parent_weight
            label[parent] = distance_to_parent
            last_node = parent

        # add the child nodes to the queue
        child_path_to_root = [node] + path_to_root
        for child in children:
            child_children = [x for x in binarytreeG[child] if x != node]
            unvisited_element = (child, child_children, child_path_to_root)
            unvisited.append(unvisited_element)

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

import unittest

class ProvidedTests(unittest.TestCase):

    def make_graph(self):
        edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7),
                 (4, 8), (4, 9), (5, 10), (5, 11), (6, 12), (6, 13)]
        tree = {}
        for n1, n2 in edges:
            make_link(tree, n1, n2)
        return tree

    def test1(self):
        tree = self.make_graph()
        labels = create_labels(tree, 1)
        distances = get_distances(tree, labels)
        self.assertEqual(distances[1][2], 1)

    def test2(self):
        tree = self.make_graph()
        labels = create_labels(tree, 1)
        distances = get_distances(tree, labels)
        self.assertEqual(distances[1][4], 2)

class DenverTests(unittest.TestCase):

    def make_graph(self):
        edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7),
                 (4, 8), (4, 9), (5, 10), (5, 11), (6, 12), (6, 13)]
        tree = {}
        for n1, n2 in edges:
            make_link(tree, n1, n2)
        return tree

    def test1(self):
        tree = self.make_graph()
        labels = create_labels(tree, 1)
        distances = get_distances(tree, labels)
        self.assertEqual(distances[1][9], 3)

    def test2(self):
        tree = self.make_graph()
        labels = create_labels(tree, 1)
        distances = get_distances(tree, labels)
        self.assertEqual(distances[3][9], 4)

    def test3(self):
        tree = self.make_graph()
        labels = create_labels(tree, 1)
        distances = get_distances(tree, labels)
        self.assertEqual(distances[8][13], 6)

    def test4(self):
        tree = {1: {}}
        labels = create_labels(tree, 1)
        self.assertDictEqual(labels, {1: {1: 0}})

    def test_3nodes_1to1(self):
        tree = {}
        make_link(tree, 1, 2)
        make_link(tree, 1, 3)
        labels = create_labels(tree, 1)
        distances = get_distances(tree, labels)
        self.assertEqual(distances[1][1], 0)

    def test_3nodes_1to2(self):
        tree = {}
        make_link(tree, 1, 2)
        make_link(tree, 1, 3)
        labels = create_labels(tree, 1)
        distances = get_distances(tree, labels)
        self.assertEqual(distances[1][2], 1)

    def test_3nodes_1to3(self):
        tree = {}
        make_link(tree, 1, 2)
        make_link(tree, 1, 3)
        labels = create_labels(tree, 1)
        distances = get_distances(tree, labels)
        self.assertEqual(distances[1][3], 1)

    def test_3nodes_2to2(self):
        tree = {}
        make_link(tree, 1, 2)
        make_link(tree, 1, 3)
        labels = create_labels(tree, 1)
        distances = get_distances(tree, labels)
        self.assertEqual(distances[2][2], 0)

    def test_3nodes_2to1(self):
        tree = {}
        make_link(tree, 1, 2)
        make_link(tree, 1, 3)
        labels = create_labels(tree, 1)
        distances = get_distances(tree, labels)
        self.assertEqual(distances[2][1], 1)

    def test_3nodes_2to3(self):
        tree = {}
        make_link(tree, 1, 2)
        make_link(tree, 1, 3)
        labels = create_labels(tree, 1)
        distances = get_distances(tree, labels)
        self.assertEqual(distances[2][3], 2)

    def test_3nodes_weighted_1to1(self):
        tree = {}
        make_link(tree, 1, 2, 2)
        make_link(tree, 1, 3, 5)
        labels = create_labels(tree, 1)
        distances = get_distances(tree, labels)
        self.assertEqual(distances[1][1], 0)

    def test_3nodes_weighted_1to2(self):
        tree = {}
        make_link(tree, 1, 2, 2)
        make_link(tree, 1, 3, 5)
        labels = create_labels(tree, 1)
        distances = get_distances(tree, labels)
        self.assertEqual(distances[1][2], 2)

    def test_3nodes_weighted_1to3(self):
        tree = {}
        make_link(tree, 1, 2, 2)
        make_link(tree, 1, 3, 5)
        labels = create_labels(tree, 1)
        distances = get_distances(tree, labels)
        self.assertEqual(distances[1][3], 5)

    def test_3nodes_weighted_2to2(self):
        tree = {}
        make_link(tree, 1, 2, 2)
        make_link(tree, 1, 3, 5)
        labels = create_labels(tree, 1)
        distances = get_distances(tree, labels)
        self.assertEqual(distances[2][2], 0)

    def test_3nodes_weighted_2to1(self):
        tree = {}
        make_link(tree, 1, 2, 2)
        make_link(tree, 1, 3, 5)
        labels = create_labels(tree, 1)
        distances = get_distances(tree, labels)
        self.assertEqual(distances[2][1], 2)

    def test_3nodes_weighted_2to3(self):
        tree = {}
        make_link(tree, 1, 2, 2)
        make_link(tree, 1, 3, 5)
        labels = create_labels(tree, 1)
        distances = get_distances(tree, labels)
        self.assertEqual(distances[2][3], 7)
