#
# Write centrality_max to return the maximum distance
# from a node to all the other nodes it can reach
#

def iter_paths(G, start_node, path=None):
    if path is None:
        path = [start_node]
    for adjacent_node in G[start_node]:
        if adjacent_node not in path:
            path.append(adjacent_node)
            yield path
            for sub_path in iter_paths(G, adjacent_node, path):
                yield sub_path
            del path[-1]

def centrality_max(G, start_node):
    max_path_length = 0
    for path in iter_paths(G, start_node):
        path_length = len(path)
        if path_length > max_path_length:
            max_path_length = path_length
    return max_path_length - 1

#################
# Testing code
#
def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G

import unittest

class InstructorTestCase(unittest.TestCase):

    def create_chain(self):
        chain = ((1,2), (2,3), (3,4), (4,5), (5,6))
        G = {}
        for n1, n2 in chain:
            make_link(G, n1, n2)
        return G

    def create_tree(self):
        tree = ((1, 2), (1, 3),
                (2, 4), (2, 5),
                (3, 6), (3, 7),
                (4, 8), (4, 9),
                (6, 10), (6, 11))
        G = {}
        for n1, n2 in tree:
            make_link(G, n1, n2)
        return G

    def test_chain_node1(self):
        G = self.create_chain()
        self.assertEquals(centrality_max(G, 1), 5)

    def test_chain_node_3(self):
        G = self.create_chain()
        self.assertEquals(centrality_max(G, 3), 3)

    def test_tree_node1(self):
        G = self.create_tree()
        self.assertEquals(centrality_max(G, 1), 3)

    def test_tree_node_11(self):
        G = self.create_tree()
        self.assertEquals(centrality_max(G, 11), 6)

class DenverTestCase(unittest.TestCase):

    def setUp(self):
        edges = [
            ('a', 'b'),
            ('b', 'k'),
            ('b', 'c'),
            ('a', 'c'),
            ('a', 'e'),
            ('c', 'd'),
            ('d', 'e'),
            ('c', 'k'),
            ('d', 'h'),
            ('e', 'h'),
            ('k', 'g'),
            ('k', 'h'),
        ]
        G = {}
        for n1, n2 in edges:
            make_link(G, n1, n2)
        self.G = G

    def test_node_a(self):
        self.assertEquals(centrality_max(self.G, 'a'), 7)

    def test_node_b(self):
        self.assertEquals(centrality_max(self.G, 'b'), 7)

    def test_node_c(self):
        self.assertEquals(centrality_max(self.G, 'c'), 7)

    def test_node_d(self):
        self.assertEquals(centrality_max(self.G, 'd'), 7)

    def test_node_e(self):
        self.assertEquals(centrality_max(self.G, 'e'), 7)

    def test_node_g(self):
        self.assertEquals(centrality_max(self.G, 'g'), 7)

    def test_node_h(self):
        self.assertEquals(centrality_max(self.G, 'h'), 7)

    def test_node_k(self):
        self.assertEquals(centrality_max(self.G, 'k'), 6)

