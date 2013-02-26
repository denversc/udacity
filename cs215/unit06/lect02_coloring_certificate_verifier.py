############
#
# Verify a coloring of a graph
#
############

# if cert a k-coloring of G?
#   colors in {0, ..., k-1}
def verify(G, cert, k):
    # make sure each node in the certificate is a node in G
    for node in cert:
        if node not in G:
            return False

    # make sure each node in G is also in the certificate
    for node in G:
        if node not in cert:
            return False

    # check that each node has a different color from all of its adjacent nodes
    colors = set()
    for node in G:
        node_color = cert[node]
        colors.add(node_color)
        for adjacent_node in G[node]:
            adjacent_node_color = cert[adjacent_node]
            if node_color == adjacent_node_color:
                return False # invalid coloring

    # make sure that we got the specified number of distinct colors
    if len(colors) != k:
        return False

    return True

#######
#
# Testing

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G


(a, b, c, d, e, f, g, h) = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
cxns = [(a, c), (a, b), (c, d), (b, d), (d, e), (d, f), (e, g), (f, g), (f, h), (g, h)]

G = {}
for (x, y) in cxns: make_link(G, x, y)


cert = {}
for (node, color) in [(a, 0), (b, 1), (c, 2), (d, 0), (e, 1), (f, 2), (g, 0), (h, 1)]:
    cert[node] = color
print verify(G, cert, 3)

cert = {}
for (node, color) in [(a, 0), (b, 1), (c, 2), (d, 0), (e, 0), (f, 1), (g, 2), (h, 0)]:
    cert[node] = color
print verify(G, cert, 4)
