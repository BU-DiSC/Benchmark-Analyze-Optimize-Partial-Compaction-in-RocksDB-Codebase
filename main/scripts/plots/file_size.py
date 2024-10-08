import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

matplotlib.rcParams['text.antialiased'] = True
fig, axs = plt.subplots(1, 4, figsize=(12, 2))

def get_data(df, strategy):
    data = df[df['Strategy'] == strategy]
    return data

def myplot(labels, sub_dirs, data_total_bytes, ax, index, word, y_start, y_end, y_ticks):
    data = []
    for dir in sub_dirs:
        data.append(pd.read_csv(dir + '/result.txt', sep='\t'))

    tick_width = 0.04

    strategies = ['kRoundRobin', 'kMinOverlappingRatio', 'kOldestLargestSeqFirst', 'kOldestSmallestSeqFirst']
    strategies_label = ['RoundRobin', 'MinOverlappingRatio', 'OldestLargestSeqFirst', 'OldestSmallestSeqFirst']
    strategy_wide = 0.16
    strategy_colors = ['red', 'blue', 'green', 'purple']

    ax.text(0.95, 0.95, word, transform=ax.transAxes, fontsize=12, verticalalignment='top', horizontalalignment='right')

    for i in range(len(data)):
        # plot all strategies
        for j in range(len(strategies)):
            strategy = strategies[j]
            df = get_data(data[i], strategy)
            min_val = df['Min'] / data_total_bytes[i]
            max_val = df['Max'] / data_total_bytes[i]
            mean_val = df['Mean'] / data_total_bytes[i]
            percentile25val = df['25th'] / data_total_bytes[i]
            percentile75val = df['75th'] / data_total_bytes[i]
            # Plot a line from low to high
            start_x = i+strategy_wide*j

            # Plot min and max
            if i == 0 and index == 0:
                ax.plot([start_x, start_x], [min_val, percentile25val], label=strategies_label[j], color=strategy_colors[j], linewidth=1)
            else:
                ax.plot([start_x, start_x], [min_val, percentile25val], color=strategy_colors[j], linewidth=1)
            ax.plot([start_x, start_x], [percentile75val, max_val], color=strategy_colors[j], linewidth=1)
            ax.plot([start_x - tick_width, start_x + tick_width], [min_val, min_val], color=strategy_colors[j], linewidth=1)
            ax.plot([start_x - tick_width, start_x + tick_width], [max_val, max_val], color=strategy_colors[j], linewidth=1)

            # Plot a box between 25th and 75th percentile
            ax.plot([start_x - tick_width, start_x + tick_width], [percentile25val, percentile25val], color=strategy_colors[j], linewidth=1)
            ax.plot([start_x - tick_width, start_x + tick_width], [percentile75val, percentile75val], color=strategy_colors[j], linewidth=1)
            ax.plot([start_x - tick_width, start_x - tick_width], [percentile25val, percentile75val], color=strategy_colors[j], linewidth=1)
            ax.plot([start_x + tick_width, start_x + tick_width], [percentile25val, percentile75val], color=strategy_colors[j], linewidth=1)

            # Plot mean
            ax.scatter(start_x, mean_val, s=15, marker='x', color=strategy_colors[j], zorder=10, linewidth=0.75)
            # ax.scatter(start_x, median_val, s=15, marker='o', color=strategy_colors[j], zorder=10, linewidth=0.75)
        if i != len(data) - 1:
            # add a split dashed line
            ax.plot([i + 0.8, i + 0.8], [y_start, y_end], color='black', linestyle='dashed', linewidth=1)

    if index == 0:
        ax.set_ylabel('Write amplification')
    # if index >= 2:
    ax.set_xlabel('Target file size (MB)')

    # Set the x-axis labels
    offset = 0.31
    xticks = [i for i in range(len(labels))]
    for i in range(len(xticks)):
        xticks[i] = xticks[i] + offset
    ax.set_xticks(xticks, labels)

    # Set the range of y-axis
    ax.set_ylim(y_start, y_end)
    ax.set_yticks(ticks=y_ticks)

save_path = '/Users/weiran/BU/EDBT/Results/Final/revision/File-Size-2.pdf'
data_root = '/Users/weiran/BU/Thesis/rocksdb/main/workspace/edbt_revision/file_size/third_run'

sub_dirs = ['100_0', '50_50']
total_bytes = 5 * 1024 * 1024 * 1024

names_1 = ['16M', '32M', '64M', '128M']
names_2 = ['4', '10']
labels = ['16', '32', '64', '128']

target_dirs = []
for sub_dir in sub_dirs:
    for dir_2 in names_2:
        dir2 = []
        for dir_1 in names_1:
            dir2.append(data_root + '/' + dir_1 + '/' + dir_2 + '/' + sub_dir)
        target_dirs.append(dir2)

indices = [(0, 0), (0, 1), (0, 2), (0, 3)]
data_total_bytes = [[total_bytes for i in range(len(labels))] for j in range(len(indices))]
words = ['(a)', '(b)', '(c)', '(d)']
y_start = 2.5
y_end = 4.5
y_ticks = np.arange(y_start, y_end + 0.1, 1)
for i in range(len(indices)):
    # idx = indices[i]
    if i < 2:
        y_start = 3.5
        y_end = 5.5
        y_ticks = [4, 5]
    else:
        y_start = 2.5
        y_end = 4.5
        y_ticks = [3, 4]
    myplot(labels, target_dirs[i], data_total_bytes[i], axs[i], i, words[i], y_start, y_end, y_ticks)

fig.subplots_adjust(bottom=0.23)
fig.subplots_adjust(top=0.84)

fig.legend(loc='upper center', 
           bbox_to_anchor=(0.5, 0.97), 
           ncol=4, 
           borderaxespad=0.0, 
           frameon=False,
           handletextpad=0.5,
           borderpad=0.3,
           labelspacing=0.2)

plt.savefig(save_path, dpi=600)
