# Finding a Favor v2
#
# Each edge (u,v) in a social network has a weight p(u,v) that
# represents the probability that u would do a favor for v if asked.
# Note that p(v,u) != p(u,v), in general.
#
# Write a function that finds the right sequence of friends to maximize
# the probability that v1 will do a favor for v2.
#

#
# Provided are two standard versions of dijkstra's algorithm that were
# discussed in class. One uses a list and another uses a heap.
#
# You should manipulate the input graph, G, so that it works using
# the given implementations.  Based on G, you should decide which
# version (heap or list) you should use.
#

# code for heap can be found in the instructors comments below
from cs215.finalexam.heap import heappopmin
from cs215.finalexam.heap import insert_heap
from cs215.finalexam.heap import decrease_val
from operator import itemgetter

import math

def maximize_probability_of_favor(G, v1, v2):
    H = {x:{} for x in G}
    for node1 in G:
        for node2 in G[node1]:
            p_node1_node2 = G[node1][node2]
            p_node1_node2_log = math.log(p_node1_node2, 2)
            p_node1_node2_log_positive = -p_node1_node2_log
            H[node1][node2] = p_node1_node2_log_positive

    results = dijkstra_heap(H, v1)
    result = results[v2]

    p_v1_v2_log_positive = result[0]
    p_v1_v2_log = -p_v1_v2_log_positive
    p_v1_v2 = 2 ** p_v1_v2_log

    path = [v2]
    node = v2
    while node != v1:
        node = results[node][1]
        path.append(node)
    path.reverse()

    return (path, p_v1_v2)

#
# version of dijkstra implemented using a heap
#
# returns a dictionary mapping a node to the distance
# to that node and the parent
#
# Do not modify this code
#
def dijkstra_heap(G, a):
    # Distance to the input node is zero, and it has
    # no parent
    first_entry = (0, a, None)
    heap = [first_entry]
    # location keeps track of items in the heap
    # so that we can update their value later
    location = {first_entry:0}
    dist_so_far = {a:first_entry}
    final_dist = {}
    while len(dist_so_far) > 0:
        dist, node, parent = heappopmin(heap, location)
        # lock it down!
        final_dist[node] = (dist, parent)
        del dist_so_far[node]
        for x in G[node]:
            if x in final_dist:
                continue
            new_dist = G[node][x] + final_dist[node][0]
            new_entry = (new_dist, x, node)
            if x not in dist_so_far:
                # add to the heap
                insert_heap(heap, new_entry, location)
                dist_so_far[x] = new_entry
            elif new_entry < dist_so_far[x]:
                # update heap
                decrease_val(heap, location, dist_so_far[x], new_entry)
                dist_so_far[x] = new_entry
    return final_dist

#
# version of dijkstra implemented using a list
#
# returns a dictionary mapping a node to the distance
# to that node and the parent
#
# Do not modify this code
#
def dijkstra_list(G, a):
    dist_so_far = {a:(0, None)} # keep track of the parent node
    final_dist = {}
    while len(final_dist) < len(G):
        node, entry = min(dist_so_far.items(), key=itemgetter(1))
        # lock it down!
        final_dist[node] = entry
        del dist_so_far[node]
        for x in G[node]:
            if x in final_dist:
                continue
            new_dist = G[node][x] + final_dist[node][0]
            new_entry = (new_dist, node)
            if x not in dist_so_far:
                dist_so_far[x] = new_entry
            elif new_entry < dist_so_far[x]:
                dist_so_far[x] = new_entry
    return final_dist

##########
#
# Test

import unittest

class ProvidedTests(unittest.TestCase):

    def get_result(self):
        G = {'a':{'b':.9, 'e':.5},
             'b':{'c':.9},
             'c':{'d':.01},
             'd':{},
             'e':{'f':.5},
             'f':{'d':.5}}
        (path, prob) = maximize_probability_of_favor(G, 'a', 'd')
        return (path, prob)

    def test1(self):
        (path, unused_prob) = self.get_result()
        self.assertListEqual(path, ['a', 'e', 'f', 'd'])

    def test2(self):
        (unused_path, prob) = self.get_result()
        self.assertAlmostEqual(prob, .5 * .5 * .5, places=3)

class FindingAFavorTestCase(unittest.TestCase):

    def assert_path(self, v1, v2, expected_path):
        (actual_path, unused_prob) = self.calculate_result(v1, v2)
        self.assertListEqual(actual_path, expected_path)

    def assert_probability(self, v1, v2, expected_prob, places=3):
        (unused_path, actual_prob) = self.calculate_result(v1, v2)
        self.assertAlmostEqual(actual_prob, expected_prob, places)

    def calculate_result(self, v1, v2):
        G = self.create_graph()
        result = maximize_probability_of_favor(G, v1, v2)
        return result

class Test2Nodes(FindingAFavorTestCase):

    def create_graph(self):
        return {
            "A": {"B": 0.25},
            "B": {"A": 0.80},
        }

    def test_AtoB_path(self):
        self.assert_path("A", "B", ["A", "B"])

    def test_AtoB_prob(self):
        self.assert_probability("A", "B", 0.25)

    def test_BtoA_path(self):
        self.assert_path("B", "A", ["B", "A"])

    def test_BtoA_prob(self):
        self.assert_probability("B", "A", 0.80)

class Test3NodeClique(FindingAFavorTestCase):

    def create_graph(self):
        return {
            "A": {"B": 0.1, "C": 0.2},
            "B": {"C": 0.3, "A": 0.9},
            "C": {"A": 0.8, "B": 0.7},
        }

    def test_AtoB_path(self):
        self.assert_path("A", "B", ["A", "C", "B"])

    def test_AtoB_prob(self):
        self.assert_probability("A", "B", 0.14)

    def test_AtoC_path(self):
        self.assert_path("A", "C", ["A", "C"])

    def test_AtoC_prob(self):
        self.assert_probability("A", "C", 0.2)

    def test_BtoA_path(self):
        self.assert_path("B", "A", ["B", "A"])

    def test_BtoA_prob(self):
        self.assert_probability("B", "A", 0.9)

    def test_BtoC_path(self):
        self.assert_path("B", "C", ["B", "C"])

    def test_BtoC_prob(self):
        self.assert_probability("B", "C", 0.3)

    def test_CtoA_path(self):
        self.assert_path("C", "A", ["C", "A"])

    def test_CtoA_prob(self):
        self.assert_probability("C", "A", 0.8)

    def test_CtoB_path(self):
        self.assert_path("C", "B", ["C", "B"])

    def test_CtoB_prob(self):
        self.assert_probability("C", "B", 0.7)

class Test4NodeClique(FindingAFavorTestCase):

    def create_graph(self):
        return {
            "A": {"B": 0.1, "C": 0.9, "D": 0.6},
            "B": {"A": 0.2, "C": 0.7, "D": 0.1},
            "C": {"A": 0.2, "B": 0.2, "D": 0.1},
            "D": {"A": 0.7, "B": 0.7, "C": 0.9},
        }

    def test_AtoB_path(self):
        self.assert_path("A", "B", ["A", "D", "B"])

    def test_AtoB_prob(self):
        self.assert_probability("A", "B", 0.42)

    def test_AtoC_path(self):
        self.assert_path("A", "C", ["A", "C"])

    def test_AtoC_prob(self):
        self.assert_probability("A", "C", 0.9)

    def test_AtoD_path(self):
        self.assert_path("A", "D", ["A", "D"])

    def test_AtoD_prob(self):
        self.assert_probability("A", "D", 0.6)

    def test_BtoA_path(self):
        self.assert_path("B", "A", ["B", "A"])

    def test_BtoA_prob(self):
        self.assert_probability("B", "A", 0.2)

    def test_BtoC_path(self):
        self.assert_path("B", "C", ["B", "C"])

    def test_BtoC_prob(self):
        self.assert_probability("B", "C", 0.7)

    def test_BtoD_path(self):
        self.assert_path("B", "D", ["B", "A", "D"])

    def test_BtoD_prob(self):
        self.assert_probability("B", "D", 0.12)

    def test_CtoA_path(self):
        self.assert_path("C", "A", ["C", "A"])

    def test_CtoA_prob(self):
        self.assert_probability("C", "A", 0.2)

    def test_CtoB_path(self):
        self.assert_path("C", "B", ["C", "B"])

    def test_CtoB_prob(self):
        self.assert_probability("C", "B", 0.2)

    def test_CtoD_path(self):
        self.assert_path("C", "D", ["C", "A", "D"])

    def test_CtoD_prob(self):
        self.assert_probability("C", "D", 0.12)

    def test_DtoA_path(self):
        self.assert_path("D", "A", ["D", "A"])

    def test_DtoA_prob(self):
        self.assert_probability("D", "A", 0.7)

    def test_DtoB_path(self):
        self.assert_path("D", "B", ["D", "B"])

    def test_DtoB_prob(self):
        self.assert_probability("D", "B", 0.7)

    def test_DtoC_path(self):
        self.assert_path("D", "C", ["D", "C"])

    def test_DtoC_prob(self):
        self.assert_probability("D", "C", 0.9)

class TestBigDipper(FindingAFavorTestCase):

    def create_graph(self):
        return {
            "A": {"B": 0.1},
            "B": {"C": 0.7},
            "C": {"D": 0.2, "E": 0.4},
            "D": {"F": 0.7},
            "E": {"F": 0.1},
            "F": {},
        }

    def test_AtoF_path(self):
        self.assert_path("A", "F", ["A", "B", "C", "D", "F"])

    def test_AtoF_prob(self):
        self.assert_probability("A", "F", 0.0098, 4)
