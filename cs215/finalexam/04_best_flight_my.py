#
# In many path-finding applications, a natural scoring function is
# "lexicographic ordering".  That is, there is one attribute of the
# path (say cost) that is the most important thing to minimize.
# However, all things being equal, if you have two paths with the same
# cost, you might prefer one with a shorter total flight time.
#
# A recent example of lexicographic ordering: In the Olympics Medal
# Tracker website, countries are sorted from most total medals to
# least total medals.  If two countries have the same number of total
# medals, the one with more gold medals is listed first.  If they have
# the same total medals and the same number of gold medals, the one
# with more silver medals is listed first.
#
# We want you to take the list of flights, given below, and create a
# graph.  Then, write a modified Dijkstra's algorithm to find the best
# combination of flights to get between two cities, where flights `x`
# is better than flights `y` if `x` has lower cost *or* if they are
# tied in cost, `x` has shorter total flight time.
#
# Concretely, to get from Broome to Fitroy Crossing,
# flights [530, 112] are better than flights [526, 622]
# because, since they both cost 110, the first flights are
# shorter - 5 hours and 52 minutes compared to
# 6 hours and 23 minutes. There maybe be even better flights, but
# you'll have to search the graph to find them.
#

class Flight(object):

    def __init__(self, number, depart_city, arrive_city, depart_time,
            arrive_time, cost):
        self.number = number
        self.depart_city = depart_city
        self.arrive_city = arrive_city
        self.depart_time = depart_time
        self.arrive_time = arrive_time
        self.cost = cost

    def total_cost(self):
        flight_length = self.arrive_time - self.depart_time
        total_cost = (self.cost, flight_length)
        return total_cost

    def __str__(self):
        return ("{0.number} {0.depart_city} {0.depart_time} to "
            "{0.arrive_city} {0.arrive_time} for ${0.cost}".format(self))

    def __repr__(self):
        return ("Flight({0.number!r}, {0.depart_city!r}, {0.arrive_city!r}, "
            "{0.depart_time!r}, {0.arrive_time!r}, {0.cost!r})".format(self))

def parse_time_str(s):
    (hour_str, minute_str) = s.split(":")
    hour = int(hour_str)
    minute = int(minute_str)
    t = (hour * 60) + minute
    return t

def flight_tuples_to_objects(flight_tuples):
    for flight_tuple in flight_tuples:
        (number, depart_city, arrive_city, depart_time_str, arrive_time_str,
            cost) = flight_tuple
        depart_time = parse_time_str(depart_time_str)
        arrive_time = parse_time_str(arrive_time_str)
        flight_obj = Flight(number, depart_city, arrive_city, depart_time,
            arrive_time, cost)
        yield flight_obj

def make_flight_graph(flights):
    cities = {}
    G = {}

    # build the graph, except for the flights outgoing from the "gadgets"
    for flight in flights:
        arrive_city = flight.arrive_city
        arrive_time = flight.arrive_time
        arrive_city_mangled = (arrive_city, arrive_time)
        if arrive_city_mangled not in G:
            G[arrive_city_mangled] = {}

        if arrive_city not in cities:
            cities[arrive_city] = set()
        cities[arrive_city].add(arrive_city_mangled)

        depart_city = flight.depart_city
        if depart_city not in G:
            G[depart_city] = {}

        if arrive_city_mangled not in G[depart_city]:
            G[depart_city][arrive_city_mangled] = flight
        else:
            conflicting_flight = G[depart_city][arrive_city_mangled]
            flight_total_cost = flight.total_cost()
            conflicting_flight_total_cost = conflicting_flight.total_cost()
            if flight_total_cost < conflicting_flight_total_cost:
                G[depart_city][arrive_city_mangled] = flight

        if depart_city not in cities:
            cities[depart_city] = set()

    # add the flights going out from the gadgets
    for flight in flights:
        arrive_city = flight.arrive_city
        arrive_time = flight.arrive_time
        arrive_city_mangled = (arrive_city, arrive_time)
        depart_time = flight.depart_time

        depart_city = flight.depart_city
        depart_cities_mangled = cities[depart_city]
        for depart_city_mangled in depart_cities_mangled:
            min_depart_time = depart_city_mangled[1]
            if depart_time >= min_depart_time:
                G[depart_city_mangled][arrive_city_mangled] = flight

    return (G, cities)

def find_best_flights(flights, origin, destination):
    flights = flight_tuples_to_objects(flights)
    flights = tuple(flights)
    (G, cities) = make_flight_graph(flights)

    destination_cities = cities[destination]
    destination_cities_remaining = set(destination_cities)
    partial = {origin: ((0, 0), [])}
    complete = {}

    while partial:

        # find the node with the smallest weight in partial
        node = None
        node_weight = None
        node_path = None
        for (cur_node, (cur_node_weight, cur_path)) in partial.iteritems():
            if node is None or cur_node_weight < node_weight:
                node = cur_node
                node_weight = cur_node_weight
                node_path = cur_path

        # update the weights for all nodes in partial
        for (adjacent_node, connecting_flight) in G[node].iteritems():
            if adjacent_node in complete:
                continue

            connecting_flight_weight = connecting_flight.total_cost()
            adjacent_node_new_weight = node_weight + connecting_flight_weight
            new_path = node_path + [connecting_flight]
            if adjacent_node not in partial:
                partial[adjacent_node] = (adjacent_node_new_weight, new_path)
            else:
                adjacent_node_weight = partial[adjacent_node]
                if adjacent_node_new_weight < adjacent_node_weight:
                    partial[adjacent_node] = (adjacent_node_new_weight, new_path)

        # move this node into the completed set
        del partial[node]
        complete[node] = (node_weight, node_path)

        # update the list of uncompleted destination nodes, and break out if
        # all of them have been accounted for
        if node in destination_cities:
            destination_cities_remaining.remove(node)
            if len(destination_cities_remaining) == 0:
                break

    # find all paths that made it all the way to the destination city
    paths = []
    for cur_destination_city in destination_cities:
        if cur_destination_city in complete:
            entry = complete[cur_destination_city]
            paths.append(entry)

    # if no paths made it all the way, there is no path at all; return None
    if len(paths) == 0:
        return None

    # otherwise, find the smallest cost of all paths that made it
    min_path_and_cost = min(paths, key=lambda x: x[0])
    min_path_flight_objects = min_path_and_cost[1]
    min_path = [x.number for x in min_path_flight_objects]
    return min_path

#
# Here is a fictious flight schedule that is roughly based on routes
# flown by Skipper, a regional airline in Australia
# (http://www.skippers.com.au/).
#
# Each tuple contains six items:
#   Flight Number, Origin, Destination, Departure Time, Arrival Time, Cost
# (Don't worry about any time zone issues; assume everything happens
# in the same time zone)
# Also note that overnight layovers are not allowed.
#
all_flights = [(523, 'Broome', 'Derby', '07:17', '08:57', 60),
               (526, 'Broome', 'Derby', '08:41', '10:30', 50),
               (527, 'Broome', 'Derby', '11:46', '13:24', 200),
               (530, 'Broome', 'Derby', '14:23', '15:59', 50),
               (540, 'Broome', 'Derby', '17:49', '19:40', 50),
               (546, 'Broome', 'Derby', '20:34', '22:09', 20),
               (547, 'Broome', 'Perth', '06:41', '08:44', 30),
               (549, 'Broome', 'Perth', '17:16', '19:18', 100),
               (559, 'Carnarvon', 'Geraldton', '09:05', '10:57', 50),
               (561, 'Carnarvon', 'Geraldton', '11:14', '13:03', 30),
               (578, 'Carnarvon', 'Geraldton', '14:56', '16:48', 150),
               (582, 'Carnarvon', 'Geraldton', '17:05', '18:46', 50),
               (598, 'Carnarvon', 'Geraldton', '22:08', '23:49', 20),
               (599, 'Carnarvon', 'Perth', '07:04', '09:46', 200),
               (100, 'Carnarvon', 'Perth', '10:53', '13:38', 60),
               (604, 'Carnarvon', 'Perth', '14:50', '17:16', 200),
               (612, 'Carnarvon', 'Perth', '19:54', '22:38', 50),
               (107, 'Derby', 'Broome', '08:44', '10:36', 160),
               (108, 'Derby', 'Broome', '21:18', '23:04', 30),
               (622, 'Derby', 'Fitzroy Crossing', '13:59', '15:04', 60),
               (112, 'Derby', 'Fitzroy Crossing', '19:24', '20:15', 60),
               (113, 'Derby', 'Geraldton', '07:00', '08:10', 20),
               (115, 'Derby', 'Geraldton', '10:00', '11:07', 200),
               (118, 'Derby', 'Geraldton', '13:24', '14:31', 50),
               (121, 'Derby', 'Geraldton', '14:41', '15:52', 50),
               (122, 'Derby', 'Geraldton', '17:05', '18:09', 60),
               (635, 'Derby', 'Geraldton', '18:59', '20:18', 60),
               (638, 'Fitzroy Crossing', 'Derby', '09:18', '10:08', 50),
               (131, 'Fitzroy Crossing', 'Derby', '13:59', '14:51', 160),
               (226, 'Fitzroy Crossing', 'Derby', '14:34', '15:34', 110),
               (139, 'Fitzroy Crossing', 'Derby', '18:43', '19:36', 50),
               (654, 'Fitzroy Crossing', 'Halls Creek', '07:55', '09:48', 180),
               (143, 'Fitzroy Crossing', 'Halls Creek', '09:45', '11:39', 20),
               (280, 'Fitzroy Crossing', 'Halls Creek', '15:10', '17:07', 110),
               (660, 'Fitzroy Crossing', 'Halls Creek', '18:41', '20:24', 30),
               (661, 'Fitzroy Crossing', 'Halls Creek', '20:35', '22:19', 200),
               (663, 'Geraldton', 'Carnarvon', '08:30', '10:24', 30),
               (152, 'Geraldton', 'Carnarvon', '12:52', '14:42', 50),
               (153, 'Geraldton', 'Carnarvon', '15:24', '17:15', 30),
               (154, 'Geraldton', 'Carnarvon', '18:07', '19:53', 180),
               (671, 'Geraldton', 'Derby', '06:01', '07:10', 120),
               (676, 'Geraldton', 'Derby', '10:46', '12:09', 20),
               (165, 'Geraldton', 'Derby', '11:29', '12:45', 30),
               (683, 'Geraldton', 'Derby', '14:17', '15:23', 50),
               (174, 'Geraldton', 'Derby', '16:45', '17:58', 180),
               (175, 'Geraldton', 'Derby', '18:31', '19:47', 20),
               (179, 'Halls Creek', 'Fitzroy Crossing', '06:32', '08:22', 200),
               (187, 'Halls Creek', 'Fitzroy Crossing', '13:19', '15:03', 200),
               (702, 'Halls Creek', 'Fitzroy Crossing', '14:04', '15:45', 20),
               (192, 'Halls Creek', 'Fitzroy Crossing', '20:08', '21:59', 160),
               (195, 'Halls Creek', 'Kalbarri', '06:43', '09:01', 110),
               (709, 'Halls Creek', 'Kalbarri', '08:45', '11:04', 200),
               (199, 'Halls Creek', 'Kalbarri', '13:21', '15:39', 20),
               (209, 'Halls Creek', 'Kalbarri', '15:45', '18:01', 100),
               (723, 'Halls Creek', 'Kalbarri', '16:04', '18:10', 50),
               (724, 'Halls Creek', 'Kalbarri', '19:52', '22:07', 160),
               (216, 'Kalbarri', 'Halls Creek', '06:15', '08:34', 100),
               (217, 'Kalbarri', 'Halls Creek', '14:57', '17:14', 200),
               (730, 'Kalbarri', 'Halls Creek', '21:05', '23:24', 20),
               (731, 'Kalbarri', 'Perth', '06:18', '08:50', 50),
               (734, 'Kalbarri', 'Perth', '12:23', '14:59', 120),
               (735, 'Kalbarri', 'Perth', '12:59', '15:19', 30),
               (738, 'Kalbarri', 'Perth', '18:41', '21:10', 60),
               (739, 'Kalbarri', 'Perth', '19:42', '22:18', 60),
               (740, 'Laverton', 'Leonora', '07:39', '08:53', 180),
               (745, 'Laverton', 'Leonora', '12:20', '13:32', 20),
               (748, 'Laverton', 'Leonora', '13:44', '15:08', 30),
               (751, 'Laverton', 'Leonora', '18:00', '19:11', 200),
               (240, 'Laverton', 'Leonora', '20:34', '21:40', 110),
               (754, 'Laverton', 'Perth', '07:21', '08:21', 180),
               (247, 'Laverton', 'Perth', '20:11', '21:22', 160),
               (248, 'Leinster', 'Perth', '08:37', '11:16', 180),
               (249, 'Leinster', 'Perth', '13:44', '16:12', 110),
               (763, 'Leinster', 'Perth', '16:29', '19:06', 160),
               (765, 'Leinster', 'Perth', '19:17', '21:47', 20),
               (981, 'Leinster', 'Wiluna', '10:51', '13:03', 200),
               (770, 'Leinster', 'Wiluna', '16:02', '18:17', 50),
               (259, 'Leinster', 'Wiluna', '19:44', '22:09', 60),
               (772, 'Leonora', 'Laverton', '10:39', '11:59', 110),
               (987, 'Leonora', 'Laverton', '15:56', '17:13', 110),
               (264, 'Leonora', 'Laverton', '21:39', '22:48', 200),
               (779, 'Leonora', 'Perth', '10:29', '11:59', 50),
               (780, 'Leonora', 'Perth', '11:26', '12:58', 50),
               (783, 'Leonora', 'Perth', '19:48', '21:25', 30),
               (278, 'Meekatharra', 'Mt Magnet', '07:40', '08:42', 60),
               (792, 'Meekatharra', 'Mt Magnet', '08:35', '09:35', 60),
               (793, 'Meekatharra', 'Mt Magnet', '11:50', '12:44', 110),
               (796, 'Meekatharra', 'Mt Magnet', '14:32', '15:26', 30),
               (798, 'Meekatharra', 'Mt Magnet', '16:56', '17:52', 160),
               (288, 'Meekatharra', 'Mt Magnet', '19:38', '20:27', 60),
               (289, 'Meekatharra', 'Perth', '08:12', '09:28', 50),
               (803, 'Meekatharra', 'Perth', '09:12', '10:25', 30),
               (805, 'Meekatharra', 'Perth', '12:10', '13:16', 50),
               (298, 'Meekatharra', 'Perth', '13:33', '14:40', 50),
               (391, 'Meekatharra', 'Perth', '16:45', '17:50', 30),
               (815, 'Meekatharra', 'Perth', '20:17', '21:29', 110),
               (817, 'Monkey Mia', 'Perth', '08:26', '10:51', 20),
               (393, 'Monkey Mia', 'Perth', '13:12', '15:51', 30),
               (825, 'Monkey Mia', 'Perth', '21:01', '23:37', 180),
               (314, 'Mt Magnet', 'Meekatharra', '06:29', '07:30', 30),
               (827, 'Mt Magnet', 'Meekatharra', '08:56', '10:00', 50),
               (829, 'Mt Magnet', 'Meekatharra', '13:09', '14:14', 30),
               (832, 'Mt Magnet', 'Meekatharra', '14:10', '15:09', 30),
               (833, 'Mt Magnet', 'Meekatharra', '17:39', '18:41', 180),
               (322, 'Mt Magnet', 'Meekatharra', '19:51', '20:55', 160),
               (333, 'Mt Magnet', 'Perth', '07:53', '08:38', 120),
               (846, 'Mt Magnet', 'Perth', '15:45', '16:29', 20),
               (967, 'Mt Magnet', 'Perth', '18:04', '18:49', 20),
               (336, 'Mt Magnet', 'Wiluna', '07:34', '09:08', 200),
               (338, 'Mt Magnet', 'Wiluna', '13:35', '15:17', 30),
               (856, 'Mt Magnet', 'Wiluna', '14:54', '16:27', 50),
               (345, 'Mt Magnet', 'Wiluna', '18:03', '19:35', 50),
               (859, 'Perth', 'Broome', '07:21', '09:14', 50),
               (348, 'Perth', 'Broome', '10:37', '12:46', 60),
               (349, 'Perth', 'Broome', '12:56', '14:57', 20),
               (350, 'Perth', 'Broome', '15:01', '17:11', 110),
               (356, 'Perth', 'Broome', '18:03', '20:03', 60),
               (364, 'Perth', 'Broome', '18:45', '20:54', 150),
               (880, 'Perth', 'Carnarvon', '07:39', '10:09', 50),
               (884, 'Perth', 'Carnarvon', '10:33', '13:11', 30),
               (374, 'Perth', 'Carnarvon', '12:04', '14:31', 50),
               (375, 'Perth', 'Carnarvon', '13:59', '16:32', 30),
               (378, 'Perth', 'Carnarvon', '17:04', '19:38', 50),
               (299, 'Perth', 'Carnarvon', '19:27', '22:09', 50),
               (383, 'Perth', 'Kalbarri', '06:41', '09:12', 120),
               (384, 'Perth', 'Kalbarri', '12:42', '15:03', 20),
               (898, 'Perth', 'Kalbarri', '19:13', '21:38', 30),
               (390, 'Perth', 'Laverton', '10:20', '11:23', 60),
               (321, 'Perth', 'Laverton', '14:08', '15:03', 60),
               (905, 'Perth', 'Laverton', '19:58', '20:53', 100),
               (395, 'Perth', 'Leinster', '06:59', '09:28', 200),
               (396, 'Perth', 'Leinster', '10:17', '12:48', 100),
               (401, 'Perth', 'Leinster', '14:24', '16:50', 50),
               (914, 'Perth', 'Leinster', '18:54', '21:34', 160),
               (404, 'Perth', 'Leonora', '11:03', '12:40', 30),
               (918, 'Perth', 'Leonora', '12:37', '14:17', 150),
               (408, 'Perth', 'Leonora', '20:42', '22:10', 100),
               (923, 'Perth', 'Meekatharra', '06:21', '07:35', 110),
               (927, 'Perth', 'Meekatharra', '10:25', '11:26', 20),
               (933, 'Perth', 'Meekatharra', '14:27', '15:24', 50),
               (934, 'Perth', 'Meekatharra', '17:49', '18:50', 200),
               (941, 'Perth', 'Meekatharra', '21:56', '23:08', 30),
               (430, 'Perth', 'Monkey Mia', '06:18', '08:48', 30),
               (943, 'Perth', 'Monkey Mia', '12:11', '14:48', 180),
               (432, 'Perth', 'Monkey Mia', '17:32', '20:13', 50),
               (433, 'Perth', 'Monkey Mia', '19:48', '22:23', 100),
               (947, 'Perth', 'Mt Magnet', '06:43', '07:23', 100),
               (948, 'Perth', 'Mt Magnet', '13:59', '14:54', 20),
               (954, 'Perth', 'Mt Magnet', '15:44', '16:26', 120),
               (955, 'Perth', 'Mt Magnet', '19:34', '20:26', 200),
               (475, 'Perth', 'Wiluna', '07:34', '09:57', 60),
               (959, 'Perth', 'Wiluna', '09:44', '12:22', 50),
               (455, 'Perth', 'Wiluna', '12:22', '14:45', 60),
               (969, 'Perth', 'Wiluna', '14:26', '16:59', 50),
               (458, 'Perth', 'Wiluna', '17:19', '19:38', 60),
               (459, 'Perth', 'Wiluna', '19:09', '21:35', 30),
               (461, 'Wiluna', 'Leinster', '07:54', '10:16', 20),
               (462, 'Wiluna', 'Leinster', '08:35', '10:50', 200),
               (463, 'Wiluna', 'Leinster', '11:50', '14:01', 200),
               (976, 'Wiluna', 'Leinster', '13:54', '16:15', 50),
               (469, 'Wiluna', 'Leinster', '17:24', '19:43', 30),
               (984, 'Wiluna', 'Leinster', '19:58', '22:13', 200),
               (847, 'Wiluna', 'Mt Magnet', '07:13', '08:42', 30),
               (478, 'Wiluna', 'Mt Magnet', '11:48', '13:14', 50),
               (993, 'Wiluna', 'Mt Magnet', '13:00', '14:27', 20),
               (483, 'Wiluna', 'Mt Magnet', '17:20', '18:57', 60),
               (422, 'Wiluna', 'Mt Magnet', '21:40', '23:21', 60),
               (494, 'Wiluna', 'Perth', '08:28', '11:07', 160),
               (253, 'Wiluna', 'Perth', '11:17', '13:41', 150),
               (498, 'Wiluna', 'Perth', '13:53', '16:13', 60),
               (501, 'Wiluna', 'Perth', '17:59', '20:27', 20),
               (505, 'Wiluna', 'Perth', '20:21', '22:41', 180)]

import unittest

class ProvidedTests(unittest.TestCase):

    def test_MtMagnet_to_FitzroyCrossing(self):
        retval = find_best_flights(all_flights, 'Mt Magnet', 'Fitzroy Crossing')
        self.assertListEquals(retval, [314, 803, 348, 530, 112])

    def test_Leonora_to_FitzroyCrossing(self):
        retval = find_best_flights(all_flights, 'Leonora', 'Fitzroy Crossing')
        self.assertIsNone(retval)

    def test_Meekatharra_to_Wiluna(self):
        retval = find_best_flights(all_flights, 'Meekatharra', 'Wiluna')
        self.assertListEqual(retval, [391, 459])

class Test_parse_time_str(unittest.TestCase):

    def test_0000(self):
        self.assertEqual(parse_time_str("00:00"), 0)

    def test_0001(self):
        self.assertEqual(parse_time_str("00:01"), 1)

    def test_0015(self):
        self.assertEqual(parse_time_str("00:15"), 15)

    def test_0100(self):
        self.assertEqual(parse_time_str("01:00"), 60)

    def test_0105(self):
        self.assertEqual(parse_time_str("01:05"), 65)

    def test_0126(self):
        self.assertEqual(parse_time_str("01:26"), 86)

    def test_0526(self):
        self.assertEqual(parse_time_str("05:26"), 326)

    def test_2253(self):
        self.assertEqual(parse_time_str("22:53"), 1373)


class Test_flight_tuples_to_objects(unittest.TestCase):

    def test_EmptyList(self):
        x = flight_tuples_to_objects([])
        x = list(x)
        self.assertListEqual(x, [])

    def test_OneFlight(self):
        x = flight_tuples_to_objects([(455, 'Perth', 'Wiluna', '12:22', '14:45', 60)])
        flight = next(x)
        self.assertRaises(StopIteration, next, x)
        self.assertEqual(flight.number, 455)
        self.assertEqual(flight.depart_city, "Perth")
        self.assertEqual(flight.arrive_city, "Wiluna")
        self.assertEqual(flight.depart_time, 742)
        self.assertEqual(flight.arrive_time, 885)
        self.assertEqual(flight.cost, 60)

    def test_TwoFlights(self):
        x = flight_tuples_to_objects([
            (455, 'Perth', 'Wiluna', '12:22', '14:45', 60),
            (314, 'Mt Magnet', 'Meekatharra', '06:29', '07:30', 30),
        ])
        flight1 = next(x)
        flight2 = next(x)
        self.assertRaises(StopIteration, next, x)

        self.assertEqual(flight1.number, 455)
        self.assertEqual(flight1.depart_city, "Perth")
        self.assertEqual(flight1.arrive_city, "Wiluna")
        self.assertEqual(flight1.depart_time, 742)
        self.assertEqual(flight1.arrive_time, 885)
        self.assertEqual(flight1.cost, 60)

        self.assertEqual(flight2.number, 314)
        self.assertEqual(flight2.depart_city, "Mt Magnet")
        self.assertEqual(flight2.arrive_city, "Meekatharra")
        self.assertEqual(flight2.depart_time, 389)
        self.assertEqual(flight2.arrive_time, 450)
        self.assertEqual(flight2.cost, 30)

class Test_make_flight_graph(unittest.TestCase):

    def test_NoFlights(self):
        (G, cities) = make_flight_graph([])
        self.assertEqual(len(G), 0)
        self.assertEqual(len(cities), 0)

    def test_1Flight(self):
        flight = Flight(123, "A", "B", 20, 40, 100)
        (G, cities) = make_flight_graph([flight])

        self.assert_dict_keys(cities, ["A", "B"])
        self.assert_dict_keys(G, ["A", ("B", 40)])
        self.assertSetEqual(cities["A"], set())
        self.assertSetEqual(cities["B"], set([("B", 40)]))

        self.assert_dict_keys(G["A"], [("B", 40)])
        self.assertIs(G["A"][("B", 40)], flight)
        self.assert_dict_keys(G[("B", 40)], [])

    def test_2Flights_DisjointCities(self):
        flight1 = Flight(123, "A", "B", 20, 40, 100)
        flight2 = Flight(456, "C", "D", 60, 80, 200)
        (G, cities) = make_flight_graph([flight1, flight2])

        self.assert_dict_keys(cities, ["A", "B", "C", "D"])
        self.assert_dict_keys(G, ["A", ("B", 40), "C", ("D", 80)])
        self.assertSetEqual(cities["A"], set())
        self.assertSetEqual(cities["B"], set([("B", 40)]))

        self.assert_dict_keys(G["A"], [("B", 40)])
        self.assertIs(G["A"][("B", 40)], flight1)
        self.assert_dict_keys(G[("B", 40)], [])

        self.assert_dict_keys(G["C"], [("D", 80)])
        self.assertIs(G["C"][("D", 80)], flight2)
        self.assert_dict_keys(G[("D", 80)], [])

    def test_2Flights_SameDepartureCity_DifferentArrivalCities(self):
        flight1 = Flight(123, "A", "B", 20, 40, 100)
        flight2 = Flight(456, "A", "C", 60, 80, 200)
        (G, cities) = make_flight_graph([flight1, flight2])

        self.assert_dict_keys(cities, ["A", "B", "C"])
        self.assert_dict_keys(G, ["A", ("B", 40), ("C", 80)])
        self.assertSetEqual(cities["A"], set())
        self.assertSetEqual(cities["B"], set([("B", 40)]))
        self.assertSetEqual(cities["C"], set([("C", 80)]))

        self.assert_dict_keys(G["A"], [("B", 40), ("C", 80)])
        self.assertIs(G["A"][("B", 40)], flight1)
        self.assertIs(G["A"][("C", 80)], flight2)
        self.assert_dict_keys(G[("B", 40)], [])
        self.assert_dict_keys(G[("C", 80)], [])

    def test_2Flights_SameDepartureCity_SameArrivalCities_DifferentTimes(self):
        flight1 = Flight(123, "A", "B", 20, 40, 100)
        flight2 = Flight(456, "A", "B", 60, 80, 200)
        (G, cities) = make_flight_graph([flight1, flight2])

        self.assert_dict_keys(cities, ["A", "B"])
        self.assert_dict_keys(G, ["A", ("B", 40), ("B", 80)])
        self.assertSetEqual(cities["A"], set())
        self.assertSetEqual(cities["B"], set([("B", 40), ("B", 80)]))

        self.assert_dict_keys(G["A"], [("B", 40), ("B", 80)])
        self.assertIs(G["A"][("B", 40)], flight1)
        self.assertIs(G["A"][("B", 80)], flight2)
        self.assert_dict_keys(G[("B", 40)], [])
        self.assert_dict_keys(G[("B", 80)], [])

    def test_2Flights_SameDepartureCity_SameArrivalCities_SameTime_Flight1DollarCheaper(self):
        flight1 = Flight(123, "A", "B", 20, 80, 100)
        flight2 = Flight(456, "A", "B", 60, 80, 200)
        (G, cities) = make_flight_graph([flight1, flight2])

        self.assert_dict_keys(cities, ["A", "B"])
        self.assert_dict_keys(G, ["A", ("B", 80)])
        self.assertSetEqual(cities["A"], set())
        self.assertSetEqual(cities["B"], set([("B", 80)]))

        self.assert_dict_keys(G["A"], [("B", 80)])
        self.assertIs(G["A"][("B", 80)], flight1)
        self.assert_dict_keys(G[("B", 80)], [])

    def test_2Flights_SameDepartureCity_SameArrivalCities_SameTime_Flight1TimeCheaper(self):
        flight1 = Flight(123, "A", "B", 20, 80, 100)
        flight2 = Flight(456, "A", "B", 10, 80, 100)
        (G, cities) = make_flight_graph([flight1, flight2])

        self.assert_dict_keys(cities, ["A", "B"])
        self.assert_dict_keys(G, ["A", ("B", 80)])
        self.assertSetEqual(cities["A"], set())
        self.assertSetEqual(cities["B"], set([("B", 80)]))

        self.assert_dict_keys(G["A"], [("B", 80)])
        self.assertIs(G["A"][("B", 80)], flight1)
        self.assert_dict_keys(G[("B", 80)], [])

    def test_2Flights_SameDepartureCity_SameArrivalCities_SameTime_Flight2DollarCheaper(self):
        flight1 = Flight(123, "A", "B", 20, 80, 200)
        flight2 = Flight(456, "A", "B", 60, 80, 100)
        (G, cities) = make_flight_graph([flight1, flight2])

        self.assert_dict_keys(cities, ["A", "B"])
        self.assert_dict_keys(G, ["A", ("B", 80)])
        self.assertSetEqual(cities["A"], set())
        self.assertSetEqual(cities["B"], set([("B", 80)]))

        self.assert_dict_keys(G["A"], [("B", 80)])
        self.assertIs(G["A"][("B", 80)], flight2)
        self.assert_dict_keys(G[("B", 80)], [])

    def test_2Flights_SameDepartureCity_SameArrivalCities_SameTime_Flight2TimeCheaper(self):
        flight1 = Flight(123, "A", "B", 20, 80, 100)
        flight2 = Flight(456, "A", "B", 60, 80, 100)
        (G, cities) = make_flight_graph([flight1, flight2])

        self.assert_dict_keys(cities, ["A", "B"])
        self.assert_dict_keys(G, ["A", ("B", 80)])
        self.assertSetEqual(cities["A"], set())
        self.assertSetEqual(cities["B"], set([("B", 80)]))

        self.assert_dict_keys(G["A"], [("B", 80)])
        self.assertIs(G["A"][("B", 80)], flight2)
        self.assert_dict_keys(G[("B", 80)], [])

    def test_2Flights_Chain_Flight2LeavesLateEnoughToCatch(self):
        flight1 = Flight(123, "A", "B", 20, 40, 100)
        flight2 = Flight(456, "B", "C", 60, 80, 200)
        (G, cities) = make_flight_graph([flight1, flight2])

        self.assert_dict_keys(cities, ["A", "B", "C"])
        self.assert_dict_keys(G, ["A", "B", ("B", 40), ("C", 80)])
        self.assertSetEqual(cities["A"], set())
        self.assertSetEqual(cities["B"], set([("B", 40)]))
        self.assertSetEqual(cities["C"], set([("C", 80)]))

        self.assert_dict_keys(G["A"], [("B", 40)])
        self.assertIs(G["A"][("B", 40)], flight1)
        self.assert_dict_keys(G[("B", 40)], [("C", 80)])
        self.assertIs(G[("B", 40)][("C", 80)], flight2)
        self.assert_dict_keys(G[("C", 80)], [])

    def test_2Flights_Chain_Flight2LeavesTooEarlyToCatch(self):
        flight1 = Flight(123, "A", "B", 20, 40, 100)
        flight2 = Flight(456, "B", "C", 39, 80, 200)
        (G, cities) = make_flight_graph([flight1, flight2])

        self.assert_dict_keys(cities, ["A", "B", "C"])
        self.assert_dict_keys(G, ["A", "B", ("B", 40), ("C", 80)])
        self.assertSetEqual(cities["A"], set())
        self.assertSetEqual(cities["B"], set([("B", 40)]))
        self.assertSetEqual(cities["C"], set([("C", 80)]))

        self.assert_dict_keys(G["A"], [("B", 40)])
        self.assertIs(G["A"][("B", 40)], flight1)
        self.assert_dict_keys(G[("B", 40)], [])
        self.assert_dict_keys(G[("C", 80)], [])

    def test_3Flights_Diamond(self):
        flight1 = Flight(123, "A", "B", 20, 40, 100)
        flight2 = Flight(456, "A", "B", 60, 80, 200)
        flight3 = Flight(789, "B", "C", 70, 90, 300)
        (G, cities) = make_flight_graph([flight1, flight2, flight3])

        self.assert_dict_keys(cities, ["A", "B", "C"])
        self.assert_dict_keys(G, ["A", "B", ("B", 40), ("B", 80), ("C", 90)])
        self.assertSetEqual(cities["A"], set())
        self.assertSetEqual(cities["B"], set([("B", 40), ("B", 80)]))
        self.assertSetEqual(cities["C"], set([("C", 90)]))

        self.assert_dict_keys(G["A"], [("B", 40), ("B", 80)])
        self.assertIs(G["A"][("B", 40)], flight1)
        self.assertIs(G["A"][("B", 80)], flight2)
        self.assert_dict_keys(G[("B", 40)], [("C", 90)])
        self.assert_dict_keys(G[("B", 80)], [])
        self.assert_dict_keys(G[("C", 90)], [])

    def assert_dict_keys(self, d, expected_keys):
        actual_keys_set = set(d.viewkeys())
        expected_keys_set = set(expected_keys)
        self.assertSetEqual(actual_keys_set, expected_keys_set)
