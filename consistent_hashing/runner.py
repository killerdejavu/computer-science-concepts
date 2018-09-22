import math
from collections import Counter

from consistent_hashing import ConsistentHashingBenchmark
from base import logger
from collections import OrderedDict


def main(number_of_nodes=15, dataset_size=10 ** 5, number_of_virtual_nodes=1):
    log = logger.get_logger(main)
    log.info("NUMBER OF NODES: {}".format(number_of_nodes))
    log.info("DATASET SIZE: {}".format(dataset_size))
    log.info("NUMBER OF VIRTUAL NODES: {}".format(number_of_virtual_nodes))
    log.info("NUMBER OF TOTAL NODES: {} * {} = {}".format(number_of_nodes, number_of_virtual_nodes, number_of_nodes*number_of_virtual_nodes))

    mhb = ConsistentHashingBenchmark(number_of_nodes=number_of_nodes, cache_size=int(math.ceil(dataset_size/(number_of_nodes-1))), number_of_virtual_nodes=number_of_virtual_nodes)
    keys = range(0, dataset_size)

    init_benchmark_data(keys, mhb)
    cnt = check_cache_miss(keys, mhb)
    mhb.add_node()
    cnt = check_cache_miss(keys, mhb, cnt)
    mhb.remove_node()
    cnt = check_cache_miss(keys, mhb, cnt)
    mhb.add_node()
    cnt = check_cache_miss(keys, mhb, cnt)
    mhb.remove_node()
    cnt = check_cache_miss(keys, mhb, cnt)
    mhb.add_node()
    cnt = check_cache_miss(keys, mhb, cnt)
    mhb.remove_node()
    cnt = check_cache_miss(keys, mhb, cnt)
    mhb.add_node()
    cnt = check_cache_miss(keys, mhb, cnt)
    mhb.remove_node()
    cnt = check_cache_miss(keys, mhb, cnt)


def init_benchmark_data(keys, mhb):
    for key in keys:
        node = mhb.find_node_for_key(key=key)
        node.get_or_if_not_present_set(key=key)
    log = logger.get_logger(init_benchmark_data)
    log.warn("CREATING INITIAL BENCHMARK DATA COMPLETE")


def check_cache_miss(keys, mhb, before=None):
    before = Counter() if before is None else before
    before_keys = before.keys()

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

    after = mhb.calculate_distribution()
    after_keys = after.keys()

    out = []

    for before_key in before_keys:
        if before_key not in after_keys:
            out.append("REMOVE {} -{}".format(before_key, before[before_key]))
    for after_key in after_keys:
        if after_key in before_keys and before[after_key] != after[after_key]:
            out.append("CHANGE {} {}".format(after_key, after[after_key] - before[after_key]))
        if after_key not in before_keys:
            out.append("ADD {} +{}".format(after_key, after[after_key]))

    log.warn("CACHE TRANSFER(%) -> {} => {}".format(was_not_cached_count * 100.0 / len(keys), out))
    return after

if __name__ == '__main__':
    main()
