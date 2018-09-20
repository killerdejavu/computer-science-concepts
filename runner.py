from modulo_hashing import ModuloHashingBenchmark
from collections import Counter


def main():
    number_of_nodes = 15
    dataset_size = 100000

    mhb = ModuloHashingBenchmark(number_of_nodes=number_of_nodes)
    keys = range(0, dataset_size)

    init_benchmark_data(keys, mhb)
    check_cache_miss(keys, mhb)
    mhb.add_node()
    check_cache_miss(keys, mhb)


def init_benchmark_data(keys, mhb):
    for key in keys:
        node = mhb.find_node_for_key(key=key)
        node.get_or_if_not_present_set(key=key)


def check_cache_miss(keys, mhb):
    was_not_cached_count = 0
    for key in keys:
        node = mhb.find_node_for_key(key=key)
        value, was_cached = node.get_or_if_not_present_set(key=key)
        if was_cached is False:
            was_not_cached_count += 1
    print "Cache Miss % - {}".format(was_not_cached_count * 100.0 / len(keys))


if __name__ == '__main__':
    main()
