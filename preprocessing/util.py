import os
import const
import numpy as np
import matplotlib.pyplot as plt

SMALL_SIZE = 20
MEDIUM_SIZE = 20
BIGGER_SIZE = 22

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

def mkdir(dir):
    if os.path.isdir(dir) == False:
        os.mkdir(dir)

def get_file_name(path):
    return path.split('/')[-1].split('.')[0]

def sort_dict(d: dict, reverse=True):
    return dict(sorted(d.items(), key=lambda item: item[1], reverse=reverse))

def distrib_by_upper_bounds(data, upper_bounds):
    bucket_map = {f"<={k}":0 for k in upper_bounds}
    for k in data:
        for upper in upper_bounds:
            if data[k] <= upper:
                bucket_map[f"<={upper}"] += 1
    return bucket_map

def stacked_barchart(title, metric_label, data, files, show=False):
    width = 0.5

    fig, ax = plt.subplots()
    fig.set_size_inches(16, 9)
    bottom = np.zeros(len(files))

    for label, value_list in data.items():
        p = ax.bar(files, value_list, width, label=label, bottom=bottom)
        bottom += value_list

    ax.set_title(title)
    ax.legend()
    plt.ylabel(metric_label)
    plt.xlabel("Program runs")
    # manager = plt.get_current_fig_manager() # make fullscreen
    # manager.resize(*manager.window.maxsize())
    plt.savefig(f"{const.PLOT_DIR}/{title}.png")
    if show:
        plt.show()

def grouped_barchart(title, metric_label, data, files, show=False):
    width = 0.15 # the width of the bars
    x = np.arange(len(files))  # the label locations

    fig, ax = plt.subplots(layout='constrained')
    fig.set_size_inches(16, 9)
    i = 0
    for label, value_list in data.items():
        rects = ax.bar(x + i*width, value_list, width, label=label)
        ax.bar_label(rects, padding=3, rotation=90, label_type='center')
        i += 1

    ax.set_title(title)
    # ax.legend(loc='center right', bbox_to_anchor=(1.05, 0.5),
    #       ncol=1, fancybox=True)
    ax.legend()
    ax.set_xticks(x + width * (len(data)-1)/2, files)
    # plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
    #         rotation_mode="anchor")
    plt.ylabel(metric_label)
    plt.xlabel("Program runs")
    # manager = plt.get_current_fig_manager() # make fullscreen
    # manager.resize(*manager.window.maxsize())
    plt.savefig(f"{const.PLOT_DIR}/{title}.png")
    if show:
        plt.show()
       

def heatmap(title, metric_label, file_diffs, files, data_func, show=False):
    n = len(files)
    diff_data = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            diff_data[i][j] = data_func(file_diffs[files[i]][files[j]])
    diff_data = np.array(diff_data)
    fig, ax = plt.subplots()
    fig.set_size_inches(16, 9)
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