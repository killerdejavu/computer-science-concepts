import hashlib

from faker import Faker

from base_benchmark import BaseBenchmark

fake = Faker()


class ModuloHashingBenchmark(BaseBenchmark):

    def find_node_for_key(self, key):
        node_number = int(hashlib.sha256(str(key)).hexdigest(), 16) % len(self.nodes)
        return self.nodes[node_number]
