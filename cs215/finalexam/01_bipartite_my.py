#
# Write a function, `bipartite` that
# takes as input a graph, `G` and tries
# to divide G into two sets where
# there are no edges between elements of the
# the same set - only between elements in
# different sets.
# If two sets exists, return one of them
# or `None` otherwise
# Assume G is connected
#

def bipartite(G):
    # special case: if the graph has less than 2 nodes then it cannot be bipartite
    if len(G) < 2:
        return None

    visited_nodes = set()
    group1 = set()
    group2 = set()

    # select an arbitrary node from G at which to start the search
    for node in G:
        break
    
    # add the arbitrarily-chosen node to the unvisited list and group 1
    unvisited_nodes = [node]
    visited_nodes.add(node)
    group1.add(node)
    
    # perform a breadth-first search through G
    while unvisited_nodes:
        node = unvisited_nodes[0]
        del unvisited_nodes[0]
        
        # determine which group the node belongs to
        if node in group1:
            group = group2
        elif node in group2:
            group = group1
        else:
            raise AssertionError("internal error: node is in neither group")
        
        # add all of its adjacent nodes to the other group and the open list
        for adjacent_node in G[node]:
            if adjacent_node not in visited_nodes:
                unvisited_nodes.append(adjacent_node)
                visited_nodes.add(adjacent_node)
                
                # if the node is connected to any nodes in the other group, then
                # this cannot be a bipartite graph
                for node in group:
                    if adjacent_node in G[node]:
                        return None
                
                group.add(adjacent_node)
    
    return group1

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

    def test1(self):    
        edges = [(1, 2), (2, 3), (1, 4), (2, 5),
                 (3, 8), (5, 6)]
        G = {}
        for n1, n2 in edges:
            make_link(G, n1, n2)
        g1 = bipartite(G)
        assert (g1 == set([1, 3, 5]) or
                g1 == set([2, 4, 6, 8]))
    
    def test2(self):
        edges = [(1, 2), (1, 3), (2, 3)]
        G = {}
        for n1, n2 in edges:
            make_link(G, n1, n2)
        g1 = bipartite(G)
        assert g1 == None
    
class DenverTests(unittest.TestCase):
    
    def test_0NodeGraph(self):
        self.assertIsNone(bipartite({}))

    def test_1NodeGraph(self):
        self.assertIsNone(bipartite({0: {}}))

    def test_2NodeGraph(self):
        G = {}
        make_link(G, 1, 2, 0)
        x = bipartite(G)
        self.assertIn(x, [set([1]), set([2])])

    def test_3NodeBipartiteGraph1(self):
        G = {}
        make_link(G, 1, 2, 0)
        make_link(G, 1, 3, 0)
        x = bipartite(G)
        self.assertIn(x, [set([1]), set([2, 3])])

    def test_3NodeBipartiteGraph2(self):
        G = {}
        make_link(G, 1, 2, 0)
        make_link(G, 2, 3, 0)
        x = bipartite(G)
        self.assertIn(x, [set([2]), set([1, 3])])

    def test_3NodeClique(self):
        G = {}
        make_link(G, 1, 2, 0)
        make_link(G, 2, 3, 0)
        make_link(G, 1, 3, 0)
        self.assertIsNone(bipartite(G))




