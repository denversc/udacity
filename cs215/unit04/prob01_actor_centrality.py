"""
Using the supplied imdb-1.tsv calculate the top 20 central actors,
using the average centrality measurement given in unit 3.
The top central actor is Tatasciore, Ford.  Who is the 20th?
"""

import io
import os
import pprint

def main():
    movies = load_movies()
    graph = actor_graph_from_movies(movies)
    centralities = calculate_centralities(graph)
    centralities.sort(key=lambda x:x[1])
    for (index, (node, centrality)) in enumerate(centralities[:20], 1):
        msg = u"{}: {} ({})".format(index, node, centrality)
        print(msg.encode("us-ascii", errors="replace"))

def calculate_centralities(graph):
    print("calculate_centralities()")
    centralities = []
    try:
        for (index, node) in enumerate(graph.itervalues(), 1):
            cur_centrality = centrality(graph, node)
            centralities.append((node.name, cur_centrality))
            if index % 20 == 0:
                print("{}/{}".format(index, len(graph)))
    except KeyboardInterrupt:
        pass
    return centralities

def centrality(graph, root):
    for node in graph.itervalues():
        node.visited = False
        node.path_length = None

    path_lengths_sum = 0
    unvisited_nodes = [None] * len(graph)
    unvisited_nodes[0] = root
    unvisited_nodes_index = 0
    unvisited_nodes_len = 1
    root.visited = True
    root.path_length = 0

    while unvisited_nodes_index < unvisited_nodes_len:
        node = unvisited_nodes[unvisited_nodes_index]
        unvisited_nodes_index += 1
        path_lengths_sum += node.path_length
        for adjacent_node in node.adjacent_nodes:
            if not adjacent_node.visited:
                adjacent_node.visited = True
                adjacent_node.path_length = node.path_length + 1
                unvisited_nodes[unvisited_nodes_len] = adjacent_node
                unvisited_nodes_len += 1

    centrality = float(path_lengths_sum) / float(unvisited_nodes_len)
    return centrality

def actor_graph_from_movies(movies):
    print("actor_graph_from_movies()")
    nodes = {}
    for actors in movies.itervalues():
        for actor1 in actors:
            if actor1 in nodes:
                node1 = nodes[actor1]
            else:
                node1 = Node(actor1)
                nodes[actor1] = node1

            for actor2 in actors:
                if actor1 != actor2:
                    if actor2 in nodes:
                        node2 = nodes[actor2]
                    else:
                        node2 = Node(actor2)
                        nodes[actor2] = node2

                    node1.adjacent_nodes.add(node2)
    return nodes

class Node(object):
    def __init__(self, name):
        self.name = name
        self.adjacent_nodes = set()
        self.visited = False
        self.path_length = 0
    def __eq__(self, other):
        return self.name == other.name
    def __ne__(self, other):
        return self.name != other.name
    def __hash__(self):
        return hash(self.name)
    def __str__(self):
        return self.name
    def __repr__(self):
        return "Node({!r})".format(self.name)

def load_movies():
    print("load_movies()")
    movies = {}
    path = get_imdb_path()
    with io.open(path, "rt", encoding="UTF-8") as f:
        for line in f:
            (actor, movie, year) = line.strip().split(u"\t")
            movie_info = (movie, year)
            if movie_info in movies:
                actors = movies[movie_info]
            else:
                actors = set()
                movies[movie_info] = actors
            actors.add(actor)
    return movies

def get_imdb_path():
    dir_path = os.path.dirname(__file__)
    path = os.path.join(dir_path, "imdb-1.tsv")
    return path

if __name__ == "__main__":
    main()
