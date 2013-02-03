# Bridge Edges v4
#
# Find the bridge edges in a graph given the
# algorithm in lecture.
# Complete the intermediate steps
#  - create_rooted_spanning_tree
#  - post_order
#  - number_of_descendants
#  - lowest_post_order
#  - highest_post_order
#
# And then combine them together in
# `bridge_edges`

# So far, we've represented graphs
# as a dictionary where G[n1][n2] == 1
# meant there was an edge between n1 and n2
#
# In order to represent a spanning tree
# we need to create two classes of edges
# we'll refer to them as "green" and "red"
# for the green and red edges as specified in lecture
#
# So, for example, the graph given in lecture
# G = {'a': {'c': 1, 'b': 1},
#      'b': {'a': 1, 'd': 1},
#      'c': {'a': 1, 'd': 1},
#      'd': {'c': 1, 'b': 1, 'e': 1},
#      'e': {'d': 1, 'g': 1, 'f': 1},
#      'f': {'e': 1, 'g': 1},
#      'g': {'e': 1, 'f': 1}
#      }
# would be written as a spanning tree
# S = {'a': {'c': 'green', 'b': 'green'},
#      'b': {'a': 'green', 'd': 'red'},
#      'c': {'a': 'green', 'd': 'green'},
#      'd': {'c': 'green', 'b': 'red', 'e': 'green'},
#      'e': {'d': 'green', 'g': 'green', 'f': 'green'},
#      'f': {'e': 'green', 'g': 'red'},
#      'g': {'e': 'green', 'f': 'red'}
#      }
#
def create_rooted_spanning_tree(G, root):
    S = {}
    nodes_to_visit = [root]
    visited = set()

    while nodes_to_visit:
        node = nodes_to_visit[0]
        del nodes_to_visit[0]
        visited.add(node)
        if node not in S:
            S[node] = {}

        for adjacent_node in G[node]:
            if adjacent_node not in visited:
                nodes_to_visit.append(adjacent_node)

            if adjacent_node in S:
                color = "red"
            else:
                color = "green"
                if adjacent_node not in S:
                    S[adjacent_node] = {}

            if adjacent_node not in S[node]:
                S[node][adjacent_node] = color
                S[adjacent_node][node] = color

    return S

# This is just one possible solution
# There are other ways to create a
# spanning tree, and the grader will
# accept any valid result
# feel free to edit the test to
# match the solution your program produces
def test_create_rooted_spanning_tree():
    G = {'a': {'c': 1, 'b': 1},
         'b': {'a': 1, 'd': 1},
         'c': {'a': 1, 'd': 1},
         'd': {'c': 1, 'b': 1, 'e': 1},
         'e': {'d': 1, 'g': 1, 'f': 1},
         'f': {'e': 1, 'g': 1},
         'g': {'e': 1, 'f': 1}
         }
    S = create_rooted_spanning_tree(G, "a")
    assert S == {'a': {'c': 'green', 'b': 'green'},
                 'b': {'a': 'green', 'd': 'red'},
                 'c': {'a': 'green', 'd': 'green'},
                 'd': {'c': 'green', 'b': 'red', 'e': 'green'},
                 'e': {'d': 'green', 'g': 'green', 'f': 'green'},
                 'f': {'e': 'green', 'g': 'red'},
                 'g': {'e': 'green', 'f': 'red'}
                 }
###########

def post_order(S, root, result=None):
    # return mapping between nodes of S and the post-order value
    # of that node
    if result is None:
        result = {}
    result[root] = -1
    for adjacent_node in sorted(S[root]):
        if adjacent_node not in result and S[root][adjacent_node] == "green":
            post_order(S, adjacent_node, result)
    result[root] = 1 + len([x for x in result if result[x] >= 0])
    return result

# This is just one possible solution
# There are other ways to create a
# spanning tree, and the grader will
# accept any valid result.
# feel free to edit the test to
# match the solution your program produces
def test_post_order():
    S = {'a': {'c': 'green', 'b': 'green'},
         'b': {'a': 'green', 'd': 'red'},
         'c': {'a': 'green', 'd': 'green'},
         'd': {'c': 'green', 'b': 'red', 'e': 'green'},
         'e': {'d': 'green', 'g': 'green', 'f': 'green'},
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'}
         }
    po = post_order(S, 'a')
    assert po == {'a':7, 'b':1, 'c':6, 'd':5, 'e':4, 'f':2, 'g':3}

##############

def number_of_descendants(S, root, counts=None):
    # return mapping between nodes of S and the number of descendants
    # of that node
    if counts is None:
        counts = {}
    count = 1 # 1 to count ourself
    counts[root] = None # placeholder to avoid re-traversing this node
    for adjacent_node in sorted(S[root]):
        if S[root][adjacent_node] == "green" and adjacent_node not in counts:
            number_of_descendants(S, adjacent_node, counts)
            sub_count = counts[adjacent_node]
            count += sub_count
    counts[root] = count
    return counts

def test_number_of_descendants():
    S =  {'a': {'c': 'green', 'b': 'green'},
          'b': {'a': 'green', 'd': 'red'},
          'c': {'a': 'green', 'd': 'green'},
          'd': {'c': 'green', 'b': 'red', 'e': 'green'},
          'e': {'d': 'green', 'g': 'green', 'f': 'green'},
          'f': {'e': 'green', 'g': 'red'},
          'g': {'e': 'green', 'f': 'red'}
          }
    nd = number_of_descendants(S, 'a')
    assert nd == {'a':7, 'b':1, 'c':5, 'd':4, 'e':3, 'f':1, 'g':1}

###############

def create_depth_map(S, root, depth=1, depths=None):
    if depths is None:
        depths = {}
    depths[root] = depth
    for adjacent_node in S[root]:
        if adjacent_node not in depths:
            edge_color = S[root][adjacent_node]
            if edge_color == "green":
                create_depth_map(S, adjacent_node, depth+1, depths)
    return depths

def lowest_post_order_recursive(S, root, po, depths, visited=None, red_edge_used=False):
    depth = depths[root]
    min_po = po[root]

    if visited is None:
        visited = set()
    visited.add(root)

    for adjacent_node in S[root]:
        if adjacent_node in visited:
            continue

        edge_color = S[root][adjacent_node]
        if edge_color == "red":
            if red_edge_used:
                continue
            else:
                cur_red_edge_used = True
        else:
            cur_red_edge_used = red_edge_used
            adjacent_node_depth = depths[adjacent_node]
            if adjacent_node_depth < depth:
                continue

        cur_min_po = lowest_post_order_recursive(S, adjacent_node, po, depths,
            visited, cur_red_edge_used)
        if cur_min_po < min_po:
            min_po = cur_min_po

    visited.remove(root)
    return min_po

def lowest_post_order(S, root, po):
    # return a mapping of the nodes in S
    # to the lowest post order value
    # below that node
    # (and you're allowed to follow 1 red edge)
    depths = create_depth_map(S, root)
    return {x: lowest_post_order_recursive(S, x, po, depths) for x in S}

def test_lowest_post_order():
    S = {'a': {'c': 'green', 'b': 'green'},
         'b': {'a': 'green', 'd': 'red'},
         'c': {'a': 'green', 'd': 'green'},
         'd': {'c': 'green', 'b': 'red', 'e': 'green'},
         'e': {'d': 'green', 'g': 'green', 'f': 'green'},
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'}
         }
    po = post_order(S, 'a')
    l = lowest_post_order(S, 'a', po)
    assert l == {'a':1, 'b':1, 'c':1, 'd':1, 'e':2, 'f':2, 'g':2}


################

def highest_post_order_recursive(S, root, po, depths, visited=None, red_edge_used=False):
    depth = depths[root]
    max_po = po[root]

    if visited is None:
        visited = set()
    visited.add(root)

    for adjacent_node in S[root]:
        if adjacent_node in visited:
            continue

        edge_color = S[root][adjacent_node]
        if edge_color == "red":
            if red_edge_used:
                continue
            else:
                cur_red_edge_used = True
        else:
            cur_red_edge_used = red_edge_used
            adjacent_node_depth = depths[adjacent_node]
            if adjacent_node_depth < depth:
                continue

        cur_max_po = highest_post_order_recursive(S, adjacent_node, po, depths,
            visited, cur_red_edge_used)
        if cur_max_po > max_po:
            max_po = cur_max_po

    visited.remove(root)
    return max_po

def highest_post_order(S, root, po):
    # return a mapping of the nodes in S
    # to the highest post order value
    # below that node
    # (and you're allowed to follow 1 red edge)
    depths = create_depth_map(S, root)
    return {x: highest_post_order_recursive(S, x, po, depths) for x in S}

def test_highest_post_order():
    S = {'a': {'c': 'green', 'b': 'green'},
         'b': {'a': 'green', 'd': 'red'},
         'c': {'a': 'green', 'd': 'green'},
         'd': {'c': 'green', 'b': 'red', 'e': 'green'},
         'e': {'d': 'green', 'g': 'green', 'f': 'green'},
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'}
         }
    po = post_order(S, 'a')
    h = highest_post_order(S, 'a', po)
    assert h == {'a':7, 'b':5, 'c':6, 'd':5, 'e':4, 'f':3, 'g':3}

#################

def bridge_edges(G, root):
    # use the four functions above
    # and then determine which edges in G are bridge edges
    # return them as a list of tuples ie: [(n1, n2), (n4, n5)]
    spanning_tree = create_rooted_spanning_tree(G, root)
    postorder = post_order(spanning_tree, root)
    num_descendents = number_of_descendants(spanning_tree, root)
    min_postorder = lowest_post_order(spanning_tree, root, postorder)
    max_postorder = highest_post_order(spanning_tree, root, postorder)

    bridge_edges = []
    unvisited_nodes = [root]
    visited_nodes = set()
    while unvisited_nodes:
        node = unvisited_nodes[0]
        del unvisited_nodes[0]
        visited_nodes.add(node)

        node_po = postorder[node]
        node_nd = num_descendents[node]
        node_minpo = min_postorder[node]
        node_maxpo = max_postorder[node]

        if node != root and (node_maxpo <= node_po) and (node_minpo > (node_po - node_nd)):
            for adjacent_node in spanning_tree[node]:
                edge_color = spanning_tree[node][adjacent_node]
                if edge_color == "red":
                    continue
                adjacent_node_po = postorder[adjacent_node]
                if adjacent_node_po > node_po:
                    bridge_edge = (node, adjacent_node)
                    break
            else:
                assert False, "unable to find green parent of node {}".format(node)

            if bridge_edge not in bridge_edges:
                inverse_bridge_edge = (bridge_edge[1], bridge_edge[0])
                bridge_edges.append(inverse_bridge_edge)

            del bridge_edge # to catch errors if they occur later on

        for adjacent_node in spanning_tree[node]:
            if adjacent_node not in visited_nodes:
                edge_color = spanning_tree[node][adjacent_node]
                if edge_color == "green":
                    unvisited_nodes.append(adjacent_node)

    return bridge_edges

import unittest

class InstructorProvidedTests(unittest.TestCase):

    def test_bridge_edges(self):
        G = {'a': {'c': 1, 'b': 1},
             'b': {'a': 1, 'd': 1},
             'c': {'a': 1, 'd': 1},
             'd': {'c': 1, 'b': 1, 'e': 1},
             'e': {'d': 1, 'g': 1, 'f': 1},
             'f': {'e': 1, 'g': 1},
             'g': {'e': 1, 'f': 1}
             }
        bridges = bridge_edges(G, 'a')
        self.assertListEqual(bridges, [('d', 'e')])

class DenversTests(unittest.TestCase):

    def test_1_node_0_edges(self):
        G = {'a': {}}
        bridges = bridge_edges(G, 'a')
        self.assertListEqual(bridges, [])

    def test_2_nodes_1_edge(self):
        G = {
            'a': {'b': 1},
            'b': {'a': 1},
        }
        bridges = bridge_edges(G, 'a')
        self.assertListEqual(bridges, [('a', 'b')])

    def test_3_nodes_in_a_chain(self):
        G = {
            'a': {'b': 1},
            'b': {'a': 1, 'c': 1},
            'c': {'b': 1},
        }
        bridges = bridge_edges(G, 'a')
        self.assertListEqual(bridges, [('a', 'b'), ('b', 'c')])

    def test_5_nodes_5_edges(self):
        G = {
            'a': {'b': 1, 'c': 1, 'd': 1},
            'b': {'a': 1, 'c': 1},
            'c': {'a': 1, 'b': 1, 'e': 1},
            'd': {'a': 1},
            'e': {'c': 1},
        }
        bridges = bridge_edges(G, 'a')
        self.assertListEqual(bridges, [('a', 'd'), ('c', 'e')])
