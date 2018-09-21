from faker import Faker

from base import logger
from node import Node
import random
fake = Faker()


class BaseBenchmark(object):

    def __init__(self, number_of_nodes=5, cache_size=100):
        self.cache_size = cache_size
        self.nodes = [self.create_node(cache_size=cache_size) for _ in range(number_of_nodes)]


    def create_node(self, cache_size):
        node = Node(name=fake.user_name(), ip=fake.ipv4(), cache_size=cache_size)
        log = logger.get_logger(self.create_node)
        log.info("Created a new node, Name - {}, IP - {}".format(node.name, node.ip))
        return node

    def add_node(self):
        self.nodes.append(self.create_node(cache_size=self.cache_size))
        log = logger.get_logger(self.add_node)
        log.info("Added a new node to the cluster, Total Nodes - {}".format(len(self.nodes)))

    def remove_node(self):
        index = random.randint(0, len(self.nodes) - 1)
        self.nodes.pop(index)
        log = logger.get_logger(self.remove_node)
        log.info("Removed a random node from the cluster, Total Nodes - {} Index - {}".format(len(self.nodes), index))
