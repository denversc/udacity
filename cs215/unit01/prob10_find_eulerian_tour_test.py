import unittest
from cs215.unit01.prob10_find_eulerian_tour_my import find_eulerian_tour

class FindEulerianTourTest(unittest.TestCase):

    def test_EmptyGraph(self):
        self.doTest([])

    def test_GraphHas1NodeAndOneEdgeToItself(self):
        self.doTest([(1, 1)])

    def test_GraphHas2NodesWith2EdgesBetweenEach(self):
        self.doTest([(1, 2), (2, 1)])

    def test_GraphHas3NodesWith2EdgesBetweenEach(self):
        self.doTest([(1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2)])

    def test_GraphHas5NodesWith2EdgesBetweenEach(self):
        self.doTest([(1, 2), (1, 3), (2, 5), (2, 3), (2, 4), (4, 3), (3, 5)])

    def test_TriangeGraph(self):
        self.doTest([(1, 2), (2, 3), (3, 1)])

    def test_RectangleGraph(self):
        self.doTest([(1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (2, 6),
            (3, 6)])

    def test_UdacityTest1(self):
        self.doTest([(1, 2), (2, 3), (3, 1)])

    def test_UdacityTest2(self):
        self.doTest([(0, 1), (1, 5), (1, 7), (4, 5), (4, 8), (1, 6), (3, 7),
            (5, 9), (2, 4), (0, 4), (2, 5), (3, 6), (8, 9)])

    def test_UdacityTest3(self):
        self.doTest([(1, 13), (1, 6), (6, 11), (3, 13), (8, 13), (0, 6),
            (8, 9), (5, 9), (2, 6), (6, 10), (7, 9), (1, 12), (4, 12), (5, 14),
            (0, 1), (2, 3), (4, 11), (6, 9), (7, 14), (10, 13)])

    def test_UdacityTest4(self):
        self.doTest([(8, 16), (8, 18), (16, 17), (18, 19), (3, 17), (13, 17),
            (5, 13), (3, 4), (0, 18), (3, 14), (11, 14), (1, 8), (1, 9),
            (4, 12), (2, 19),(1, 10), (7, 9), (13, 15), (6, 12), (0, 1),
            (2, 11), (3, 18), (5, 6), (7, 15), (8, 13), (10, 17)])

    def doTest(self, edges):
        actual = find_eulerian_tour(edges)
        self.assertEulerianTour(actual, edges)

    def assertEulerianTour(self, path, edges):
        path = list(path)
        edges = list(edges)
        untraversed_edges = list(edges)

        first_node = None
        last_node = None
        for node in path:
            if first_node is None:
                first_node = node
                last_node = node
            else:
                edge1 = (last_node, node)
                edge2 = (node, last_node)
                if edge1 in untraversed_edges:
                    edge = edge1
                elif edge2 in untraversed_edges:
                    edge = edge2
                elif edge1 in edges:
                    self.fail("path {!r} traverses edge {} multiple times "
                        "in graph {!r}".format(path, edge1, edges))
                elif edge2 in edges:
                    self.fail("path {!r} traverses edge {} multiple times "
                        "in graph {!r}".format(path, edge2, edges))
                else:
                    self.fail("path {!r} traverses non-existent edge {} "
                        "in graph {!r}".format(path, edge1, edges))

                untraversed_edges.remove(edge)
                last_node = node

        num_untraversed_edges = len(untraversed_edges)
        self.assertEquals(num_untraversed_edges, 0,
            "path {!r} does not traverse the following {} edges: {!r}"
            .format(path, num_untraversed_edges, untraversed_edges))
        self.assertEquals(first_node, last_node, "path {!r} begins at node "
            "{!r} and ends at node {!r}, but a tour must begin and end with "
            "the same node".format(path, first_node, last_node))

class Test_assertEulerianTour(unittest.TestCase):

    def setUp(self):
        self.x = FindEulerianTourTest("doTest")

    def test_EmptyGraph_EmptyEdges_Pass(self):
        self.x.assertEulerianTour([], [])

    def test_NonEmptyGraph_EmptyEdges_Fail(self):
        with self.assertRaises(AssertionError) as cm:
            self.x.assertEulerianTour([], [(0, 1)])
        self.assertEquals("{}".format(cm.exception),
            "path [] does not traverse the following 1 edges: [(0, 1)]")

    def test_EmptyGraph_NonEmptyEdges_Fail(self):
        with self.assertRaises(AssertionError) as cm:
            self.x.assertEulerianTour([0, 1], [])
        self.assertEquals("{}".format(cm.exception),
            "path [0, 1] traverses non-existent edge (0, 1) in graph []")

    def test_EdgeVisitedTwoTimes_Fail(self):
        with self.assertRaises(AssertionError) as cm:
            self.x.assertEulerianTour([0, 1, 1, 0, 1], [(0, 1), (1, 1), (0, 1)])
        self.assertEquals("{}".format(cm.exception),
            "path [0, 1, 1, 0, 1] traverses edge (0, 1) multiple times "
            "in graph [(0, 1), (1, 1), (0, 1)]")

    def test_EdgeVisitedTwoTimesOppositeDirection_Fail(self):
        with self.assertRaises(AssertionError) as cm:
            self.x.assertEulerianTour([0, 1, 1, 0, 1], [(1, 0), (1, 1), (1, 0)])
        self.assertEquals("{}".format(cm.exception),
            "path [0, 1, 1, 0, 1] traverses edge (1, 0) multiple times "
            "in graph [(1, 0), (1, 1), (1, 0)]")

    def test_1NodeGraph_EulerianTourGiven_Pass(self):
        self.x.assertEulerianTour([1, 1], [(1, 1)])

    def test_2NodeGraph_EulerianTourGiven_Pass(self):
        self.x.assertEulerianTour([1, 2, 1], [(1, 2), (2, 1)])

    def test_3NodeGraph_EulerianTourGiven_Pass(self):
        self.x.assertEulerianTour([1, 2, 3, 1], [(1, 2), (2, 3), (3, 1)])

    def test_3NodeGraph_NonEulerianTourGiven_Fail(self):
        path = [1, 2, 3, 1]
        graph = [(1, 2), (2, 1), (2, 3), (3, 1)]
        with self.assertRaises(AssertionError) as cm:
            self.x.assertEulerianTour(path, graph)
        self.assertEquals("{}".format(cm.exception),
            "path [1, 2, 3, 1] does not traverse the following 1 edges: [(2, 1)]")

    def test_3NodeGraph_NonEulerianPathDoesNotEndOnStartingNode_Fail(self):
        path = [1, 2, 1, 3, 2]
        graph = [(1, 2), (2, 1), (2, 3), (3, 1)]
        with self.assertRaises(AssertionError) as cm:
            self.x.assertEulerianTour(path, graph)
        self.assertEquals("{}".format(cm.exception),
            "path [1, 2, 1, 3, 2] begins at node 1 and ends at node 2, "
            "but a tour must begin and end with the same node")
