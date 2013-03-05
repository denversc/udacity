# In the lecture, we described how a solution to k_clique_decision(G, k)
# can be used to solve independent_set_decision(H,s).
# Write a Python function that carries out this transformation.

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

# This function should use the k_clique_decision function
# to solve the independent set decision problem
def independent_set_decision(H, s):
    # Create a new graph G which is the complement of H; that is, if two nodes
    # are connected in H then they are not connected in G and if two nodes are
    # not connected in H then they are connected in G
    G = {x:{} for x in H}
    for node1 in H:
        node1_neighbours = frozenset(H[node1])
        for node2 in H:
            if node1 == node2 or node2 not in node1_neighbours:
                make_link(G, node1, node2)

    # now use k_clique_decision on the complement of H to determine if H
    # contains an independent set
    has_independent_set = k_clique_decision(G, s)
    return has_independent_set

import unittest

class DenverTests(unittest.TestCase):

    def test_GraphA_2Nodes(self):
        G = {}
        make_link(G, 1, 2)
        self.assertEqual(independent_set_decision(G, 1), True)
        self.assertEqual(independent_set_decision(G, 2), False)

    def test_GraphB_Triange(self):
        G = {}
        make_link(G, 1, 2)
        make_link(G, 2, 3)
        make_link(G, 1, 3)
        self.assertEqual(independent_set_decision(G, 1), True)
        self.assertEqual(independent_set_decision(G, 2), False)
        self.assertEqual(independent_set_decision(G, 3), False)

    def test_GraphC_Square(self):
        G = {}
        make_link(G, 1, 2)
        make_link(G, 2, 3)
        make_link(G, 3, 4)
        make_link(G, 4, 1)
        self.assertEqual(independent_set_decision(G, 1), True)
        self.assertEqual(independent_set_decision(G, 2), True)
        self.assertEqual(independent_set_decision(G, 3), False)
        self.assertEqual(independent_set_decision(G, 4), False)

    def test_GraphC_SquareCycle(self):
        G = {}
        make_link(G, 1, 2)
        make_link(G, 2, 3)
        make_link(G, 3, 4)
        make_link(G, 4, 1)
        make_link(G, 1, 3)
        make_link(G, 2, 4)
        self.assertEqual(independent_set_decision(G, 1), True)
        self.assertEqual(independent_set_decision(G, 2), False)
        self.assertEqual(independent_set_decision(G, 3), False)
        self.assertEqual(independent_set_decision(G, 4), False)

    def test_GraphD_Star(self):
        G = {}
        make_link(G, 1, 2)
        make_link(G, 1, 3)
        make_link(G, 1, 4)
        make_link(G, 1, 5)
        make_link(G, 1, 6)
        self.assertEqual(independent_set_decision(G, 1), True)
        self.assertEqual(independent_set_decision(G, 2), True)
        self.assertEqual(independent_set_decision(G, 3), True)
        self.assertEqual(independent_set_decision(G, 4), True)
        self.assertEqual(independent_set_decision(G, 5), True)
        self.assertEqual(independent_set_decision(G, 6), False)

    def test_GraphD_BigDipper(self):
        G = {}
        make_link(G, 1, 2)
        make_link(G, 2, 3)
        make_link(G, 3, 4)
        make_link(G, 4, 5)
        make_link(G, 5, 6)
        make_link(G, 6, 3)
        self.assertEqual(independent_set_decision(G, 1), True)
        self.assertEqual(independent_set_decision(G, 2), True)
        self.assertEqual(independent_set_decision(G, 3), True)
        self.assertEqual(independent_set_decision(G, 4), False)
        self.assertEqual(independent_set_decision(G, 5), False)
        self.assertEqual(independent_set_decision(G, 6), False)
