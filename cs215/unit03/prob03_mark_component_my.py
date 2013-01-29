# Rewrite `mark_component` to not use recursion
# and instead use the `open_list` data structure
# discussed in lecture
#

def mark_component(G, node, marked):
    total_marked = 0
    nodes_to_visit = [node]

    while len(nodes_to_visit) > 0:
        node = nodes_to_visit[0]
        del nodes_to_visit[0]

        if node not in marked:
            marked[node] = True
            total_marked += 1
            for adjacent_node in G[node]:
                if adjacent_node not in marked:
                    nodes_to_visit.append(adjacent_node)

    return total_marked

#########
# Code for testing
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

class Test_mark_component_InstructorProvidedTestCases(unittest.TestCase):

    def setUp(self):
        test_edges = [(1, 2), (2, 3), (4, 5), (5, 6)]
        G = {}
        for n1, n2 in test_edges:
            make_link(G, n1, n2)
        self.marked = {}
        self.mark_component_retval = mark_component(G, 1, self.marked)

    def test_retval(self):
        self.assertEquals(self.mark_component_retval, 3)

    def test_1_in_marked(self):
        self.assertIn(1, self.marked)

    def test_2_in_marked(self):
        self.assertIn(2, self.marked)

    def test_3_in_marked(self):
        self.assertIn(3, self.marked)

    def test_4_not_in_marked(self):
        self.assertNotIn(4, self.marked)

    def test_5_not_in_marked(self):
        self.assertNotIn(5, self.marked)

    def test_6_not_in_marked(self):
        self.assertNotIn(6, self.marked)

class Test_mark_component_DenversTests(unittest.TestCase):

    def test_GraphWith1NodeThatHasALinkToItself_retval(self):
        retval = self.invoke_mark_component([(1, 1)], 1)
        self.assertEquals(retval, 1)

    def test_GraphWith1NodeThatHasALinkToItself_marked(self):
        marked = {}
        self.invoke_mark_component([(1, 1)], 1, marked)
        self.assertEquals(marked, {1:True})

    def test_TwoConnectedComponents_Component1_retval(self):
        retval = self.invoke_mark_component([(1, 2), (1, 3), (4, 5)], 1)
        self.assertEquals(retval, 3)

    def test_TwoConnectedComponents_Component1_marked(self):
        marked = {}
        self.invoke_mark_component([(1, 2), (1, 3), (4, 5)], 1, marked)
        self.assertEquals(marked, {1:True, 2:True, 3:True})

    def test_TwoConnectedComponents_Component2_retval(self):
        retval = self.invoke_mark_component([(1, 2), (1, 3), (4, 5)], 4)
        self.assertEquals(retval, 2)

    def test_TwoConnectedComponents_Component2_marked(self):
        marked = {}
        self.invoke_mark_component([(1, 2), (1, 3), (4, 5)], 4, marked)
        self.assertEquals(marked, {4:True, 5:True})

    def invoke_mark_component(self, edges, starting_node, marked=None):
        G = {}
        for n1, n2 in edges:
            make_link(G, n1, n2)
        if marked is None:
            marked = {}
        mark_component_retval = mark_component(G, starting_node, marked)
        return (mark_component_retval)

if __name__ == "__main__":
    unittest.main(verbosity=2)
