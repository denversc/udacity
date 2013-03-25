#
# Take a weighted graph representing a social network where the weight
# between two nodes is the "love" between them.  In this "feel the
# love of a path" problem, we want to find the best path from node `i`
# and node `j` where the score for a path is the maximum love of an
# edge on this path. If there is no path from `i` to `j` return
# `None`.  The returned path doesn't need to be simple, ie it can
# contain cycles or repeated vertices.
#
# Devise and implement an algorithm for this problem.
#

def get_reachable_nodes(G, i):
    unvisited_nodes = [i]
    visited_nodes = set([i])
    while unvisited_nodes:
        node = unvisited_nodes[0]
        del unvisited_nodes[0]
        for adjacent_node in G[node]:
            if adjacent_node not in visited_nodes:
                visited_nodes.add(adjacent_node)
                unvisited_nodes.append(adjacent_node)
    return visited_nodes

def get_max_path_weight(G, nodes):
    max_edge_weight = None
    for node in nodes:
        for weight in G[node].values():
            if weight > max_edge_weight or max_edge_weight is None:
                max_edge_weight = weight
    return max_edge_weight

def feel_the_love(G, i, j):
    # return a path (a list of nodes) between `i` and `j`,
    # with `i` as the first node and `j` as the last node,
    # or None if no path exists

    reachable_nodes = get_reachable_nodes(G, i)
    if j not in reachable_nodes:
        return None

    max_edge_weight = get_max_path_weight(G, reachable_nodes)
    if max_edge_weight is None:
        return None

    unvisited = [([i], None)]
    while True:
        (path, path_weight) = unvisited[0]
        del unvisited[0]
        node = path[-1]

        for adjacent_node in G[node]:
            new_path = path + [adjacent_node]

            new_edge_weight = G[node][adjacent_node]
            if path_weight is None:
                new_path_weight = new_edge_weight
            elif new_edge_weight > path_weight:
                new_path_weight = new_edge_weight
            else:
                new_path_weight = path_weight

            if new_path_weight == max_edge_weight and new_path[-1] == j:
                return new_path

            unvisited.append((new_path, new_path_weight))

import unittest

def score_of_path(G, path):
    max_love = -float('inf')
    for n1, n2 in zip(path[:-1], path[1:]):
        love = G[n1][n2]
        if love > max_love:
            max_love = love
    return max_love

class ProvidedTests(unittest.TestCase):

    def test1(self):
        G = {'a':{'c':1},
             'b':{'c':1},
             'c':{'a':1, 'b':1, 'e':1, 'd':1},
             'e':{'c':1, 'd':2},
             'd':{'e':2, 'c':1},
             'f':{}}
        path = feel_the_love(G, 'a', 'b')
        self.assertEquals(score_of_path(G, path), 2)

    def test2(self):
        G = {'a':{'c':1},
             'b':{'c':1},
             'c':{'a':1, 'b':1, 'e':1, 'd':1},
             'e':{'c':1, 'd':2},
             'd':{'e':2, 'c':1},
             'f':{}}
        path = feel_the_love(G, 'a', 'f')
        self.assertIsNone(path)

class DenverTests(unittest.TestCase):

    def test_1Node0Edges(self):
        G = {1: {}}
        x = feel_the_love(G, 1, 1)
        self.assertIsNone(x)

    def test_1Node1Edge(self):
        G = {1: {1: 1}}
        x = feel_the_love(G, 1, 1)
        self.assertListEqual(x, [1, 1])

    def test_2Nodes0Edges(self):
        G = {1:{}, 2:{}}
        x = feel_the_love(G, 1, 2)
        self.assertIsNone(x)

    def test_2Nodes1Edge(self):
        G = {1:{2:1}, 2:{1:1}}
        x = feel_the_love(G, 1, 2)
        self.assertListEqual(x, [1, 2])

    def test_3NodesChain_DirectLinkMostLove(self):
        G = {
            1: {2:5},
            2: {1:5, 3:1},
            3: {2:1},
        }
        x = feel_the_love(G, 1, 2)
        self.assertListEqual(x, [1, 2])

    def test_3NodesChain_IndirectLinkMostLove(self):
        G = {
            1: {2:5},
            2: {1:5, 3:10},
            3: {2:10},
        }
        x = feel_the_love(G, 1, 2)
        self.assertListEqual(x, [1, 2, 3, 2])

    def test_5NodeRing1(self):
        G = {
            1: {2:6, 5:1},
            2: {3:1, 1:6},
            3: {4:1, 2:1},
            4: {5:1, 3:1},
            5: {1:1, 4:1},
        }
        x = feel_the_love(G, 1, 4)
        self.assertListEqual(x, [1, 2, 3, 4])

    def test_5NodeRing2(self):
        G = {
            1: {2:1, 5:6},
            2: {3:1, 1:1},
            3: {4:1, 2:1},
            4: {5:1, 3:1},
            5: {1:6, 4:1},
        }
        x = feel_the_love(G, 1, 4)
        self.assertListEqual(x, [1, 5, 4])

    def test_Star1(self):
        G = {
            1: {2:1, 3:1, 4:1, 5:1},
            2: {1:1},
            3: {1:1},
            4: {1:1},
            5: {1:1},
        }
        x = feel_the_love(G, 1, 4)
        self.assertListEqual(x, [1, 4])

    def test_Star2(self):
        G = {
            1: {2:1, 3:1, 4:10, 5:1},
            2: {1:1},
            3: {1:1},
            4: {1:10},
            5: {1:1},
        }
        x = feel_the_love(G, 1, 2)
        self.assertListEqual(x, [1, 4, 1, 2])

    def test_2Stars_NodesInSameConnectedComponent(self):
        G = {
            1: {2:1, 3:1, 4:10, 5:1},
            2: {1:1},
            3: {1:1},
            4: {1:10},
            5: {1:1},
            10: {20:1, 30:1, 40:10, 50:1},
            20: {10:1},
            30: {10:1},
            40: {10:10},
            50: {10:1},
        }
        x = feel_the_love(G, 1, 2)
        self.assertListEqual(x, [1, 4, 1, 2])

    def test_2Stars_NodesInDifferentConnectedComponents(self):
        G = {
            1: {2:1, 3:1, 4:10, 5:1},
            2: {1:1},
            3: {1:1},
            4: {1:10},
            5: {1:1},
            10: {20:1, 30:1, 40:10, 50:1},
            20: {10:1},
            30: {10:1},
            40: {10:10},
            50: {10:1},
        }
        x = feel_the_love(G, 1, 10)
        self.assertIsNone(x)

    def test_2StarsConnectedByBridge(self):
        G = {
            1: {2:1, 3:1, 4:10, 5:1},
            2: {1:1},
            3: {1:1},
            4: {1:10},
            5: {1:1, 50:20},
            10: {20:1, 30:1, 40:10, 50:1},
            20: {10:1},
            30: {10:1},
            40: {10:10},
            50: {10:1, 5:20},
        }
        x = feel_the_love(G, 2, 3)
        self.assertListEqual(x, [2, 1, 5, 50, 5, 1, 3])
