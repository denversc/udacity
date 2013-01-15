# Find Eulerian Tour
#
# Write a function that takes in a graph
# represented as a list of tuples
# and return a list of nodes that
# you would follow on an Eulerian Tour
#
# For example, if the input graph was
# [(1, 2), (2, 3), (3, 1)]
# A possible Eulerian tour would be [1, 2, 3, 1]

def find_eulerian_tour_recursive(path, edges):
    if len(edges) == 0:
        return path

    start_node = path[-1]
    for edge in edges:
        if start_node in edge:
            next_node = edge[0] if edge[0] != start_node else edge[1]
            edge_index = edges.index(edge)
            edges0 = edges[:edge_index] + edges[edge_index+1:]
            path0 = path + (next_node,)
            tour = find_eulerian_tour_recursive(path0, edges0)
            if tour is not None and tour[0] == tour[-1]:
                return tour

def find_eulerian_tour(graph):
    graph = tuple(graph)
    if len(graph) == 0:
        return []

    for edge in graph:
        for start_node in edge:
            tour = find_eulerian_tour_recursive((start_node,), graph)
            if tour is not None:
                return tour

    assert False, "unable to make a Eulerian tour"

