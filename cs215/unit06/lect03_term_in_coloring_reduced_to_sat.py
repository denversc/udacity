"""
Calculate the number of "clauses" in the formula generated that reduces the
k-colorability problem to SAT.
"""

def factorial(n):
    product = n
    for number in range(n - 1):
        product *= (number + 1)
    return product

def num_combinations(n, k):
    n_factorial = factorial(n)
    k_factorial = factorial(k)
    n_minus_k_factorial = factorial(n - k)
    return n_factorial / (k_factorial * n_minus_k_factorial)

def num_terms_helper(n, m, k):
    # each node has one clause that ensures that it is assigned at least 1 color
    yield n

    # for each node there is one clause per pair of colors, to ensure that no
    # more than 1 color is assigned to the node; so the formula per node is
    # C(n, 2) whose formula is n!/(k!(n-k)!)
    num_color_pairwise_combinations = num_combinations(k, 2)
    yield n * num_color_pairwise_combinations

    # for each edge there is a clause to ensure that the two nodes connected by
    # the edge do not have the same color; each color is checked individually
    yield m * k

def num_terms(n, m, k):
    """
    Returns the number of terms in a boolean formula that is satisfiable if and
    only if a graph G with n nodes and m edges can be colored with k colors.
    n is the number of nodes.
    m is the number of edges.
    k is the number of colors.
    """
    return sum(num_terms_helper(n, m, k))
