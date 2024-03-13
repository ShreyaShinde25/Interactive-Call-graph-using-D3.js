import argparse
import json
import os
from collections import deque
from collections import defaultdict
import consts

def get_method_signature(method_data):
    return f"{method_data['className']}.{method_data['methodName']}.{method_data['methodDescriptor']}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script summarizing stats related to callers-callees from a single program run.')
    parser.add_argument('--input', '-i', type=str, required=True, help='path to input (.json) file to process with caller-callee data.')
    parser.add_argument('--output', '-o', type=str, default='', help='output (.json) file name which will stats from analysis.') 

    args = parser.parse_args()

    out_dir = 'out'
    if os.path.isdir(out_dir) == False:
        os.mkdir(out_dir) 
    stats_json = f"{out_dir}/{args.output}"
    if args.output == '':
        file_name = args.input.split('/')[-1].split('.')[0]
        stats_json = f"{out_dir}/{file_name}_stats.json"


    with open(args.input, 'r') as f:
        data = json.load(f)
    
    methods = data['methods']
    METHODS = {m['id']: m for m in data['methods']}
    paths = data['paths']
    METHOD_FREQ = defaultdict(int)
    EXEC_TYPE_FREQ = defaultdict(int)
    INVOKE_FREQ = defaultdict(int)
    ROOT_FREQ = defaultdict(int)
    LAMBDAS = defaultdict(int)
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
                if "$$Lambda$" in method_signature:
                    LAMBDAS[method_signature] += 1
                METHOD_FREQ[method_signature] += 1
                EXEC_TYPE_FREQ[entry["execType"]] += 1
                for child in entry["children"]:
                    q.append(child)
                    child_method_data = METHODS[child["id"]]
                    child_method_signature = get_method_signature(child_method_data)
                    # edge_id = f"{method_signature}->{child_method_signature}:{child['callSite']}"
                    edge_id = f"{method_signature}->{child_method_signature}"
                    INVOKE_FREQ[edge_id] += 1
    with open(stats_json, 'w') as f:
        stats = {
            consts.STATS_KEY_METHODS: dict(sorted(METHOD_FREQ.items(), key=lambda item: item[1], reverse=True)), 
            consts.STATS_KEY_EXEC_TYPES: dict(sorted(EXEC_TYPE_FREQ.items(), key=lambda item: item[1], reverse=True)),
            consts.STATS_KEY_INVOKES: dict(sorted(INVOKE_FREQ.items(), key=lambda item: item[1], reverse=True)), 
            consts.STATS_KEY_ROOTS: dict(sorted(ROOT_FREQ.items(), key=lambda item: item[1], reverse=True)),
            consts.STATS_KEY_LAMBDAS: dict(sorted(LAMBDAS.items(), key=lambda item: item[1], reverse=True)),
            consts.STATS_KEY_LAMBDA_COUNT: len(LAMBDAS),
            consts.STATS_KEY_METHOD_COUNT: len(METHOD_FREQ),
            consts.STATS_KEY_INVOKE_COUNT: len(INVOKE_FREQ),
        }
        json.dump(stats, f, indent=4)




    


    