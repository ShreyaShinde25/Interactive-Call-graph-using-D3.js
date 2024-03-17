import argparse
import json
import os
from collections import deque
from collections import defaultdict
import const
import util

def get_method_signature(method_data):
    return f"{method_data['className']}.{method_data['methodName']}{method_data['methodDescriptor']}"

def gen_stats(data, file_name, save_to_disk=True):
    METHODS = {m['id']: m for m in data['methods']}
    paths = data['paths']
    ALL_METHOD_FREQ = defaultdict(int) # keep track of all methods
    EXEC_TYPE_FREQ = defaultdict(int)
    ALL_INVOKE_FREQ = defaultdict(int) # keep track of all invocations
    DEFAULT_INVOKE_FREQ = defaultdict(int) # keep track of only default-default invocations
    ROOT_FREQ = defaultdict(int)
    LAMBDA_FREQ = defaultdict(int) # keep track of only lambda methods
    REFLECT_METHOD_FREQ = defaultdict(int) # keep track of only reflection generated methods
    DEFAULT_METHOD_FREQ = defaultdict(int) # keep track of only default methods
    for root in paths:
        q = deque()
        q.append(root)
        ROOT_FREQ[root["id"]] += 1
        while q:
            n = len(q)
            for _ in range(n):
                entry = q.popleft()
                method_data = METHODS[entry["id"]]
                method_signature = get_method_signature(method_data)
                # count lambda methods separately
                if "$$Lambda$" in method_signature: 
                    LAMBDA_FREQ[method_signature] += 1
                # count reflection generated methods separately
                elif "jdk.internal.reflect.Generated" in method_signature: 
                    REFLECT_METHOD_FREQ[method_signature] += 1
                # count default methods 
                else:
                    DEFAULT_METHOD_FREQ[method_signature] += 1
                # count total methods 
                ALL_METHOD_FREQ[method_signature] += 1
                EXEC_TYPE_FREQ[entry["execType"]] += 1
                for child in entry["children"]:
                    q.append(child)
                    child_method_data = METHODS[child["id"]]
                    child_method_signature = get_method_signature(child_method_data)
                    edge_id = f"{method_signature}->{child_method_signature}:{child['callSite']}"
                    # edge_id = f"{method_signature}->{child_method_signature}"
                    if "$$Lambda$" in method_signature or "$$Lambda$" in child_method_signature: 
                        pass
                    elif "jdk.internal.reflect.Generated" in method_signature \
                        or "jdk.internal.reflect.Generated" in child_method_signature: 
                        pass
                    else:
                        DEFAULT_INVOKE_FREQ[edge_id] += 1
                    ALL_INVOKE_FREQ[edge_id] += 1
    stats = {
        const.STATS_KEY_ROOTS: util.sort_dict(ROOT_FREQ),
        const.STATS_KEY_EXEC_TYPES: util.sort_dict(EXEC_TYPE_FREQ),

        const.STATS_KEY_ALL_METHODS: util.sort_dict(ALL_METHOD_FREQ), 
        const.STATS_KEY_DEFAULT_METHODS: util.sort_dict(DEFAULT_METHOD_FREQ),
        const.STATS_KEY_LAMBDA_METHODS: util.sort_dict(LAMBDA_FREQ),
        const.STATS_KEY_REFLECT_METHODS: util.sort_dict(REFLECT_METHOD_FREQ),
        const.STATS_KEY_ALL_METHOD_COUNT: len(ALL_METHOD_FREQ),
        const.STATS_KEY_DEFAULT_METHOD_COUNT: len(DEFAULT_METHOD_FREQ),
        const.STATS_KEY_LAMBDA_METHOD_COUNT: len(LAMBDA_FREQ),
        const.STATS_KEY_REFLECT_METHOD_COUNT: len(REFLECT_METHOD_FREQ),
        const.STATS_KEY_ALL_METHOD_FREQ_SUM: sum(ALL_METHOD_FREQ.values()),
        const.STATS_KEY_DEFAULT_METHODS_FREQ_SUM: sum(DEFAULT_METHOD_FREQ.values()),
        const.STATS_KEY_LAMBDA_MEHTOD_FREQ_SUM: sum(LAMBDA_FREQ.values()),
        const.STATS_KEY_REFLECT_METHOD_FREQ_SUM: sum(REFLECT_METHOD_FREQ.values()),
        const.STATS_KEY_ALL_METHOD_FREQ_DISTRIB: util.distrib_by_upper_bounds(ALL_METHOD_FREQ, const.DISTRIB_BOUNDS),
        const.STATS_KEY_DEFAULT_METHOD_FREQ_DISTRIB: util.distrib_by_upper_bounds(DEFAULT_METHOD_FREQ, const.DISTRIB_BOUNDS),
        
        const.STATS_KEY_ALL_INVOKES: util.sort_dict(ALL_INVOKE_FREQ), 
        const.STATS_KEY_DEFAULT_INVOKES: util.sort_dict(DEFAULT_INVOKE_FREQ),
        const.STATS_KEY_ALL_INVOKE_COUNT: len(ALL_INVOKE_FREQ),
        const.STATS_KEY_DEFAULT_INVOKE_COUNT: len(DEFAULT_INVOKE_FREQ),
        const.STATS_KEY_ALL_INVOKE_FREQ_SUM: sum(ALL_INVOKE_FREQ.values()),
        const.STATS_KEY_DEFAULT_INVOKE_FREQ_SUM: sum(DEFAULT_INVOKE_FREQ.values()),
        const.STATS_KEY_ALL_INVOKE_FREQ_DISTRIB: util.distrib_by_upper_bounds(ALL_INVOKE_FREQ, const.DISTRIB_BOUNDS),
        const.STATS_KEY_DEFAULT_INVOKE_FREQ_DISTRIB: util.distrib_by_upper_bounds(DEFAULT_INVOKE_FREQ, const.DISTRIB_BOUNDS),
    }

    if save_to_disk:
        stats_json = f"{const.OUT_DIR}/stats_{file_name}.json"
        with open(stats_json, 'w') as f:
            json.dump(stats, f, indent=4)
    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script summarizing stats related to callers-callees from a single program run.')
    parser.add_argument('--input', '-i', type=str, required=True, help='path to input (.json) file to process with caller-callee data.')
    parser.add_argument('--output', '-o', type=str, default='', help='output (.json) file name which will stats from analysis.') 

    args = parser.parse_args()

    out_dir = const.OUT_DIR
    util.mkdir(const.OUT_DIR)

    file_name = {args.output}
    if args.output == '':
        file_name = args.input.split('/')[-1].split('.')[0]

    with open(args.input, 'r') as f:
        data = json.load(f)
    
    gen_stats(data, file_name=file_name, save_to_disk=True)

    




    


    