# Decision problems are often just as hard as as actually returning an answer.
# Show how a k-clique can be found using a solution to the k-clique decision
# problem.  Write a Python function that takes a graph G and a number k
# as input, and returns a list of k nodes from G that are all connected
# in the graph.  Your function should make use of "k_clique_decision(G, k)",
# which takes a graph G and a number k and answers whether G contains a k-clique.
# We will also provide the standard routines for adding and removing edges from a graph.

# Returns a list of all the subsets of a list of size k
def k_subsets(lst, k):
    if len(lst) < k:
        return []
    if len(lst) == k:
        return [lst]
    if k == 1:
        return [[i] for i in lst]
    return k_subsets(lst[1:], k) + map(lambda x: x + [lst[0]], k_subsets(lst[1:], k - 1))

# Checks if the given list of nodes forms a clique in the given graph.
def is_clique(G, nodes):
    for pair in k_subsets(nodes, 2):
        if pair[1] not in G[pair[0]]:
            return False
    return True

# Determines if there is clique of size k or greater in the given graph.
def k_clique_decision(G, k):
    nodes = G.keys()
    for i in range(k, len(nodes) + 1):
        for subset in k_subsets(nodes, i):
            if is_clique(G, subset):
                return True
    return False

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G

def break_link(G, node1, node2):
    if node1 not in G:
        print "error: breaking link in a non-existent node"
        return
    if node2 not in G:
        print "error: breaking link in a non-existent node"
        return
    if node2 not in G[node1]:
        print "error: breaking non-existent link"
        return
    if node1 not in G[node2]:
        print "error: breaking non-existent link"
        return
    del G[node1][node2]
    del G[node2][node1]
    return G

def k_clique(G, k):
    if not k_clique_decision(G, k):
        return False

    for node in tuple(G):
        adjacent_nodes = []
        for adjacent_node in tuple(G[node]):
            break_link(G, node, adjacent_node)
            adjacent_nodes.append(adjacent_node)
        del G[node]
        if not k_clique_decision(G, k):
            G[node] = {}
            for adjacent_node in adjacent_nodes:
                make_link(G, node, adjacent_node)

    k_clique_nodes = [x for x in G]
    return k_clique_nodes

import unittest

class DenverTests(unittest.TestCase):

    def test_1NodeGraph_k1(self):
        G = {1: {}}
        actual = k_clique(G, 1)
        self.assertSameNodeSet(actual, [1])

    def test_1NodeGraph_k2(self):
        G = {1: {}}
        actual = k_clique(G, 2)
        self.assertIs(actual, False)

    def test_2NodeConnectedGraph_k1(self):
        G = {}
        make_link(G, 1, 2)
        actual = k_clique(G, 1)
        self.assertSameNodeSet(actual, [1], [2])

    def test_2NodeConnectedGraph_k2(self):
        G = {}
        make_link(G, 1, 2)
        actual = k_clique(G, 2)
        self.assertSameNodeSet(actual, [1, 2])

    def test_2NodeConnectedGraph_k3(self):
        G = {}
        make_link(G, 1, 2)
        actual = k_clique(G, 3)
        self.assertIs(actual, False)

    def test_2NodeDisconnectedGraph_k1(self):
        G = {1:{}, 2:{}}
        actual = k_clique(G, 1)
        self.assertSameNodeSet(actual, [1], [2])

    def test_2NodeDisconnectedGraph_k2(self):
        G = {1:{}, 2:{}}
        actual = k_clique(G, 2)
        self.assertIs(actual, False)

    def test_3NodeConnectedGraph_k1(self):
        G = {}
        make_link(G, 1, 2)
        make_link(G, 2, 3)
        make_link(G, 3, 1)
        actual = k_clique(G, 1)
        self.assertSameNodeSet(actual, [1], [2], [3])

    def test_3NodeConnectedGraph_k2(self):
        G = {}
        make_link(G, 1, 2)
        make_link(G, 2, 3)
        make_link(G, 3, 1)
        actual = k_clique(G, 2)
        self.assertSameNodeSet(actual, [1, 2], [2, 3], [1, 3])

    def test_3NodeConnectedGraph_k3(self):
        G = {}
        make_link(G, 1, 2)
        make_link(G, 2, 3)
        make_link(G, 3, 1)
        actual = k_clique(G, 3)
        self.assertSameNodeSet(actual, [1, 2, 3])

    def test_3NodeConnectedGraph_k4(self):
        G = {}
        make_link(G, 1, 2)
        make_link(G, 2, 3)
        make_link(G, 3, 1)
        actual = k_clique(G, 4)
        self.assertIs(actual, False)

    def test_3NodeChain_k1(self):
        G = {}
        make_link(G, 1, 2)
        make_link(G, 2, 3)
        actual = k_clique(G, 1)
        self.assertSameNodeSet(actual, [1], [2], [3])

    def test_3NodeChain_k2(self):
        G = {}
        make_link(G, 1, 2)
        make_link(G, 2, 3)
        actual = k_clique(G, 2)
        self.assertSameNodeSet(actual, [1, 2], [2, 3])

    def test_3NodeChain_k3(self):
        G = {}
        make_link(G, 1, 2)
        make_link(G, 2, 3)
        actual = k_clique(G, 3)
        self.assertIs(actual, False)

    def test_3CliqueWithOffshoots_k3(self):
        G = {}
        make_link(G, 1, 2)
        make_link(G, 2, 3)
        make_link(G, 1, 3)
        make_link(G, 1, 4)
        make_link(G, 1, 5)
        make_link(G, 2, 6)
        make_link(G, 2, 7)
        make_link(G, 3, 8)
        make_link(G, 3, 9)
        actual = k_clique(G, 3)
        self.assertSameNodeSet(actual, [1, 2, 3])

    def test_Two3CliquesWithOffshoots_k3(self):
        G = {}
        make_link(G, 1, 2)
        make_link(G, 2, 3)
        make_link(G, 1, 3)
        make_link(G, 1, 4)
        make_link(G, 1, 5)
        make_link(G, 2, 6)
        make_link(G, 2, 7)
        make_link(G, 3, 8)
        make_link(G, 3, 9)
        make_link(G, 7, 9)
        make_link(G, 8, 9)
        make_link(G, 7, 8)
        actual = k_clique(G, 3)
        self.assertSameNodeSet(actual, [1, 2, 3], [7, 8, 9])

    def test_3CliquesWith4CliqueOffshoots_k4(self):
        G = {}
        make_link(G, 1, 2)
        make_link(G, 2, 3)
        make_link(G, 1, 3)
        make_link(G, 1, 4)
        make_link(G, 1, 5)
        make_link(G, 2, 6)
        make_link(G, 2, 7)
        make_link(G, 3, 8)
        make_link(G, 3, 9)
        make_link(G, 6, 9)
        make_link(G, 7, 9)
        make_link(G, 8, 9)
        make_link(G, 6, 8)
        make_link(G, 7, 8)
        make_link(G, 6, 7)
        actual = k_clique(G, 4)
        self.assertSameNodeSet(actual, [6, 7, 8, 9])

    def assertSameNodeSet(self, actual, expected, *expecteds):
        actual_set = frozenset(actual)
        assert len(actual_set) == len(actual)

        expecteds = (expected,) + expecteds
        expected_sets = []
        for expected in expecteds:
            expected_set = frozenset(expected)
            assert len(expected_set) == len(expected)
            expected_sets.append(expected_set)

        for expected_set in expected_sets:
            if actual_set == expected_set:
                break
        else:
            self.fail("unexpected list of nodes given: {} (expected one of {})"
                .format(actual, ", ".join("{}".format(x) for x in expecteds)))

