import math

from modulo_hashing import ModuloHashingBenchmark
from base import logger


def main(number_of_nodes=15, dataset_size=10**5):

    log = logger.get_logger(main)
    log.info("Number of nodes - {}".format(number_of_nodes))
    log.info("Dataset Size - {}".format(dataset_size))

    mhb = ModuloHashingBenchmark(number_of_nodes=number_of_nodes, cache_size=int(math.ceil(dataset_size/(number_of_nodes-1))))
    keys = range(0, dataset_size)

    init_benchmark_data(keys, mhb)
    check_cache_miss(keys, mhb)
    mhb.add_node()
    check_cache_miss(keys, mhb)
    mhb.remove_node()
    check_cache_miss(keys, mhb)
    mhb.add_node()
    check_cache_miss(keys, mhb)
    mhb.remove_node()
    check_cache_miss(keys, mhb)
    mhb.add_node()
    check_cache_miss(keys, mhb)
    mhb.remove_node()
    check_cache_miss(keys, mhb)
    mhb.add_node()
    check_cache_miss(keys, mhb)
    mhb.remove_node()
    check_cache_miss(keys, mhb)


def init_benchmark_data(keys, mhb):
    for key in keys:
        node = mhb.find_node_for_key(key=key)
        node.get_or_if_not_present_set(key=key)
    log = logger.get_logger(init_benchmark_data)
    log.info("Creating Initial Benchmark Data Complete")


def check_cache_miss(keys, mhb):

    was_not_cached_count = 0
    for key in keys:
        node = mhb.find_node_for_key(key=key)
        value, was_cached = node.get_or_if_not_present_set(key=key)
        if was_cached is False:
            was_not_cached_count += 1

    log = logger.get_logger(check_cache_miss)
    log.info("Cache Miss % - {}".format(was_not_cached_count * 100.0 / len(keys)))


if __name__ == '__main__':
    main()
