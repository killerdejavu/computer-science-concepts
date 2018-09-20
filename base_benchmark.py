import random

from faker import Faker

from modulo_hashing import logger
from node import Node

fake = Faker()


class BaseBenchmark(object):

    def __init__(self, number_of_nodes=5):
        self.nodes = [self.create_node() for _ in range(number_of_nodes)]

    def create_node(self):
        node = Node(name=fake.user_name(), ip=fake.ipv4())
        log = logger.get_logger(self.create_node)
        log.info("Created a new node, Name - {}, IP - {}".format(node.name, node.ip))
        return node

    def add_node(self):
        self.nodes.append(self.create_node())
        log = logger.get_logger(self.add_node)
        log.info("Added a new node to the cluster, Total Nodes - {}".format(len(self.nodes)))

    def remove_node(self):
        self.nodes.pop(random.randint(0, len(self.nodes) - 1))
        log = logger.get_logger(self.remove_node)
        log.info("Removed a random node from the cluster, Total Nodes - {}".format(len(self.nodes)))
