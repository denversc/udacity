#
# Given a list of numbers, L, find a number, x, that
# minimizes the sum of the absolute value of the difference
# between each element in L and x: SUM_{i=0}^{n-1} |L[i] - x|
#
# Your code should run in Theta(n) time
#

def minimize_absolute(L):
    length = len(L)
    if length % 2 != 0:
        x = find_kth_sorted_element(L, (length - 1) / 2)
    else:
        x1 = find_kth_sorted_element(L, length / 2)
        x2 = find_kth_sorted_element(L, (length / 2) - 1)
        # need to figure out which of x1 and x2 minimizes
        x1_sum = sum(abs(x - x1) for x in L)
        x2_sum = sum(abs(x - x2) for x in L)
        x = x1 if x1_sum < x2_sum else x2
    return x

def find_kth_sorted_element(L, k):
    partition = L[0]
    lower = []
    upper = []
    for index in xrange(1, len(L)):
        element = L[index]
        if element <= partition:
            lower.append(element)
        else:
            upper.append(element)

    rank_partition = len(lower)
    if rank_partition == k:
        return partition
    elif rank_partition > k:
        return find_kth_sorted_element(lower, k)
    else:
        return find_kth_sorted_element(upper, k - rank_partition - 1)

import unittest
import random

class DenverTests(unittest.TestCase):
    
    def test_ListLength1(self):
        actual = minimize_absolute([5])
        self.assertEqual(actual, 5)
    
    def test_ListLength2_AllSameValues(self):
        actual = minimize_absolute([5, 5])
        self.assertEqual(actual, 5)
    
    def test_ListLength2_DifferentValues_Index0IsCorrect(self):
        actual = minimize_absolute([5, 8])
        self.assertEqual(actual, 5)
    
    def test_ListLength2_DifferentValues_Index1IsCorrect(self):
        actual = minimize_absolute([8, 5])
        self.assertEqual(actual, 5)
    
    def test_ListLength3_SameValues(self):
        actual = minimize_absolute([5, 5, 5])
        self.assertEqual(actual, 5)
    
    def test_ListLength3_DifferentValues_Index0IsCorrect(self):
        actual = minimize_absolute([5, 3, 8])
        self.assertEqual(actual, 5)
    
    def test_ListLength3_DifferentValues_Index1IsCorrect(self):
        actual = minimize_absolute([8, 5, 3])
        self.assertEqual(actual, 5)
    
    def test_ListLength3_DifferentValues_Index2IsCorrect(self):
        actual = minimize_absolute([8, 3, 5])
        self.assertEqual(actual, 5)
    
    def test_BigList(self):
        values = list(range(5001))
        random.shuffle(values)
        actual = minimize_absolute(values)
        self.assertEqual(actual, 2500)
