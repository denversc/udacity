#
# Write partition to return a new array with
# all values less then `v` to the left
# and all values greater then `v` to the right
#

def partition(L, v):
    P = []
    # your code here
    return P

def rank(L, v):
    pos = 0
    for val in L:
        if val < v:
            pos += 1
    return pos
