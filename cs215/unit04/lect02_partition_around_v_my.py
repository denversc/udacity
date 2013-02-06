#
# Write partition to return a new array with
# all values less then `v` to the left
# and all values greater then `v` to the right
#

def partition(L, v):
    P = []
    num_less_than_v = 0
    for x in L:
        if x < v:
            P.insert(0, x)
            num_less_than_v += 1
        elif x > v:
            P.append(x)
    P.insert(num_less_than_v, v)
    return P

def rank(L, v):
    pos = 0
    for val in L:
        if val < v:
            pos += 1
    return pos

import unittest

class PartitionTest(unittest.TestCase):

    def test_list_length_1(self):
        self.assertListEqual(partition([5], 5), [5])

    def test_list_length_2_PartitionElement0(self):
        self.assertListEqual(partition([4, 5], 4), [4, 5])

    def test_list_length_2_PartitionElement1(self):
        self.assertListEqual(partition([5, 4], 5), [4, 5])

    def test_list_length_3_PartitionElement0(self):
        self.assertListEqual(partition([6, 5, 4], 4), [4, 6, 5])

    def test_list_length_3_PartitionElement1(self):
        self.assertListEqual(partition([6, 4, 5], 5), [4, 5, 6])

    def test_list_length_3_PartitionElement2(self):
        self.assertListEqual(partition([5, 6, 4], 6), [4, 5, 6])










