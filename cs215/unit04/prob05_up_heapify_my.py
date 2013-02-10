#
# write up_heapify, an algorithm that checks if
# node i and its parent satisfy the heap
# property, swapping and recursing if they don't
#
# L should be a heap when up_heapify is done
#

def up_heapify(L, i):
    if i != 0:
        value = L[i]
        parent_index = parent(i)
        parent_value = L[parent_index]
        if value < parent_value:
            L[parent_index] = value
            L[i] = parent_value
            up_heapify(L, parent_index)

def parent(i):
    return (i - 1) / 2
def left_child(i):
    return 2 * i + 1
def right_child(i):
    return 2 * i + 2
def is_leaf(L, i):
    return (left_child(i) >= len(L)) and (right_child(i) >= len(L))
def one_child(L, i):
    return (left_child(i) < len(L)) and (right_child(i) >= len(L))

import unittest

class InstructorTests(unittest.TestCase):
    def test1(self):
        L = [2, 4, 3, 5, 9, 7, 7]
        L.append(1)
        up_heapify(L, 7)
        self.assertEqual(L[0], 1)
    def test2(self):
        L = [2, 4, 3, 5, 9, 7, 7]
        L.append(1)
        up_heapify(L, 7)
        self.assertEqual(L[1], 2)
        assert 2 == L[1]
