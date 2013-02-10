#
# Given a list L of n numbers, find the mode
# (the number that appears the most times).
# Your algorithm should run in Theta(n).
# If there are ties - just pick one value to return
#

def mode(L):
    counts = {}
    for element in L:
        if element in counts:
            counts[element] += 1
        else:
            counts[element] = 1

    max_count = 0
    for element in counts:
        cur_count = counts[element]
        if cur_count > max_count:
            max_element = element
            max_count = cur_count
    return max_element


import unittest
import time
from random import randint

class InstructorTest(unittest.TestCase):

    def test(self):
        assert 5 == mode([1, 5, 2, 5, 3, 5])
        iterations = (10, 20, 30, 100, 200, 300, 1000, 5000, 10000, 20000, 30000)
        times = []
        for i in iterations:
            L = []
            for j in range(i):
                L.append(randint(1, 10))
            start = time.clock()
            for j in range(500):
                mode(L)
            end = time.clock()
            print start, end
            times.append(float(end - start))
        slopes = []
        for (x1, x2), (y1, y2) in zip(zip(iterations[:-1], iterations[1:]), zip(times[:-1], times[1:])):
            print (x1, x2), (y1, y2)
            slopes.append((y2 - y1) / (x2 - x1))
        # if mode runs in linear time,
        # these factors should be close (kind of)
        print slopes

# test()
