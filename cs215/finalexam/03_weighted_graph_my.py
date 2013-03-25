#
# In lecture, we took the bipartite Marvel graph,
# where edges went between characters and the comics
# books they appeared in, and created a weighted graph
# with edges between characters where the weight was the
# number of comic books in which they both appeared.
#
# In this assignment, determine the weights between
# comic book characters by giving the probability
# that a randomly chosen comic book containing one of
# the characters will also contain the other
#

from marvel import marvel, characters

def create_weighted_graph(bipartiteG, characters):

    # create a graph that maps comic books to their characters
    comics = {x:set() for x in bipartiteG if x not in characters}
    for character in characters:
        for comic in bipartiteG[character]:
            comics[comic].add(character)
    print(len(comics))

    # create a new graph that maps characters to characters and where the weight
    # of the edges is the number of comics in which they co-appear
    G = {}
    for character1 in characters:
        for character2 in characters:
            if character1 == character2:
                continue

            co_appearance_count = 0
            for comic in bipartiteG[character1]:
                if character2 in comics[comic]:
                    co_appearance_count += 1

            if co_appearance_count > 0:
                if character1 in G:
                    G[character1][character2] = co_appearance_count
                else:
                    G[character1] = {character2: co_appearance_count}

                if character2 in G:
                    G[character2][character1] = co_appearance_count
                else:
                    G[character2] = {character1: co_appearance_count}

    # translate the edge weights into probabilities
    num_comics = len(comics)
    for character1 in G:
        for character2 in G[character1]:
            num_co_appearances = G[character1][character2]
            appearing_comics = set(bipartiteG[character1]) | set(bipartiteG[character2])
            num_appearing_comics = len(appearing_comics)

            p_both_chars_coappear = float(num_co_appearances) / num_comics
            p_once_of_chars_appear = float(num_appearing_comics) / num_comics
            p_both_chars_appear_given_once_char_appears = p_both_chars_coappear / p_once_of_chars_appear
            G[character1][character2] = p_both_chars_appear_given_once_char_appears

    return G

######
#
# Test

import unittest

class DenverTests(unittest.TestCase):

    def test_Provided1(self):
        bipartiteG = {'charA':{'comicB':1, 'comicC':1},
                      'charB':{'comicB':1, 'comicD':1},
                      'charC':{'comicD':1},
                      'comicB':{'charA':1, 'charB':1},
                      'comicC':{'charA':1},
                      'comicD': {'charC':1, 'charB':1}}
        G = create_weighted_graph(bipartiteG, ['charA', 'charB', 'charC'])
        # three comics contain charA or charB
        # charA and charB are together in one of them
        self.assertEqual(G['charA']['charB'], 1.0 / 3)
        self.assertIsNone(G['charA'].get('charA'))
        self.assertIsNone(G['charA'].get('charC'))

    def test_Provided2(self):
        create_weighted_graph(marvel, characters)

    def test_Denver1(self):
        G = create_weighted_graph(marvel, characters)
        self.assertEqual(G["HULK/DR. ROBERT BRUC"]["DEMOLITION MAN/DENNI"], 0.0345)
