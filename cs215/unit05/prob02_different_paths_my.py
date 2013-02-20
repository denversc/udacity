"""
Use your code from earlier to change the Marvel graph to only have characters
as nodes. Use 1.0/count as the weight, where count is the number of comic books
each character appeared in together.

For each character in this list
    'SPIDER-MAN/PETER PAR'
    'GREEN GOBLIN/NORMAN '
    'WOLVERINE/LOGAN '
    'PROFESSOR X/CHARLES '
    'CAPTAIN AMERICA'
search your weighted graph. Find all the characters where the shortest path by
weight to that character is different by weight from the shortest path measured
by counting the number of hops.

For example, there is a direct link between 'SPIDER-MAN/PETER PAR' and 'YAP',
but the shortest weighted path between the two is
['SPIDER-MAN/PETER PAR', 'WOLVERINE/LOGAN ', 'SHADOWCAT/KATHERINE ', 'YAP']

As another example, the shortest path by hops between 'WOLVERINE/LOGAN ' and
'HOARFROST/' is
    ['WOLVERINE/LOGAN ', 'CITIZEN V II/HELMUT ', 'HOARFROST/']
but by weight, the shortest path is
    ['WOLVERINE/LOGAN ', 'CYCLOPS/SCOTT SUMMER', 'BEAST/HENRY &HANK& P',
        'CAPTAIN AMERICA', 'HAWK', 'HOARFROST/']

We've given you two of the paths. There are over 20 000 more.
When you've found the total number, fill your answer in box.
"""

import csv
import unittest

def load_marvel_characters():
    """
    Reads the marvel comic characters graph from "marvel_characters.txt".
    Returns a dict whose keys are the names of the comic books and whose values
    are the list of characters that appeared in that comic book.
    """
    comics = {}
    with open("marvel_characters.txt", "rb") as f:
        tsv = csv.reader(f, delimiter='\t')
        for (character, comic) in tsv:
            try:
                characters_in_comic = comics[comic]
            except KeyError:
                comics[comic] = [character]
            else:
                characters_in_comic.append(character)
    return comics


def create_marvel_graph(comics):
    """
    Creates a graph of Marvel characters from the given loaded Marvel comics,
    as returned by load_marvel_characters().

    Returns a graph whose nodes are characters in the given comics where an edge
    between two characters indicates that they co-appeared in one or more comics.
    The weight of the edges is 1/count, where count is the number of comics in
    which the two characters co-appeared.  Therefore, edges with smaller weights
    indicate characters that appear together more often than those with higher
    weights.

    Returns a dict whose keys are the names of the characters and whose values
    are also dicts.  These "value" dicts have character names as their keys,
    which indicates an edge connecting the two character nodes.  The
    corresponding value is the "weight" of the edge.
    """
    graph = {}
    for characters in comics.itervalues():
        for character1 in characters:
            for character2 in characters:
                if character1 is not character2:
                    try:
                        edges = graph[character1]
                    except KeyError:
                        edges = {character2: 1}
                        graph[character1] = edges
                    else:
                        try:
                            edges[character2] += 1
                        except KeyError:
                            edges[character2] = 1

    for edges in graph.itervalues():
        for (character, count) in edges.iteritems():
            new_weight = 1.0 / count
            edges[character] = new_weight

    return graph


def get_shortest_hops(graph, node):
    """
    Calculates the shortest path by number of hops in the given graph from the
    given node to all other nodes.  Returns a dict whose keys are the nodes in
    the given graph and whose values are list of nodes whose values represent
    the shortest path by hops.
    """
    unvisited_nodes = [(node, [node])]
    shortest_hops = {node: [node]}
    while unvisited_nodes:
        (node, path) = unvisited_nodes[0]
        del unvisited_nodes[0]
        for adjacent_node in graph[node]:
            if adjacent_node not in shortest_hops:
                shortest_path = path + [adjacent_node]
                shortest_hops[adjacent_node] = shortest_path
                unvisited_nodes.append((adjacent_node, shortest_path))
    return shortest_hops


def get_shortest_weighted_paths(graph, node):
    """
    Calculates the shortest weighted path in the given graph from the given
    node to all other nodes.  Returns a dict whose keys are the nodes in the
    given graph and whose values are list of nodes whose values represent the
    shortest path by weight.
    """
    return dijkstra(graph, node)

class Heap(object):

    def __init__(self):
        self.values = []
        self.name_index_map = {}

    def __len__(self):
        return len(self.values)

    def __contains__(self, name):
        return name in self.name_index_map

    def add(self, name, value, path):
        element = (name, value, path)
        index = len(self.values)
        self.values.append(element)
        self.name_index_map[name] = index
        self._up_heapify(index)

    def remove_smallest_element(self):
        element = self.values[0]
        element_name = element[0]
        del self.name_index_map[element_name]

        last_element = self.values[-1]
        del self.values[-1]
        if len(self.values) > 0:
            self.values[0] = last_element
            last_element_name = last_element[0]
            self.name_index_map[last_element_name] = 0
            self._down_heapify(0)
        return element

    def get_value(self, name):
        index = self.name_index_map[name]
        element = self.values[index]
        value = element[1]
        return value

    def get_path(self, name):
        index = self.name_index_map[name]
        element = self.values[index]
        path = element[2]
        return path

    def set_value(self, name, new_value, new_path):
        index = self.name_index_map[name]
        old_element = self.values[index]
        old_value = old_element[1]
        assert new_value <= old_value, "new_value={} old_value={}".format(new_value, old_value)
        new_element = (name, new_value, new_path)
        self.values[index] = new_element
        self._up_heapify(index)

    def _up_heapify(self, index):
        element = self.values[index]
        value = element[1]
        while index > 0:
            parent_index = self._parent_index(index)
            parent_element = self.values[parent_index]
            parent_value = parent_element[1]
            if value < parent_value:
                self._swap(index, parent_index)
                index = parent_index
            else:
                break # heap property is satisfied

    def _down_heapify(self, index):
        element = self.values[index]
        value = element[1]
        while True:
            left_child_index = self._left_child_index(index)
            right_child_index = self._right_child_index(index)

            if left_child_index >= len(self.values):
                left_child_element = None
            else:
                left_child_element = self.values[left_child_index]

            if right_child_index >= len(self.values):
                right_child_element = None
            else:
                right_child_element = self.values[right_child_index]

            if left_child_element is None:
                assert right_child_element is None # sanity check
                break # we are a leaf node; no more down_heapifying necessary
            elif right_child_element is None:
                left_child_value = left_child_element[1]
                if value > left_child_value:
                    self._swap(index, left_child_index)
                break # we are a left node; no more down_heapifying necessary
            else:
                left_child_value = left_child_element[1]
                right_child_value = right_child_element[1]
                if value <= left_child_value and value <= right_child_value:
                    break # heap property satisfied
                if left_child_value > right_child_value:
                    swap_index = right_child_index
                else:
                    swap_index = left_child_index
                self._swap(index, swap_index)
                index = swap_index

    def _swap(self, index1, index2):
        element1 = self.values[index1]
        element2 = self.values[index2]
        self.values[index1] = element2
        self.values[index2] = element1
        name1 = element1[0]
        name2 = element2[0]
        self.name_index_map[name1] = index2
        self.name_index_map[name2] = index1

    def _parent_index(self, index):
        if index <= 0:
            raise ValueError("element {} has no parent".format(index))
        elif index % 2 == 0:
            parent_index = (index / 2) - 1
        else:
            parent_index = (index - 1) / 2
        return parent_index

    def _left_child_index(self, index):
        left_child_index = (index * 2) + 1
        return left_child_index

    def _right_child_index(self, index):
        right_child_index = (index * 2) + 2
        return right_child_index

def dijkstra(G, v):
    dist_so_far = Heap()
    dist_so_far.add(v, 0.0, [v])
    final_dist = {}
    while len(final_dist) < len(G):
        try:
            shortest_dist_node = dist_so_far.remove_smallest_element()
        except IndexError:
            break # no more nodes left; this must be a disconnected graph
        w = shortest_dist_node[0]
        shortest_path_length = shortest_dist_node[1]
        shortest_path = shortest_dist_node[2]
        # lock it down!
        final_dist[w] = (shortest_path_length, shortest_path)
        for x in G[w]:
            if x not in final_dist:
                if x not in dist_so_far:
                    distance = final_dist[w][0] + G[w][x]
                    dist_so_far.add(x, distance, final_dist[w][1] + [x])
                else:
                    dist_so_far_x = dist_so_far.get_value(x)
                    possibly_smaller_dist_so_far_x = final_dist[w][0] + G[w][x]
                    if possibly_smaller_dist_so_far_x < dist_so_far_x:
                        dist_so_far.set_value(x, possibly_smaller_dist_so_far_x,
                            final_dist[w][1] + [x])
    return {x:final_dist[x][1] for x in final_dist}

def get_num_different_paths(comics, characters):
    print("create_marvel_graph()")
    graph = create_marvel_graph(comics)
    count = 0
    for character in characters:
        print("Processing {}".format(character))
        shortest_hops = get_shortest_hops(graph, character)
        shortest_weighted_paths = get_shortest_weighted_paths(graph, character)

        for node in shortest_hops:
            assert node in shortest_weighted_paths # sanity check
            hops_path = shortest_hops[node]
            weighted_path = shortest_weighted_paths[node]
            if hops_path != weighted_path:
                count += 1

        # just a sanity check
        for node in shortest_weighted_paths:
            assert node in shortest_hops

    return count

class DenverTests(unittest.TestCase):

    def test_3Nodes(self):
        comics = {
            "book1": ["Spider-Man", "Hulk"],
            "book2": ["Spider-Man", "Hulk"],
            "book3": ["Spider-Man", "He-Man"],
            "book4": ["He-Man", "Hulk"],
        }
        actual = get_num_different_paths(comics, ["Spider-Man", "He-Man", "Hulk"])
        self.assertEqual(actual, 0)

    def test_4NodesDisconnected(self):
        comics = {
            "book1": ["Spider-Man", "Hulk"],
            "book2": ["Spider-Man", "Hulk"],
            "book3": ["She-Ra", "He-Man"],
        }
        actual = get_num_different_paths(comics, ["Spider-Man", "He-Man", "She-Ra", "Hulk"])
        self.assertEqual(actual, 0)

    def test_4NodesChain(self):
        comics = {
            "book1": ["A", "B"],
            "book2": ["B", "C"],
            "book3": ["C", "D"],
        }
        actual = get_num_different_paths(comics, ["A", "B", "C", "D"])
        self.assertEqual(actual, 0)

    def test_4NodesWithRepeats(self):
        comics = {
            "book1": ["A", "B"],
            "book2": ["B", "C"],
            "book3": ["A", "D"], "book4": ["A", "D"], "book5": ["A", "D"], "book6": ["A", "D"],
            "book7": ["E", "D"], "book8": ["E", "D"], "book9": ["E", "D"], "booka": ["E", "D"],
            "bookb": ["E", "C"], "bookc": ["E", "C"], "bookd": ["E", "C"], "booke": ["E", "C"],
        }
        actual = get_num_different_paths(comics, ["A", "B", "C", "D", "E"])
        self.assertEqual(actual, 2)

    def test_3NodesConnected(self):
        comics = {
            "book1": ["A", "B"],
            "book2": ["A", "C"], "book3": ["A", "C"], "book4": ["A", "C"], "book5": ["A", "C"],
            "book5": ["C", "B"], "book6": ["C", "B"], "book7": ["C", "B"], "book8": ["C", "B"],
        }
        actual = get_num_different_paths(comics, ["A", "B", "C"])
        self.assertEqual(actual, 2)

CHARACTERS_OF_INTEREST = [
    'SPIDER-MAN/PETER PAR',
    'GREEN GOBLIN/NORMAN ',
    'WOLVERINE/LOGAN ',
    'PROFESSOR X/CHARLES ',
    'CAPTAIN AMERICA',
]

if __name__ == "__main__":
    print("load_marvel_characters()")
    comics = load_marvel_characters()
    count = get_num_different_paths(comics, CHARACTERS_OF_INTEREST)
    print count
