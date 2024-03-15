import argparse
import os
import json 
import consts
import subprocess
import util

def generate_stats_file(input_file, out_dir, output_name):
    cmd = f"python stats.py -i {input_file} -o {output_name}_stats.json"
    print(cmd)
    result = subprocess.run(cmd.split(" "))
    return f"{out_dir}/{output_name}_stats.json"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script comparing caller-callee relationships between program runs.')
    parser.add_argument('--input1', '-i1', type=str, required=True, help='path to the first input (.json) file to process with caller-callee data.')
    parser.add_argument('--input2', '-i2', type=str, required=True, help='path to the second input (.json) file to process with caller-callee data.')
    parser.add_argument('--output', '-o', type=str, default='', help='output (.json) file name which will contain results from the comparison.') 

    args = parser.parse_args()

    out_dir = 'out'
    if os.path.isdir(out_dir) == False:
        os.mkdir(out_dir) 
    diff_json = f"{out_dir}/{args.output}"
    if args.output == '':
        file_name1 = args.input1.split('/')[-1].split('.')[0].replace("_stats", "")
        file_name2 = args.input2.split('/')[-1].split('.')[0].replace("_stats", "")
        diff_json = f"{out_dir}/diff_{file_name1}_{file_name2}.json"

    # generate stats files
    stats_json_path1 = generate_stats_file(args.input1, out_dir, file_name1)
    stats_json_path2 = generate_stats_file(args.input2, out_dir, file_name2)
    stats1 = None
    stats2 = None
    with open(stats_json_path1, 'r') as f:
        stats1 = json.load(f)
    with open(stats_json_path2, 'r') as f:
        stats2 = json.load(f)
    
    diff = {
        consts.DIFF_KEY_FILE_NAME_1: file_name1,
        consts.DIFF_KEY_FILE_NAME_2: file_name2,
        consts.DIFF_KEY_SHARED_METHODS: {},
        consts.DIFF_KEY_METHODS: {},
        consts.DIFF_KEY_SHARED_INVOKES: {},
        consts.DIFF_KEY_INVOKES: {},
        consts.DIFF_KEY_LAMBDA_METHODS: {},
        consts.DIFF_KEY_LAMBDA_INVOKES: {},
        consts.DIFF_KEY_REFLECT_METHODS: {},
        consts.DIFF_KEY_REFLECT_INVOKES: {},
    }

    # compare methods
    for k in stats1[consts.STATS_KEY_METHODS]:
        if k not in stats2[consts.STATS_KEY_METHODS]:
            # write only single invocation count
            if "$$Lambda$" in k:
                diff[consts.DIFF_KEY_LAMBDA_METHODS][k] = stats1[consts.STATS_KEY_METHODS][k]
            elif "jdk.internal.reflect.Generated" in k:
                diff[consts.DIFF_KEY_REFLECT_METHODS][k] = stats1[consts.STATS_KEY_METHODS][k]
            else:
                diff[consts.DIFF_KEY_METHODS][k] = stats1[consts.STATS_KEY_METHODS][k]
        else:
            # write both invocation counts 
            diff[consts.DIFF_KEY_SHARED_METHODS][k] = [stats1[consts.STATS_KEY_METHODS][k], stats2[consts.STATS_KEY_METHODS][k]]
    for k in stats2[consts.STATS_KEY_METHODS]:
        if k not in stats1[consts.STATS_KEY_METHODS]:
            if "$$Lambda$" in k:
                diff[consts.DIFF_KEY_LAMBDA_METHODS][k] = stats2[consts.STATS_KEY_METHODS][k]
            elif "jdk.internal.reflect.Generated" in k:
                diff[consts.DIFF_KEY_REFLECT_METHODS][k] = stats2[consts.STATS_KEY_METHODS][k]
            else:
                diff[consts.DIFF_KEY_METHODS][k] = stats2[consts.STATS_KEY_METHODS][k]

    # compare invocations
    for k in stats1[consts.STATS_KEY_INVOKES]:
        if k not in stats2[consts.STATS_KEY_INVOKES]:
            if "$$Lambda$" in k:
                diff[consts.DIFF_KEY_LAMBDA_INVOKES][k] = stats1[consts.STATS_KEY_INVOKES][k]
            elif "jdk.internal.reflect.Generated" in k:
                diff[consts.DIFF_KEY_REFLECT_INVOKES][k] = stats1[consts.STATS_KEY_INVOKES][k]
            else:
                diff[consts.DIFF_KEY_INVOKES][k] = stats1[consts.STATS_KEY_INVOKES][k]
        else:
            diff[consts.DIFF_KEY_SHARED_INVOKES][k] = [stats1[consts.STATS_KEY_INVOKES][k], stats2[consts.STATS_KEY_INVOKES][k]]
    for k in stats2[consts.STATS_KEY_INVOKES]:
        if k not in stats1[consts.STATS_KEY_INVOKES]:
            if "$$Lambda$" in k:
                diff[consts.DIFF_KEY_LAMBDA_INVOKES][k] = stats2[consts.STATS_KEY_INVOKES][k]
            elif "jdk.internal.reflect.Generated" in k:
                diff[consts.DIFF_KEY_REFLECT_INVOKES][k] = stats2[consts.STATS_KEY_INVOKES][k]
            else:
                diff[consts.DIFF_KEY_INVOKES][k] = stats2[consts.STATS_KEY_INVOKES][k]

    diff[consts.DIFF_KEY_SHARED_METHOD_COUNT] = len(diff[consts.DIFF_KEY_SHARED_METHODS])
    diff[consts.DIFF_KEY_METHOD_COUNT] = len(diff[consts.DIFF_KEY_METHODS])
    diff[consts.DIFF_KEY_SHARED_INVOKE_COUNT] = len(diff[consts.DIFF_KEY_SHARED_INVOKES])
    diff[consts.DIFF_KEY_INVOKE_COUNT] = len(diff[consts.DIFF_KEY_INVOKES])
    diff[consts.DIFF_KEY_LAMBDA_COUNT] = len(diff[consts.DIFF_KEY_LAMBDA_METHODS])
    diff[consts.DIFF_KEY_LAMBDA_INVOKE_COUNT] = len(diff[consts.DIFF_KEY_LAMBDA_INVOKES])
    diff[consts.DIFF_KEY_REFLECT_COUNT] = len(diff[consts.DIFF_KEY_REFLECT_METHODS])
    diff[consts.DIFF_KEY_REFLECT_INVOKE_COUNT] = len(diff[consts.DIFF_KEY_REFLECT_INVOKES])
    
    diff[consts.DIFF_KEY_METHODS] = util.sort_dict(diff[consts.DIFF_KEY_METHODS])
    diff[consts.DIFF_KEY_INVOKES] = util.sort_dict(diff[consts.DIFF_KEY_INVOKES])
    diff[consts.DIFF_KEY_LAMBDA_METHODS] = util.sort_dict(diff[consts.DIFF_KEY_LAMBDA_METHODS])
    diff[consts.DIFF_KEY_LAMBDA_INVOKES] = util.sort_dict(diff[consts.DIFF_KEY_LAMBDA_INVOKES])
    diff[consts.DIFF_KEY_REFLECT_METHODS] = util.sort_dict(diff[consts.DIFF_KEY_REFLECT_METHODS])
    diff[consts.DIFF_KEY_REFLECT_INVOKES] = util.sort_dict(diff[consts.DIFF_KEY_REFLECT_INVOKES])

    with open(diff_json, 'w') as f:
        json.dump(diff, f, indent=4)
    
