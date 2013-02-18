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
    Calculates the shortest number of hops in the given graph from the given
    node to all other nodes.  Returns a dict whose keys are the nodes in the
    given graph and whose values are ints whose values are the shortest hops.
    """
    unvisited_nodes = [(node, 0)]
    shortest_hops = {node: 0}
    while unvisited_nodes:
        (node, path_length) = unvisited_nodes[0]
        del unvisited_nodes[0]
        adjacent_nodes_path_length = path_length + 1
        for adjacent_node in graph[node]:
            if adjacent_node not in shortest_hops:
                shortest_hops[adjacent_node] = adjacent_nodes_path_length
                unvisited_nodes.append((adjacent_node, adjacent_nodes_path_length))
    return shortest_hops


def get_shortest_weighted_paths(graph, node):
    """
    Calculates the shortest weighted path in the given graph from the given
    node to all other nodes.  Returns a dict whose keys are the nodes in the
    given graph and whose values are floats whose values are the sums of the
    weights of a shortest weighted path.
    """
    # TO BE IMPLEMENTED

CHARACTERS_OF_INTEREST = [
    'SPIDER-MAN/PETER PAR',
    'GREEN GOBLIN/NORMAN ',
    'WOLVERINE/LOGAN ',
    'PROFESSOR X/CHARLES ',
    'CAPTAIN AMERICA',
]

if __name__ == "__main__":
    comics = load_marvel_characters()
    graph = create_marvel_graph(comics)
    for character in CHARACTERS_OF_INTEREST:
        shortest_hops = get_shortest_hops(graph, character)
        shortest_weighted_paths = get_shortest_weighted_paths(graph, character)




