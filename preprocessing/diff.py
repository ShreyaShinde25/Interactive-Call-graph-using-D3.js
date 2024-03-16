import argparse
import os
import json 
import const
import subprocess
import util
import stats

def gen_diff(stats1, stats2, file_name1, file_name2):
    diff_data = {
        const.DIFF_KEY_FILE_NAME_1: file_name1,
        const.DIFF_KEY_FILE_NAME_2: file_name2,
        const.DIFF_KEY_SHARED_METHODS: {},
        const.DIFF_KEY_SHARED_INVOKES: {},
        const.DIFF_KEY_F1_ONLY_METHODS: {},
        const.DIFF_KEY_F1_ONLY_LAMBDA_METHODS: {},
        const.DIFF_KEY_F1_ONLY_REFLECT_METHODS: {},
        const.DIFF_KEY_F1_ONLY_INVOKES: {},
        const.DIFF_KEY_F1_ONLY_LAMBDA_INVOKES: {},
        const.DIFF_KEY_F1_ONLY_REFLECT_INVOKES: {},
        const.DIFF_KEY_F2_ONLY_METHODS: {},
        const.DIFF_KEY_F2_ONLY_LAMBDA_METHODS: {},
        const.DIFF_KEY_F2_ONLY_REFLECT_METHODS: {},
        const.DIFF_KEY_F2_ONLY_INVOKES: {},
        const.DIFF_KEY_F2_ONLY_LAMBDA_INVOKES: {},
        const.DIFF_KEY_F2_ONLY_REFLECT_INVOKES: {},
    }

    # compare methods
    for k in stats1[const.STATS_KEY_METHODS]:
        if k not in stats2[const.STATS_KEY_METHODS]:
            # write only single invocation count
            if "$$Lambda$" in k:
                diff_data[const.DIFF_KEY_F1_ONLY_LAMBDA_METHODS][k] = stats1[const.STATS_KEY_METHODS][k]
            elif "jdk.internal.reflect.Generated" in k:
                diff_data[const.DIFF_KEY_F1_ONLY_REFLECT_METHODS][k] = stats1[const.STATS_KEY_METHODS][k]
            else:
                diff_data[const.DIFF_KEY_F1_ONLY_METHODS][k] = stats1[const.STATS_KEY_METHODS][k]
        else:
            # write both invocation counts 
            diff_data[const.DIFF_KEY_SHARED_METHODS][k] = [stats1[const.STATS_KEY_METHODS][k], stats2[const.STATS_KEY_METHODS][k]]
    for k in stats2[const.STATS_KEY_METHODS]:
        if k not in stats1[const.STATS_KEY_METHODS]:
            if "$$Lambda$" in k:
                diff_data[const.DIFF_KEY_F2_ONLY_LAMBDA_METHODS][k] = stats2[const.STATS_KEY_METHODS][k]
            elif "jdk.internal.reflect.Generated" in k:
                diff_data[const.DIFF_KEY_F2_ONLY_REFLECT_METHODS][k] = stats2[const.STATS_KEY_METHODS][k]
            else:
                diff_data[const.DIFF_KEY_F2_ONLY_METHODS][k] = stats2[const.STATS_KEY_METHODS][k]

    # compare invocations
    for k in stats1[const.STATS_KEY_INVOKES]:
        if k not in stats2[const.STATS_KEY_INVOKES]:
            if "$$Lambda$" in k:
                diff_data[const.DIFF_KEY_F1_ONLY_LAMBDA_INVOKES][k] = stats1[const.STATS_KEY_INVOKES][k]
            elif "jdk.internal.reflect.Generated" in k:
                diff_data[const.DIFF_KEY_F1_ONLY_REFLECT_INVOKES][k] = stats1[const.STATS_KEY_INVOKES][k]
            else:
                diff_data[const.DIFF_KEY_F1_ONLY_INVOKES][k] = stats1[const.STATS_KEY_INVOKES][k]
        else:
            diff_data[const.DIFF_KEY_SHARED_INVOKES][k] = [stats1[const.STATS_KEY_INVOKES][k], stats2[const.STATS_KEY_INVOKES][k]]
    for k in stats2[const.STATS_KEY_INVOKES]:
        if k not in stats1[const.STATS_KEY_INVOKES]:
            if "$$Lambda$" in k:
                diff_data[const.DIFF_KEY_F2_ONLY_LAMBDA_INVOKES][k] = stats2[const.STATS_KEY_INVOKES][k]
            elif "jdk.internal.reflect.Generated" in k:
                diff_data[const.DIFF_KEY_F2_ONLY_REFLECT_INVOKES][k] = stats2[const.STATS_KEY_INVOKES][k]
            else:
                diff_data[const.DIFF_KEY_F2_ONLY_INVOKES][k] = stats2[const.STATS_KEY_INVOKES][k]

    diff_data[const.DIFF_KEY_SHARED_METHOD_COUNT] = len(diff_data[const.DIFF_KEY_SHARED_METHODS])
    diff_data[const.DIFF_KEY_F1_ONLY_METHOD_COUNT] = len(diff_data[const.DIFF_KEY_F1_ONLY_METHODS])
    diff_data[const.DIFF_KEY_F1_ONLY_LAMBDA_METHOD_COUNT] = len(diff_data[const.DIFF_KEY_F1_ONLY_LAMBDA_METHODS])
    diff_data[const.DIFF_KEY_F1_ONLY_REFLECT_METHOD_COUNT] = len(diff_data[const.DIFF_KEY_F1_ONLY_REFLECT_METHODS])
    diff_data[const.DIFF_KEY_F1_METHOD_COUNT] = stats1[const.STATS_KEY_METHOD_COUNT]
    diff_data[const.DIFF_KEY_F2_ONLY_METHOD_COUNT] = len(diff_data[const.DIFF_KEY_F2_ONLY_METHODS])
    diff_data[const.DIFF_KEY_F2_ONLY_LAMBDA_METHOD_COUNT] = len(diff_data[const.DIFF_KEY_F2_ONLY_LAMBDA_METHODS])
    diff_data[const.DIFF_KEY_F2_ONLY_REFLECT_METHOD_COUNT] = len(diff_data[const.DIFF_KEY_F2_ONLY_REFLECT_METHODS])
    diff_data[const.DIFF_KEY_F2_METHOD_COUNT] = stats2[const.STATS_KEY_METHOD_COUNT]

    diff_data[const.DIFF_KEY_F1_ONLY_METHOD_FREQ_COUNT] = sum(diff_data[const.DIFF_KEY_F1_ONLY_METHODS].values())
    diff_data[const.DIFF_KEY_F1_ONLY_LAMBDA_METHOD_FREQ_COUNT] = sum(diff_data[const.DIFF_KEY_F1_ONLY_LAMBDA_METHODS].values())
    diff_data[const.DIFF_KEY_F1_ONLY_REFLECT_METHOD_FREQ_COUNT] = sum(diff_data[const.DIFF_KEY_F1_ONLY_REFLECT_METHODS].values())
    diff_data[const.DIFF_KEY_F1_METHOD_FREQ_COUNT] = stats1[const.STATS_KEY_METHOD_FREQ_COUNT]
    diff_data[const.DIFF_KEY_F1_ONLY_METHOD_FREQ_DISTRIB] = util.distrib_by_upper_bounds(
                                                                diff_data[const.DIFF_KEY_F1_ONLY_METHODS], const.DISTRIB_BOUNDS)
    diff_data[const.DIFF_KEY_F2_ONLY_METHOD_FREQ_COUNT] = sum(diff_data[const.DIFF_KEY_F2_ONLY_METHODS].values())
    diff_data[const.DIFF_KEY_F2_ONLY_LAMBDA_METHOD_FREQ_COUNT] = sum(diff_data[const.DIFF_KEY_F2_ONLY_LAMBDA_METHODS].values())
    diff_data[const.DIFF_KEY_F2_ONLY_REFLECT_METHOD_FREQ_COUNT] = sum(diff_data[const.DIFF_KEY_F2_ONLY_REFLECT_METHODS].values())
    diff_data[const.DIFF_KEY_F2_METHOD_FREQ_COUNT] = stats2[const.STATS_KEY_METHOD_FREQ_COUNT]
    diff_data[const.DIFF_KEY_F2_ONLY_METHOD_FREQ_DISTRIB] = util.distrib_by_upper_bounds(
                                                                diff_data[const.DIFF_KEY_F2_ONLY_METHODS], const.DISTRIB_BOUNDS)

    diff_data[const.DIFF_KEY_SHARED_INVOKE_COUNT] = len(diff_data[const.DIFF_KEY_SHARED_INVOKES])
    diff_data[const.DIFF_KEY_F1_ONLY_INVOKE_COUNT] = len(diff_data[const.DIFF_KEY_F1_ONLY_INVOKES])
    diff_data[const.DIFF_KEY_F1_ONLY_LAMBDA_INVOKE_COUNT] = len(diff_data[const.DIFF_KEY_F1_ONLY_LAMBDA_INVOKES])
    diff_data[const.DIFF_KEY_F1_ONLY_REFLECT_INVOKE_COUNT] = len(diff_data[const.DIFF_KEY_F1_ONLY_REFLECT_INVOKES])
    diff_data[const.DIFF_KEY_F1_INVOKE_COUNT] = stats1[const.STATS_KEY_INVOKE_COUNT]
    diff_data[const.DIFF_KEY_F2_ONLY_INVOKE_COUNT] = len(diff_data[const.DIFF_KEY_F2_ONLY_INVOKES])
    diff_data[const.DIFF_KEY_F2_ONLY_LAMBDA_INVOKE_COUNT] = len(diff_data[const.DIFF_KEY_F2_ONLY_LAMBDA_INVOKES])
    diff_data[const.DIFF_KEY_F2_ONLY_REFLECT_INVOKE_COUNT] = len(diff_data[const.DIFF_KEY_F2_ONLY_REFLECT_INVOKES])
    diff_data[const.DIFF_KEY_F2_INVOKE_COUNT] = stats2[const.STATS_KEY_INVOKE_COUNT]

    diff_data[const.DIFF_KEY_F1_ONLY_INVOKE_FREQ_COUNT] = sum(diff_data[const.DIFF_KEY_F1_ONLY_INVOKES].values())
    diff_data[const.DIFF_KEY_F1_ONLY_LAMBDA_INVOKE_FREQ_COUNT] = sum(diff_data[const.DIFF_KEY_F1_ONLY_LAMBDA_INVOKES].values())
    diff_data[const.DIFF_KEY_F1_ONLY_REFLECT_INVOKE_FREQ_COUNT] = sum(diff_data[const.DIFF_KEY_F1_ONLY_REFLECT_INVOKES].values())
    diff_data[const.DIFF_KEY_F1_INVOKE_FREQ_COUNT] = stats1[const.STATS_KEY_INVOKE_FREQ_COUNT]
    diff_data[const.DIFF_KEY_F1_ONLY_INVOKE_FREQ_DISTRIB] = util.distrib_by_upper_bounds(
                                                                diff_data[const.DIFF_KEY_F1_ONLY_INVOKES], const.DISTRIB_BOUNDS)
    
    diff_data[const.DIFF_KEY_F2_ONLY_INVOKE_FREQ_COUNT] = sum(diff_data[const.DIFF_KEY_F2_ONLY_INVOKES].values())
    diff_data[const.DIFF_KEY_F2_ONLY_LAMBDA_INVOKE_FREQ_COUNT] = sum(diff_data[const.DIFF_KEY_F2_ONLY_LAMBDA_INVOKES].values())
    diff_data[const.DIFF_KEY_F2_ONLY_REFLECT_INVOKE_FREQ_COUNT] = sum(diff_data[const.DIFF_KEY_F2_ONLY_REFLECT_INVOKES].values())
    diff_data[const.DIFF_KEY_F2_INVOKE_FREQ_COUNT] = stats2[const.STATS_KEY_INVOKE_FREQ_COUNT]
    diff_data[const.DIFF_KEY_F2_ONLY_INVOKE_FREQ_DISTRIB] = util.distrib_by_upper_bounds(
                                                                diff_data[const.DIFF_KEY_F2_ONLY_INVOKES], const.DISTRIB_BOUNDS)

    diff_data[const.DIFF_KEY_F1_ONLY_METHODS] = util.sort_dict(diff_data[const.DIFF_KEY_F1_ONLY_METHODS])
    diff_data[const.DIFF_KEY_F1_ONLY_LAMBDA_METHODS] = util.sort_dict(diff_data[const.DIFF_KEY_F1_ONLY_LAMBDA_METHODS])
    diff_data[const.DIFF_KEY_F1_ONLY_REFLECT_METHODS] = util.sort_dict(diff_data[const.DIFF_KEY_F1_ONLY_REFLECT_METHODS])
    diff_data[const.DIFF_KEY_F2_ONLY_METHODS] = util.sort_dict(diff_data[const.DIFF_KEY_F2_ONLY_METHODS])
    diff_data[const.DIFF_KEY_F2_ONLY_LAMBDA_METHODS] = util.sort_dict(diff_data[const.DIFF_KEY_F2_ONLY_LAMBDA_METHODS])
    diff_data[const.DIFF_KEY_F2_ONLY_REFLECT_METHODS] = util.sort_dict(diff_data[const.DIFF_KEY_F2_ONLY_REFLECT_METHODS])
    
    diff_data[const.DIFF_KEY_F1_ONLY_INVOKES] = util.sort_dict(diff_data[const.DIFF_KEY_F1_ONLY_INVOKES])
    diff_data[const.DIFF_KEY_F1_ONLY_LAMBDA_INVOKES] = util.sort_dict(diff_data[const.DIFF_KEY_F1_ONLY_LAMBDA_INVOKES])
    diff_data[const.DIFF_KEY_F1_ONLY_REFLECT_INVOKES] = util.sort_dict(diff_data[const.DIFF_KEY_F1_ONLY_REFLECT_INVOKES])
    diff_data[const.DIFF_KEY_F2_ONLY_INVOKES] = util.sort_dict(diff_data[const.DIFF_KEY_F2_ONLY_INVOKES])
    diff_data[const.DIFF_KEY_F2_ONLY_LAMBDA_INVOKES] = util.sort_dict(diff_data[const.DIFF_KEY_F2_ONLY_LAMBDA_INVOKES])
    diff_data[const.DIFF_KEY_F2_ONLY_REFLECT_INVOKES] = util.sort_dict(diff_data[const.DIFF_KEY_F2_ONLY_REFLECT_INVOKES])
    
    return diff_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script comparing caller-callee relationships between program runs.')
    parser.add_argument('--input1', '-i1', type=str, required=True, help='path to the first input (.json) file to process with caller-callee data.')
    parser.add_argument('--input2', '-i2', type=str, required=True, help='path to the second input (.json) file to process with caller-callee data.')
    parser.add_argument('--output', '-o', type=str, default='', help='output (.json) file name which will contain results from the comparison.') 

    args = parser.parse_args()

    out_dir = const.OUT_DIR
    util.mkdir(out_dir)

    diff_json = f"{out_dir}/{args.output}"
    if args.output == '':
        file_name1 = util.get_file_name(args.input1).replace("stats_", "")
        file_name2 = util.get_file_name(args.input2).replace("stats_", "")
        diff_json = f"{out_dir}/diff_{file_name1}_{file_name2}.json"

    # generate stats files
    with open(args.input1, 'r') as f:
        stats1 = stats.gen_stats(json.load(f))
        json.dump(stats1, f"{out_dir}/stats_{file_name1}.json", indent=4)
    with open(args.input2, 'r') as f:
        stats2 = stats.gen_stats(json.load(f))
        json.dump(stats2, f"{out_dir}/stats_{file_name2}.json", indent=4)

    
    diff_data = gen_diff(stats1, stats2, file_name1, file_name2)

    with open(diff_json, 'w') as f:
        json.dump(diff_data, f, indent=4)
    
