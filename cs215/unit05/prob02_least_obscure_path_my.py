# -*- coding: UTF-8 -*-
#
# Another way of thinking of a path in the Kevin Bacon game
# is not about finding *short* paths, but by finding paths
# that don’t use obscure movies.  We will give you a
# list of movies along with their obscureness score.
#
# For this assignment, we'll approximate obscurity
# based on the multiplicative inverse of the amount of
# money the movie made.  Though, its not really important where
# the obscurity score came from.
#
# Use the the imdb-1.tsv and imdb-weights.tsv files to find
# the obscurity of the “least obscure”
# path from a given actor to another.
# The obscurity of a path is the maximum obscurity of
# any of the movies used along the path.
#
# You will have to do the processing in your local environment
# and then copy in your answer.
#
# Hint: A variation of Dijkstra can be used to solve this problem.
#

import io
import threading

class Movie(object):
    __slots__ = ("name", "year", "obscurity_score", "actors")
    def __init__(self, name, year, obscurity_score):
        self.name = name
        self.year = year
        self.obscurity_score = obscurity_score
        self.actors = []
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        if isinstance(other, Movie):
            return self.name == other.name and self.year == other.year
        else:
            return False
    def __str__(self):
        return "{} ({})".format(self.name, self.year)
    def __repr__(self):
        return "Movie({0.name!r}, {0.year!r}, {0.obscurity_score!r})".format(self)


class Actor(object):
    __slots__ = ("name", "__hash__", "index", "movies", "connections")
    def __init__(self, name):
        self.name = name
        self.__hash__ = name.__hash__
        self.index = None
        self.movies = []
        self.connections = {}
    def __eq__(self, other):
        return self.name == other.name
    def __str__(self):
        return u"{}".format(self.name)
    def __repr__(self):
        return "Actor({!r})".format(self.name)


def load_graph():
    """
    Loads the movie database and returns the actors and their connections.
    Returns a list of Actor objects whose "movie" attributes are None but whose
    "connections" attribute is a dict whose keys are actors, with whom they have
    co-appeared, and whose values are floats, the obscurity score of the
    smallest obscurity score of all movies in which the two actors co-appeared.
    """
    print("Loading imdb-weights.tsv")
    movies = {}
    with io.open("imdb-weights.tsv", "rt", encoding="UTF-8") as f:
        for line in f:
            (name, year, revenue_str) = line.rstrip().split(u"\t")
            revenue = float(revenue_str)
            obscurity_score = 1.0 / revenue
            key = (name, year)
            assert key not in movies
            movies[key] = Movie(name, year, obscurity_score)

    print("Loading imdb-1.tsv")
    actors = {}
    with io.open("imdb-1.tsv", "rt", encoding="UTF-8") as f:
        for line in f:
            (actor_name, movie_name, movie_year) = line.rstrip().split(u"\t")
            try:
                actor = actors[actor_name]
            except KeyError:
                actor = Actor(actor_name)
                actors[actor_name] = actor

            movie = movies[(movie_name, movie_year)]
            actor.movies.append(movie)
            movie.actors.append(actor)

    print("Building connections between actors")
    for actor1 in actors.itervalues():
        for movie in actor1.movies:
            for actor2 in movie.actors:
                if actor1 != actor2:
                    try:
                        cur_min_obscurity_score = actor1.connections[actor2]
                    except KeyError:
                        actor1.connections[actor2] = movie.obscurity_score
                    else:
                        if cur_min_obscurity_score > movie.obscurity_score:
                            actor1.connections[actor2] = movie.obscurity_score

    print("Cleaning up actors")
    actors = [x for x in actors.itervalues()]
    for actor in actors:
        actor.movies = None
    return tuple(actors)

def calculate_least_obscure_paths_between_actors(actors):
    """
    Calculates the obscurity score of the least obscure path between all pairs
    of actors in the given graph.
    *actors* must be the object returned from load_graph().
    Returns a dict whose keys are Actor objects and whose values are dicts.
    The value dicts also have Actor objects as their keys and their values
    are floats whose values are the maximum obscurity score of the most obscure
    movie on the shortest path between the two actors.
    """
    # for Floyd-Warshall, we need to assign a numeric value to each actor node
    actors_len = len(actors)
    print("Initializing Actor Indices ({})".format(actors_len))
    actor_indices = tuple(x for x in xrange(actors_len))
    for (index, actor) in enumerate(actors):
        actor.index = index
    del index
    del actor

    # fill in the initial matrix with direct links in the graph
    print("Creating initial matrix")
    matrix = [[None] * (actors_len - i) for i in reversed(actor_indices)]
    for i in actor_indices:
        actor1 = actors[i]
        matrix[i][i] = 0.0 # a node links to itself with no cost
        for (actor2, obscurity_score) in actor1.connections.iteritems():
            assert actor1.index != actor2.index, "{}=={} ({!r}, {!r})".format(actor1.index, actor2.index, actor1, actor2)
            if actor2.index < actor1.index:
                matrix[actor1.index][actor2.index] = obscurity_score
    del i
    del actor1
    del actor2

    floyd_warshall(matrix, actors, actor_indices)

    return matrix

def floyd_warshall(matrix, actors, actor_indices):
    for k in actor_indices:
        print("k={}".format(k))
        actork = actors[k]
        for row in actor_indices:
            for col in actor_indices:
                # since the edges are two-way, the matix is symmetric and we
                # can ignore the bottom half
                if col > row:
                    continue

                actor1 = actors[row]
                if actork not in actor1.connections:
                    continue
                actor1_k_obscurity = actor1.connections[actork]

                actor2 = actors[col]
                if actork not in actor2.connections:
                    continue
                actor2_k_obscurity = actor2.connections[actork]

                if actor1_k_obscurity >= actor2_k_obscurity:
                    min_obscurity_2 = actor1_k_obscurity
                else:
                    min_obscurity_2 = actor2_k_obscurity

                cur_min_obscurity = matrix[row][col]
                if cur_min_obscurity is None or min_obscurity_2 < cur_min_obscurity:
                    matrix[row][col] = min_obscurity_2



# Change the `None` values in this dictionary to be the obscurity score
# of the least obscure path between the two actors
answer = {(u'Boone Junior, Mark', u'Del Toro, Benicio'): None,
          (u'Braine, Richard', u'Coogan, Will'): None,
          (u'Byrne, Michael (I)', u'Quinn, Al (I)'): None,
          (u'Cartwright, Veronica', u'Edelstein, Lisa'): None,
          (u'Curry, Jon (II)', u'Wise, Ray (I)'): None,
          (u'Di Benedetto, John', u'Hallgrey, Johnathan'): None,
          (u'Hochendoner, Jeff', u'Cross, Kendall'): None,
          (u'Izquierdo, Ty', u'Kimball, Donna'): None,
          (u'Jace, Michael', u'Snell, Don'): None,
          (u'James, Charity', u'Tuerpe, Paul'): None,
          (u'Kay, Dominic Scott', u'Cathey, Reg E.'): None,
          (u'McCabe, Richard', u'Washington, Denzel'): None,
          (u'Reid, Kevin (I)', u'Affleck, Rab'): None,
          (u'Reid, R.D.', u'Boston, David (IV)'): None,
          (u'Restivo, Steve', u'Preston, Carrie (I)'): None,
          (u'Rodriguez, Ramon (II)', u'Mulrooney, Kelsey'): None,
          (u'Rooker, Michael (I)', u'Grady, Kevin (I)'): None,
          (u'Ruscoe, Alan', u'Thornton, Cooper'): None,
          (u'Sloan, Tina', u'Dever, James D.'): None,
          (u'Wasserman, Jerry', u'Sizemore, Tom'): None}

# Here are some test cases.
# For example, the obscurity score of the least obscure path
# between 'Ali, Tony' and 'Allen, Woody' is 0.5657
test = {(u'Ali, Tony', u'Allen, Woody'): 0.5657,
        (u'Auberjonois, Rene', u'MacInnes, Angus'): 0.0814,
        (u'Avery, Shondrella', u'Dorsey, Kimberly (I)'): 0.7837,
        (u'Bollo, Lou', u'Jeremy, Ron'): 0.4763,
        (u'Byrne, P.J.', u'Clarke, Larry'): 0.109,
        (u'Couturier, Sandra-Jessica', u'Jean-Louis, Jimmy'): 0.3649,
        (u'Crawford, Eve (I)', u'Cutler, Tom'): 0.2052,
        (u'Flemyng, Jason', u'Newman, Laraine'): 0.139,
        (u'French, Dawn', u'Smallwood, Tucker'): 0.2979,
        (u'Gunton, Bob', u'Nagra, Joti'): 0.2136,
        (u'Hoffman, Jake (I)', u'Shook, Carol'): 0.6073,
        (u'Kamiki, Ry\xfbnosuke', u'Thor, Cameron'): 0.3644,
        (u'Roache, Linus', u'Dreyfuss, Richard'): 0.6731,
        (u'Sanchez, Phillip (I)', u'Wiest, Dianne'): 0.5083,
        (u'Sheppard, William Morgan', u'Crook, Mackenzie'): 0.0849,
        (u'Stan, Sebastian', u'Malahide, Patrick'): 0.2857,
        (u'Tessiero, Michael A.', u'Molen, Gerald R.'): 0.2056,
        (u'Thomas, Ken (I)', u'Bell, Jamie (I)'): 0.3941,
        (u'Thompson, Sophie (I)', u'Foley, Dave (I)'): 0.1095,
        (u'Tzur, Mira', u'Heston, Charlton'): 0.3642}

def do_test(graph, matrix, actor1_name, actor2_name, expected):
    for actor1 in graph:
        if actor1.name == actor1_name:
            break
    else:
        raise Exception("cannot find actor: {}".format(actor1_name))

    for actor2 in graph:
        if actor2.name == actor2_name:
            break
    else:
        raise Exception("cannot find actor: {}".format(actor2_name))

    row = actor1.index
    col = actor2.index
    if col > row:
        row, col = col, row

    actual = matrix[row][col]
    if actual == expected:
        print(u"PASS {}->{}".format(actor1, actor2).encode("US-ASCII", errors="replace"))
    else:
        print(u"** FAIL ** {}->{} actual={} expected={}".format(actor1, actor2, actual, expected).encode("US-ASCII", errors="replace"))

if __name__ == "__main__":
    graph = load_graph()
    least_obscure_paths = calculate_least_obscure_paths_between_actors(graph)
    for actors in test:
        expected = test[actors]
        do_test(graph, least_obscure_paths, actors[0], actors[1], expected)
