#
# The code below uses a linear
# scan to find the unfinished node
# with the smallest distance from
# the source.
#
# Modify it to use a heap instead
#

class Heap(object):

    def __init__(self):
        self.values = []
        self.name_index_map = {}

    def __len__(self):
        return len(self.values)

    def __contains__(self, name):
        return name in self.name_index_map

    def add(self, name, value):
        element = (name, value)
        index = len(self.values)
        self.values.append(element)
        self.name_index_map[name] = index
        self._up_heapify(index)

    def remove_smallest_element(self):
        element = self.values[0]
        element_name = element[0]
        del self.name_index_map[element_name]

        last_element = self.values[-1]
        del self.values[-1]
        if len(self.values) > 0:
            self.values[0] = last_element
            last_element_name = last_element[0]
            self.name_index_map[last_element_name] = 0
            self._down_heapify(0)
        return element

    def get_value(self, name):
        index = self.name_index_map[name]
        element = self.values[index]
        value = element[1]
        return value

    def set_value(self, name, new_value):
        index = self.name_index_map[name]
        old_element = self.values[index]
        old_value = old_element[1]
        assert new_value <= old_value, "new_value={} old_value={}".format(new_value, old_value)
        new_element = (name, new_value)
        self.values[index] = new_element
        self._up_heapify(index)

    def _up_heapify(self, index):
        element = self.values[index]
        value = element[1]
        while index > 0:
            parent_index = self._parent_index(index)
            parent_element = self.values[parent_index]
            parent_value = parent_element[1]
            if value < parent_value:
                self._swap(index, parent_index)
                index = parent_index
            else:
                break # heap property is satisfied

    def _down_heapify(self, index):
        element = self.values[index]
        value = element[1]
        while True:
            left_child_index = self._left_child_index(index)
            right_child_index = self._right_child_index(index)

            if left_child_index >= len(self.values):
                left_child_element = None
            else:
                left_child_element = self.values[left_child_index]

            if right_child_index >= len(self.values):
                right_child_element = None
            else:
                right_child_element = self.values[right_child_index]

            if left_child_element is None:
                assert right_child_element is None # sanity check
                break # we are a leaf node; no more down_heapifying necessary
            elif right_child_element is None:
                left_child_value = left_child_element[1]
                if value > left_child_value:
                    self._swap(index, left_child_index)
                break # we are a left node; no more down_heapifying necessary
            else:
                left_child_value = left_child_element[1]
                right_child_value = right_child_element[1]
                if value <= left_child_value and value <= right_child_value:
                    break # heap property satisfied
                if left_child_value > right_child_value:
                    swap_index = right_child_index
                else:
                    swap_index = left_child_index
                self._swap(index, swap_index)
                index = swap_index

    def _swap(self, index1, index2):
        element1 = self.values[index1]
        element2 = self.values[index2]
        self.values[index1] = element2
        self.values[index2] = element1
        name1 = element1[0]
        name2 = element2[0]
        self.name_index_map[name1] = index2
        self.name_index_map[name2] = index1

    def _parent_index(self, index):
        if index <= 0:
            raise ValueError("element {} has no parent".format(index))
        elif index % 2 == 0:
            parent_index = (index / 2) - 1
        else:
            parent_index = (index - 1) / 2
        return parent_index

    def _left_child_index(self, index):
        left_child_index = (index * 2) + 1
        return left_child_index

    def _right_child_index(self, index):
        right_child_index = (index * 2) + 2
        return right_child_index

def dijkstra(G,v):
    dist_so_far = Heap()
    dist_so_far.add(v, 0)
    final_dist = {}
    while len(final_dist) < len(G):
        shortest_dist_node = dist_so_far.remove_smallest_element()
        w = shortest_dist_node[0]
        # lock it down!
        final_dist[w] = shortest_dist_node[1]
        for x in G[w]:
            if x not in final_dist:
                if x not in dist_so_far:
                    distance = final_dist[w] + G[w][x]
                    dist_so_far.add(x, distance)
                else:
                    dist_so_far_x = dist_so_far.get_value(x)
                    possibly_smaller_dist_so_far_x = final_dist[w] + G[w][x]
                    if possibly_smaller_dist_so_far_x < dist_so_far_x:
                        dist_so_far.set_value(x, possibly_smaller_dist_so_far_x)
    return final_dist

############
#
# Test

def make_link(G, node1, node2, w):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        (G[node1])[node2] = 0
    (G[node1])[node2] += w
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        (G[node2])[node1] = 0
    (G[node2])[node1] += w
    return G


def test():
    # shortcuts
    (a,b,c,d,e,f,g) = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    triples = ((a,c,3),(c,b,10),(a,b,15),(d,b,9),(a,d,4),(d,f,7),(d,e,3),
               (e,g,1),(e,f,5),(f,g,2),(b,f,1))
    G = {}
    for (i,j,k) in triples:
        make_link(G, i, j, k)

    dist = dijkstra(G, a)
    assert dist[g] == 8 #(a -> d -> e -> g)
    assert dist[b] == 11 #(a -> d -> e -> g -> f -> b)
