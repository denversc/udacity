"""
Using the supplied imdb-1.tsv calculate the top 20 central actors,
using the average centrality measurement given in unit 3.
The top central actor is Tatasciore, Ford.  Who is the 20th?
"""

import collections
import io
import os

def main():
    movies = load_movies()
    graph = actor_graph_from_movies(movies)
    centralities = calculate_actor_centralities(graph)
    centralities.sort(key=lambda x:x[1])
    for (index, (node, centrality)) in enumerate(centralities[:20], 1):
        msg = u"{}: {} ({})".format(index, node, centrality)
        print(msg.encode("us-ascii", errors="replace"))

def calculate_actor_centralities(graph):
    print("calculate_centralities()")
    centralities = []
    try:
        for (index, node) in enumerate(graph, 1):
            if node.node_type == "actor":
                centrality = actor_centrality(graph, node)
                centralities.append((node.name, centrality))
            if index % 50 == 0:
                print("{}/{}".format(index, len(graph)))
    except KeyboardInterrupt:
        pass
    return centralities

def actor_centrality(graph, root):
    for node in graph:
        node.visited = False
        node.path_length = None

    path_lengths_sum = 0
    unvisited_nodes = collections.deque()
    unvisited_nodes.append(root)
    root.visited = True
    root.path_length = 0

    while unvisited_nodes:
        node = unvisited_nodes.popleft()
        for adjacent_node in node.adjacent_nodes:
            if not adjacent_node.visited:
                adjacent_node.visited = True
                adjacent_node.path_length = node.path_length + 1
                unvisited_nodes.append(adjacent_node)
                path_lengths_sum += adjacent_node.path_length

    centrality = float(path_lengths_sum) / float(len(graph) - 1)
    return centrality

def actor_graph_from_movies(movies):
    print("actor_graph_from_movies()")
    movie_nodes = {}
    actor_nodes = {}

    for (movie, actors) in movies.iteritems():
        for actor in actors:
            if actor in actor_nodes:
                actor_node = actor_nodes[actor]
            else:
                actor_node = Node(actor, "actor")
                actor_nodes[actor] = actor_node

            if movie in movie_nodes:
                movie_node = movie_nodes[movie]
            else:
                movie_node = Node(movie, "movie")
                movie_nodes[movie] = movie_node

            actor_node.adjacent_nodes.add(movie_node)
            movie_node.adjacent_nodes.add(actor_node)

    nodes = []
    nodes.extend(actor_nodes.values())
    nodes.extend(movie_nodes.values())
    return nodes

class Node(object):
    def __init__(self, name, node_type):
        self.name = name
        self.node_type = node_type
        self.adjacent_nodes = set()
        self.visited = False
        self.path_length = 0
    def __eq__(self, other):
        return (self.name == other.name) and (self.node_type == other.node_type)
    def __ne__(self, other):
        return (self.name != other.name) and (self.node_type != other.node_type)
    def __hash__(self):
        return hash(self.name)
    def __str__(self):
        return "{} ({})".format(self.name, self.node_type)
    def __repr__(self):
        return "Node({!r}, {!r})".format(self.name, self.node_type)

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
