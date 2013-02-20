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

class Movie(object):
    __slots__ = ("name", "year", "obscurity_score")
    def __init__(self, name, year, obscurity_score):
        self.name = name
        self.year = year
        self.obscurity_score = obscurity_score
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
    __slots__ = ("name")
    def __init__(self, name):
        self.name = name
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        if isinstance(other, Actor):
            return self.name == other.name
        else:
            return False
    def __str__(self):
        return "{}".format(self.name)
    def __repr__(self):
        return "Actor({!r})".format(self.name)

def load_graph():
    """
    Loads the movie database and returns it as a weighted graph.
    Returns a graph connecting movies to actors that appeared in those movies.
    The graph is stored as a dict whose keys are Actor and Movie objects and
    whose values are sets whose values are also Actor and Movie objects to
    which the node is connected.
    """
    movies = {}
    with io.open("imdb-weights.tsv", "rt", encoding="UTF-8") as f:
        for line in f:
            (name, year, revenue_str) = line.rstrip().split(u"\t")
            revenue = float(revenue_str)
            obscurity_score = 1.0 / revenue
            key = (name, year)
            assert key not in movies
            movies[key] = Movie(name, year, obscurity_score)

    graph = {}
    with io.open("imdb-1.tsv", "rt", encoding="UTF-8") as f:
        for line in f:
            (actor_name, movie_name, movie_year) = line.rstrip().split(u"\t")
            movie = movies[(movie_name, movie_year)]
            actor = Actor(actor_name)
            if movie in graph:
                graph[movie].add(actor)
            else:
                graph[movie] = set([actor])
            if actor in graph:
                graph[actor].add(movie)
            else:
                graph[actor] = set([movie])

    for key in tuple(graph.keys()):
        graph[key] = frozenset(graph[key])

    return {x: frozenset(y) for x, y in graph.iteritems()}

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

if __name__ == "__main__":
    graph = load_graph()
    from pprint import pprint as pp
    pp(graph)
