import bisect
import hashlib
import random
from collections import Counter

from faker import Faker

from base import base_benchmark
from base import logger

fake = Faker()

KEY_SPACE = 2 ** 256


class ConsistentHashingBenchmark(base_benchmark.BaseBenchmark):

    def __init__(self, number_of_nodes=15, cache_size=100, number_of_virtual_nodes=1):
        self.cache_size = cache_size
        self.number_of_virtual_nodes = number_of_virtual_nodes
        self.ordered_node_locations, self.location_to_node_map = [], {}
        for i in range(number_of_nodes):
            self.add_node()

    def calculate_distribution(self):
        cnt = Counter()
        for i in range(len(self.ordered_node_locations)):
            node_name = self.location_to_node_map[self.ordered_node_locations[i]].name
            space = self.ordered_node_locations[i] - self.ordered_node_locations[i - 1]
            if i == 0:
                space += KEY_SPACE
            distribution_perc = (space * 100.0) / KEY_SPACE
            cnt[node_name] += distribution_perc
        return cnt

    def find_node_for_key(self, key):
        hexdigest = long(hashlib.sha256(str(key)).hexdigest(), 16) % KEY_SPACE
        node_index = bisect.bisect_right(self.ordered_node_locations, hexdigest) % len(
            self.ordered_node_locations)
        node_location_hash = self.ordered_node_locations[node_index]
        return self.location_to_node_map[node_location_hash]

    def add_node(self):
        node = self.create_node(cache_size=self.cache_size)

        for i in range(self.number_of_virtual_nodes):
            node_location_hash = long(hashlib.sha256(str(node.ip + "virtual_node:" + str(i))).hexdigest(),
                                     16) % KEY_SPACE
            self.location_to_node_map[node_location_hash] = node

            # Populate node's virtual_node_locations list
            node.virtual_node_locations.append(node_location_hash)

            bisect.insort_right(self.ordered_node_locations,
                                node_location_hash)
        log = logger.get_logger(self.add_node)
        log.debug("ADDED NODE - {}".format(node.name))
        log.debug("ORDER - {}".format([self.location_to_node_map[i].name for i in self.ordered_node_locations]))
        log.debug("KEY-SPACE DISTRIBUTION - {}".format(self.calculate_distribution()))
        log.debug("CACHE FILL(%) - {}".format([(n.name, len(n.cache)*100.0/n.cache_size) for n in set(self.location_to_node_map.values())]))

    def remove_node(self):
        index = random.randint(0, len(self.ordered_node_locations) - 1)
        location_hash = self.ordered_node_locations[index]
        node = self.location_to_node_map[location_hash]

        # Remove all virtual node's locations from list and remove all virtual node mappings to
        #  node from dict
        for virtual_location in node.virtual_node_locations:
            self.ordered_node_locations.remove(virtual_location)
            del self.location_to_node_map[virtual_location]

        log = logger.get_logger(self.remove_node)
        log.error("REMOVED NODE - {}".format(node.name))
        log.error("ORDER - {}".format([self.location_to_node_map[i].name for i in self.ordered_node_locations]))
        log.error("KEY-SPACE DISTRIBUTION - {}".format(self.calculate_distribution()))
        log.error("CACHE FILL(%) - {}".format([(n.name, len(n.cache)*100.0/n.cache_size) for n in set(self.location_to_node_map.values())]))