import argparse
import diff
import const
import os
import json
import stats
import util
import numpy as np
import matplotlib.pyplot as plt


def gen_heatmap(title, metric_label, n, file_diffs, files, value_func,show=False):
    diff_data = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            diff_data[i][j] = value_func(file_diffs[files[i]][files[j]])
    diff_data = np.array(diff_data)
    fig, ax = plt.subplots()
    im = ax.imshow(diff_data)

    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(n), labels=files)
    ax.set_yticks(np.arange(n), labels=files)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            text = ax.text(j, i, diff_data[i, j], ha="center", va="center")
    # Add the color bar
    cbar = ax.figure.colorbar(im, ax = ax)
    cbar.ax.set_ylabel(metric_label, rotation = -90, va = "bottom")

    ax.set_title(title)
    fig.tight_layout()
    plt.ylabel('f1')
    plt.xlabel('f2')
    plt.savefig(f"{const.PLOT_DIR}/{title}.png")
    if show:
        plt.show()

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
    out_dir = const.OUT_DIR
    util.mkdir(out_dir)
    util.mkdir(const.PLOT_DIR)
    stats_table = {}
    # generate stats for each input file
    for file_name in files:
        with open(f"{args.dir}/{file_name}.json", 'r') as f:
            stats1 = stats.gen_stats(json.load(f))
        with open(f"{out_dir}/stats_{file_name}.json", 'w') as f:
            json.dump(stats1, f, indent=4)
        stats_table[file_name] = stats1
    file_diffs = {f: {} for f in files}
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            print(f"diff: {files[i]} vs {files[j]}")
            file_diffs[files[i]][files[j]] = diff.gen_diff(
                                                stats_table[files[i]], 
                                                stats_table[files[j]],
                                                files[i],
                                                files[j])

    gen_heatmap(f"{args.prefix}: Method Freq. Count Ratios",
                "f1-only Method Freq. Count:Total f1 Method Freq. Count",
                n, 
                file_diffs, 
                files, 
                lambda data: round(data[const.DIFF_KEY_F1_ONLY_METHOD_FREQ_COUNT]/data[const.DIFF_KEY_F1_METHOD_FREQ_COUNT],5),
                show=args.show)
    
    gen_heatmap(f"{args.prefix}: Method Count Ratios",
                "f1-only Method Count:Total f1 Method Count",
                n, 
                file_diffs, 
                files, 
                lambda data: round(data[const.DIFF_KEY_F1_ONLY_METHOD_COUNT]/data[const.DIFF_KEY_F1_METHOD_COUNT],5),
                show=args.show)
    

    gen_heatmap(f"{args.prefix}: Invoke Count Ratios",
                "f1-only Invoke Count:Total f1 Invoke Count",
                n, 
                file_diffs, 
                files, 
                lambda data: round(data[const.DIFF_KEY_F1_ONLY_INVOKE_COUNT]/data[const.DIFF_KEY_F1_INVOKE_COUNT],5),
                show=args.show)

    gen_heatmap(f"{args.prefix}: Invoke Freq. Count Ratios",
                "f1-only Invoke Freq. Count:Total f1 Invoke Freq. Count",
                n, 
                file_diffs, 
                files, 
                lambda data: round(data[const.DIFF_KEY_F1_ONLY_INVOKE_FREQ_COUNT]/data[const.DIFF_KEY_F1_INVOKE_FREQ_COUNT],5),
                show=args.show)
    