import math
from collections import Counter

from consistent_hashing import ConsistentHashingBenchmark
from base import logger
from collections import OrderedDict


def main(number_of_nodes=15, dataset_size=10 ** 5):
    log = logger.get_logger(main)
    log.info("Number of nodes - {}".format(number_of_nodes))
    log.info("Dataset Size - {}".format(dataset_size))

    mhb = ConsistentHashingBenchmark(number_of_nodes=number_of_nodes, cache_size=dataset_size)
    keys = range(0, dataset_size)

    init_benchmark_data(keys, mhb)
    check_cache_miss(keys, mhb)
    mhb.add_node()
    check_cache_miss(keys, mhb)
    check_cache_miss(keys, mhb)
    mhb.add_node()
    check_cache_miss(keys, mhb)
    mhb.remove_node()
    check_cache_miss(keys, mhb)
    check_cache_miss(keys, mhb)
    mhb.add_node()
    check_cache_miss(keys, mhb)
    check_cache_miss(keys, mhb)
    mhb.add_node()
    check_cache_miss(keys, mhb)
    mhb.remove_node()
    check_cache_miss(keys, mhb)
    check_cache_miss(keys, mhb)


def init_benchmark_data(keys, mhb):
    for key in keys:
        node = mhb.find_node_for_key(key=key)
        node.get_or_if_not_present_set(key=key)
    log = logger.get_logger(init_benchmark_data)
    log.warn("Creating Initial Benchmark Data Complete")


def check_cache_miss(keys, mhb):
    cnt = OrderedDict()
    log = logger.get_logger(check_cache_miss)
    was_not_cached_count = 0
    for key in keys:
        node = mhb.find_node_for_key(key=key)
        value, was_cached = node.get_or_if_not_present_set(key=key)
        if was_cached is False:
            if node.name not in cnt:
                cnt[node.name] = 1
            else:
                cnt[node.name] += 1
            was_not_cached_count += 1

    log.warn("Cache Miss % - {}".format(cnt))
    log.warn("Cache Miss % - {}".format(was_not_cached_count * 100.0 / len(keys)))


if __name__ == '__main__':
    main()
