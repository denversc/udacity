#
# Design and implement an algorithm that can preprocess a
# graph and then answer the question "is x connected to y in the
# graph" for any x and y in constant time Theta(1).
#

#
# `process_graph` will be called only once on each graph.  If you want,
# you can store whatever information you need for `is_connected` in
# global variables
#

def process_graph(G):
    global connectedness
    connectedness = {}
    for initial_node in G:
        unvisited = [initial_node]
        visited = set()

        while unvisited:
            node = unvisited[-1]
            del unvisited[-1]
            visited.add(node)

            for node in G[node]:
                if node not in visited and node not in unvisited:
                    unvisited.append(node)

        connectedness[initial_node] = visited

#
# When being graded, `is_connected` will be called
# many times so this routine needs to be quick
#
def is_connected(i, j):
    global connectedness
    return j in connectedness[i]

import unittest

class ProvidedTests(unittest.TestCase):

    G1 = {1:{2:1},
          2:{1:1},
          3:{4:1},
          4:{3:1},
          5:{}}

    G2 = {1:{2:1, 3:1},
          2:{1:1},
          3:{4:1, 1:1},
          4:{3:1},
          5:{}}

    def test_G1_1_and_2(self):
        process_graph(self.G1)
        self.assertTrue(is_connected(1, 2))
        assert is_connected(1, 3) == False

    def test_G1_1_and_3(self):
        process_graph(self.G1)
        self.assertFalse(is_connected(1, 3))

    def test_G2_1_and_2(self):
        process_graph(self.G2)
        self.assertTrue(is_connected(1, 2))

    def test_G2_1_and_3(self):
        process_graph(self.G2)
        self.assertTrue(is_connected(1, 3))

    def test_G2_1_and_5(self):
        process_graph(self.G2)
        self.assertFalse(is_connected(1, 5))
