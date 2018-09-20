import random


class Node(object):

    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.cache = dict()

    def __repr__(self):
        return "{} - {} - {}".format(self.name, self.ip, self.cache)

    def _add_value(self, key):
        self.cache[key] = self._get_random_value()

    @staticmethod
    def _get_random_value():
        return random.randint(1, 10 ** 7)

    def _get_value(self, key):
        return self.cache.get(key)

    def get_or_if_not_present_set(self, key):
        if key in self.cache:
            return self.cache[key], True
        else:
            self._add_value(key=key)
            return self._get_value(key=key), False
