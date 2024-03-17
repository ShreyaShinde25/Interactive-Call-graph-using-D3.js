import argparse
import diff
import const
import os
import json
import stats
import util


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script performing pairwise diff of caller-callee relationships between program runs.')
    parser.add_argument('--prefix', '-p', type=str, required=True, help='file name prefix for pairwise diff (.json) files to with caller-callee data.')
    parser.add_argument('--dir', '-d', type=str, default=const.OUT_DIR, help='directory which contains the (.json) files to perform pairwise diffs.')
    parser.add_argument('--show', default=False, action=argparse.BooleanOptionalAction, help='Show generated plots one at a time.')
    args = parser.parse_args()

    files = [util.get_file_name(f) for f in os.listdir(args.dir) if os.path.isfile(os.path.join(args.dir, f)) and f.startswith(args.prefix)]
    files.sort()
    n = len(files)
    print(files)
    util.mkdir(const.OUT_DIR)
    util.mkdir(const.PLOT_DIR)
    stats_data_map = {}
    # generate stats for each input file
    for file_name in files:
        with open(f"{args.dir}/{file_name}.json", 'r') as f:
            stats_data_map[file_name] = stats.gen_stats(json.load(f), file_name=file_name, save_to_disk=True)
    file_diffs = {f: {} for f in files}
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            print(f"diff: {files[i]} vs {files[j]}")
            file_diffs[files[i]][files[j]] = diff.gen_diff(
                                                stats_data_map[files[i]], 
                                                stats_data_map[files[j]],
                                                files[i],
                                                files[j],
                                                save_to_disk=False)
    ROUNDING = 3
    util.heatmap(f"{args.prefix}: Shared Method Count Ratios",
                "Shared Method Count : Total f1 Method Count",
                file_diffs, 
                files, 
                lambda data: round(data[const.DIFF_KEY_SHARED_METHOD_COUNT]/data[const.DIFF_KEY_F1_ALL_METHOD_COUNT],ROUNDING),
                show=args.show)
    
    util.heatmap(f"{args.prefix}: Unique Method Count Ratios",
                "f1-only Method Count : Total f1 Method Count",
                file_diffs, 
                files, 
                lambda data: round(data[const.DIFF_KEY_F1_ONLY_DEFAULT_METHOD_COUNT]/data[const.DIFF_KEY_F1_ALL_METHOD_COUNT],ROUNDING),
                show=args.show)

    util.heatmap(f"{args.prefix}: Unique Method Freq. Sum Ratios",
                "f1-only Method Freq. Sum : Total f1 Method Freq. Sum",
                file_diffs, 
                files, 
                lambda data: round(data[const.DIFF_KEY_F1_ONLY_DEFAULT_METHOD_FREQ_SUM]/data[const.DIFF_KEY_F1_ALL_METHOD_FREQ_SUM],ROUNDING),
                show=args.show)
    
    util.heatmap(f"{args.prefix}: Unique Method with Freq. <= 1 Ratios",
                "f1-only Method w. Freq. <=1 : f1-only Method Count",
                file_diffs, 
                files, 
                lambda data: round(data[const.DIFF_KEY_F1_ONLY_DEFAULT_METHOD_FREQ_DISTRIB]["<=1"]/data[const.DIFF_KEY_F1_ONLY_DEFAULT_METHOD_COUNT],ROUNDING),
                show=args.show) 

    util.heatmap(f"{args.prefix}: Shared Invoke Count Ratios",
                "Shared Invoke Count : Total f1 Invoke Count",
                file_diffs, 
                files, 
                lambda data: round(data[const.DIFF_KEY_SHARED_INVOKE_COUNT]/data[const.DIFF_KEY_F1_INVOKE_COUNT],ROUNDING),
                show=args.show)
    
    util.heatmap(f"{args.prefix}: Unique Invoke Count Ratios",
                "f1-only Invoke Count : Total f1 Invoke Count",
                file_diffs, 
                files, 
                lambda data: round(data[const.DIFF_KEY_SHARED_INVOKE_COUNT]/data[const.DIFF_KEY_F1_INVOKE_COUNT],ROUNDING),
                show=args.show)

    util.heatmap(f"{args.prefix}: Unique Invoke Freq. Sum Ratios",
                "f1-only Invoke Freq. Sum : Total f1 Invoke Freq. Sum",
                file_diffs, 
                files, 
                lambda data: round(data[const.DIFF_KEY_F1_ONLY_INVOKE_FREQ_SUM]/data[const.DIFF_KEY_F1_INVOKE_FREQ_SUM],ROUNDING),
                show=args.show)

    util.heatmap(f"{args.prefix}: Unique Invoke with Freq. <= 1 Ratios",
                "f1-only Invoke w. Freq. <=1 : f1-only Invoke Count",
                file_diffs, 
                files, 
                lambda data: round(data[const.DIFF_KEY_F1_ONLY_INVOKE_FREQ_DISTRIB]["<=1"]/data[const.DIFF_KEY_F1_ONLY_INVOKE_COUNT],ROUNDING),
                show=args.show) 

    DISTRIB_KEYS = [f"<={v}" for v in const.DISTRIB_BOUNDS]
    d = {k: [stats_data_map[f][const.STATS_KEY_ALL_METHOD_FREQ_DISTRIB][k] for f in files] for k in DISTRIB_KEYS}
    util.grouped_barchart(title=f"{args.prefix}: Method Freq. Distribution",
                     metric_label="Frequency",
                     data=d,
                     files=files,
                     show=args.show,)
    d = {k: [stats_data_map[f][const.STATS_KEY_ALL_INVOKE_FREQ_DISTRIB][k] for f in files] for k in DISTRIB_KEYS}
    util.grouped_barchart(title=f"{args.prefix}: Invoke Freq. Distribution",
                     metric_label="Frequency",
                     data=d,
                     files=files,
                     show=args.show,)
    
    METHOD_TYPES = {
        "reflect": const.STATS_KEY_REFLECT_METHOD_COUNT, 
        "lambda": const.STATS_KEY_LAMBDA_METHOD_COUNT, 
        "default": const.STATS_KEY_DEFAULT_INVOKE_COUNT}
    d = {k: [stats_data_map[f][METHOD_TYPES[k]] for f in files] for k in METHOD_TYPES}
    util.stacked_barchart(title=f"{args.prefix}: Method Count Breakdown",
                     metric_label="Count",
                     data=d,
                     files=files,
                     show=args.show,)
    METHOD_TYPES = {
        "reflect": const.STATS_KEY_REFLECT_METHOD_FREQ_SUM, 
        "lambda": const.STATS_KEY_LAMBDA_MEHTOD_FREQ_SUM,
        "default": const.STATS_KEY_DEFAULT_METHODS_FREQ_SUM}

    d = {k: [stats_data_map[f][METHOD_TYPES[k]] for f in files] for k in METHOD_TYPES}
    util.stacked_barchart(title=f"{args.prefix}: Method Freq. Sum Breakdown",
                     metric_label="Frequency",
                     data=d,
                     files=files,
                     show=args.show,)