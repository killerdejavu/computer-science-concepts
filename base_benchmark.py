import random

from faker import Faker

from node import Node

fake = Faker()


class BaseBenchmark(object):

    def __init__(self, number_of_nodes=5):
        self.nodes = [self.create_node() for _ in range(number_of_nodes)]

    @staticmethod
    def create_node():
        return Node(name=fake.user_name(), ip=fake.ipv4())

    def add_node(self):
        self.nodes.append(self.create_node())

    def remove_node(self):
        self.nodes.pop(random.randint(0, len(self.nodes) - 1))
