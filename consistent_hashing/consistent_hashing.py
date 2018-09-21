import bisect
import hashlib
import random

from faker import Faker

from base import base_benchmark
from base import logger

fake = Faker()

KEY_SPACE = 2 ** 64


class ConsistentHashingBenchmark(base_benchmark.BaseBenchmark):

    def __init__(self, number_of_nodes=15, cache_size=100):
        self.cache_size = cache_size
        self.ordered_node_locations, self.location_to_node_map = [], {}
        for i in range(number_of_nodes):
            self.add_node()

    def find_node_for_key(self, key):
        hexdigest = int(hashlib.sha256(str(key)).hexdigest(), 16) % KEY_SPACE
        node_index = bisect.bisect_right(self.ordered_node_locations, hexdigest) % len(
            self.ordered_node_locations)
        node_location_hash = self.ordered_node_locations[node_index]
        return self.location_to_node_map[node_location_hash]

    def add_node(self):
        node = self.create_node(cache_size=self.cache_size)
        node_location_hash = int(hashlib.sha256(str(node.ip)).hexdigest(), 16) % KEY_SPACE
        self.location_to_node_map[node_location_hash] = node

        bisect.insort_right(self.ordered_node_locations,
                            node_location_hash)
        log = logger.get_logger(self.add_node)
        log.info("Added a new node to the cluster, Total Nodes - {}, Node - {}, Order - {}".format(
            len(self.ordered_node_locations), node.name,
                 [self.location_to_node_map[i].name for i in self.ordered_node_locations]))

    def remove_node(self):
        index = random.randint(0, len(self.ordered_node_locations) - 1)
        location_hash = self.ordered_node_locations[index]
        self.ordered_node_locations.pop(index)
        node = self.location_to_node_map[location_hash]
        log = logger.get_logger(self.remove_node)
        log.info(
            "Removed a random node from the cluster, Total Nodes - {} Index - {} Node - {}, Order - {}".format(
                len(self.ordered_node_locations), index, node.name, [self.location_to_node_map[i].name for i in self.ordered_node_locations]))
        del node
