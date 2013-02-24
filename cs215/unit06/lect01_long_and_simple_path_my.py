#
# Modify long_and_simple_path
# to build and return the path
#

# Find me that path!
def long_and_simple_path(G, u, v, l):
    """
    G: Graph
    u: starting node
    v: ending node
    l: minimum length of path
    """
    if not long_and_simple_decision(G, u, v, l):
        return False
    # Otherwise, build and return the path
    if l <= 2:
        return [u, v]

    for adjacent_node in G[v]:
        sub_path = long_and_simple_path(G, u, adjacent_node, l - 1)
        if sub_path:
            return sub_path + [v]

    return False

#############

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

flights = [(1, 2), (1, 3), (2, 3), (2, 6), (2, 4), (2, 5), (3, 6), (4, 5)]
G = {}
for (x, y) in flights: make_link(G, x, y)

def all_perms(seq):
    if len(seq) == 0: return [[]]
    if len(seq) == 1: return [seq, []]
    most = all_perms(seq[1:])
    first = seq[0]
    rest = []
    for perm in most:
        for i in range(len(perm) + 1):
            rest.append(perm[0:i] + [first] + perm[i:])
    return most + rest

def check_path(G, path):
    for i in range(len(path) - 1):
        if path[i + 1] not in G[path[i]]: return False
    return True

def long_and_simple_decision(G, u, v, l):
    if l == 0:
        return False
    n = len(G)
    perms = all_perms(G.keys())
    for perm in perms:
        # check path
        if (len(perm) >= l and check_path(G, perm) and perm[0] == u
            and perm[len(perm) - 1] == v):
            return True
    return False

import unittest

class DenverTests(unittest.TestCase):

    def test_GraphA_01(self):
        G = {}
        make_link(G, "a", "b")
        self.assertEqual(long_and_simple_path(G, "a", "b", 1), ["a", "b"])

    def test_GraphA_02(self):
        G = {}
        make_link(G, "a", "b")
        self.assertEqual(long_and_simple_path(G, "a", "b", 2), ["a", "b"])

    def test_GraphA_03(self):
        G = {}
        make_link(G, "a", "b")
        self.assertEqual(long_and_simple_path(G, "a", "b", 3), False)

    def test_GraphB_01(self):
        G = {}
        make_link(G, "a", "b")
        make_link(G, "b", "c")
        self.assertEqual(long_and_simple_path(G, "a", "b", 1), ["a", "b"])

    def test_GraphB_02(self):
        G = {}
        make_link(G, "a", "b")
        make_link(G, "b", "c")
        self.assertEqual(long_and_simple_path(G, "a", "b", 2), ["a", "b"])

    def test_GraphB_03(self):
        G = {}
        make_link(G, "a", "b")
        make_link(G, "b", "c")
        self.assertEqual(long_and_simple_path(G, "a", "b", 3), False)

    def test_GraphB_04(self):
        G = {}
        make_link(G, "a", "b")
        make_link(G, "b", "c")
        self.assertEqual(long_and_simple_path(G, "a", "c", 1), ["a", "b", "c"])

    def test_GraphB_05(self):
        G = {}
        make_link(G, "a", "b")
        make_link(G, "b", "c")
        self.assertEqual(long_and_simple_path(G, "a", "c", 2), ["a", "b", "c"])

    def test_GraphB_06(self):
        G = {}
        make_link(G, "a", "b")
        make_link(G, "b", "c")
        self.assertEqual(long_and_simple_path(G, "a", "c", 3), ["a", "b", "c"])

    def test_GraphB_07(self):
        G = {}
        make_link(G, "a", "b")
        make_link(G, "b", "c")
        self.assertEqual(long_and_simple_path(G, "a", "c", 4), False)




