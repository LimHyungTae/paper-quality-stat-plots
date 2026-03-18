# Feature extraction speed comparison: FPFH vs. Faster-PFH,
# across single-thread / multi-thread and w/ or w/o ground segmentation.
#
# DataFrame fed to seaborn:
#   'thread'   : "Single-thread" | "Multi-thread"                        → x-axis
#   'alg_name' : "FPFH w/o GS" | "FPFH w/ GS" | "Faster-PFH w/o GS" | "Faster-PFH w/ GS"  → hue
#   'time'     : float, feature extraction time [s]                      → y-axis
#
# To use your own data, build a DataFrame with the same structure:
#   df = pd.DataFrame({
#       'thread':   ['Single-thread', 'Single-thread', 'Multi-thread', ...],
#       'alg_name': ['Method A', 'Method B', 'Method A', ...],
#       'time':     [0.45, 0.12, 0.10, ...],
#   })
# Then update hue_order, order, and pairs to match your group labels.

from statannotations.Annotator import Annotator
from variables import *
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

def load_time_data(dir, alg_name):
    if (alg_name == "fpfh"):
        data1 = np.loadtxt(dir + '/2_to_6_FPFH_extraction_and_matching.txt')
        data2 = np.loadtxt(dir + '/6_to_10_FPFH_extraction_and_matching.txt')
        data3 = np.loadtxt(dir + '/10_to_12_FPFH_extraction_and_matching.txt')
    elif (alg_name == "kiss-pfh"):
        data1 = np.loadtxt(dir + '/2_to_6_KISS-PFH_extraction_and_matching.txt')
        data2 = np.loadtxt(dir + '/6_to_10_KISS-PFH_extraction_and_matching.txt')
        data3 = np.loadtxt(dir + '/10_to_12_KISS-PFH_extraction_and_matching.txt')

    time_extraction = np.concatenate((data1[:, 0], data2[:, 0], data3[:, 0]))
    return time_extraction

def load_all_time_data(dir, seq_names, alg_name):
    all_data = np.array([])
    for seq_name in seq_names:
        time_data_for_each_seq = load_time_data(dir + "/" + seq_name, alg_name)
        all_data = np.concatenate((all_data, time_data_for_each_seq))

    return all_data
#######################################

data_list = []

saved_data_path = 'data/speed_data.pkl'

if not os.path.exists(saved_data_path):
    seq_names = ["00", "02", "05", "08", "DCC01", "KAIST02", "Riverside01"]
    for alg_name in ["fpfh", "kiss-pfh"]:
        for ground in ["w-gs", "wo-gs"]:
            for thread in ['single-thread', 'multi-thread']:
                dir = "data/240118_fpfh_vs_ours_speed/240114_i9_{}-{}-0.3-1.5-0.9-{}".format(alg_name, ground, thread)
                data = load_all_time_data(dir, seq_names, alg_name)

                for time in data:
                    if (alg_name == "fpfh"):
                        saved_alg_name = "FPFH"
                    else:
                        saved_alg_name = "Faster-PFH"

                    if (ground == "w-gs"):
                        saved_alg_name += " w/ GS"
                    else:
                        saved_alg_name += " w/o GS"

                    if (thread == "single-thread"):
                        saved_thread = "Single-thread"
                    else:
                        saved_thread = "Multi-thread"
                    data_list.append({'ground': ground, 'alg_name': saved_alg_name, 'thread': saved_thread, 'time': time})

    df = pd.DataFrame(data_list)
    df.to_pickle(saved_data_path)
else:
    df = pd.read_pickle(saved_data_path)

print(df)
df['time'] = pd.to_numeric(df['time'], errors='coerce')
df['alg_name'] = df['alg_name'].str.replace('W/', 'w/')
df['alg_name'] = df['alg_name'].str.replace('W/o', 'w/o')
stats = df.groupby(['thread', 'alg_name'])['time'].agg(['mean', 'var'])
print(stats)

sns.set(style="whitegrid")

x = "thread"
y = "time"
hue = "alg_name"
hue_order = ['FPFH w/o GS', 'FPFH w/ GS', 'Faster-PFH w/o GS', 'Faster-PFH w/ GS']
order = ['Single-thread', 'Multi-thread']

# pairs=[(("Single-thread", "FPFH W/o GS"), ("Single-thread", "FPFH W/ GS")),
#        (("Single-thread", "Faster PFH W/o GS"), ("Single-thread", "Faster PFH W/ GS")),
#        (("Multi-thread", "FPFH W/o GS"), ("Multi-thread", "FPFH W/ GS")),
#        (("Multi-thread", "Faster PFH W/o GS"), ("Multi-thread", "Faster PFH W/ GS"))]
pairs=[(("Single-thread", "FPFH w/o GS"), ("Single-thread", "Faster-PFH w/o GS")),
       (("Single-thread", "FPFH w/ GS"), ("Single-thread", "Faster-PFH w/ GS")),
       (("Multi-thread", "FPFH w/o GS"), ("Multi-thread", "Faster-PFH w/o GS")),
       (("Multi-thread", "FPFH w/ GS"), ("Multi-thread", "Faster-PFH w/ GS"))]

plt.figure(figsize=(fig_width4x4, fig_width4x4))
plt.gca().tick_params(axis='y', which='major', pad=-5) # increase pad when tick numbers grow large
plt.ylim(0, 0.8)
plt.yticks([0.0, 0.2, 0.4, 0.6, 0.8])

ax = sns.boxplot(data=df, x=x, y=y, order=order, hue=hue, hue_order=hue_order, linewidth=1.0)
# When you want to draw red lines
ax.set_xlim(left=-left_margin, right=len(order)-right_margin)
# plt.axhline(y=0.1, color='red', linestyle='--', linewidth=3.0)
# Log scale should be place here!!

# plt.yscale('log')
annot = Annotator(ax, pairs, data=df, x=x, y=y, order=order, hue=hue, hue_order=hue_order)
annot.new_plot(ax, pairs, data=df, x=x, y=y, order=order, hue=hue, hue_order=hue_order)
annot.configure(test='Mann-Whitney', verbose=2)
annot.apply_test()
annot.annotate()

plt.rcParams['font.family'] = 'Times New Roman'
# plt.rcParams['font.size'] = 12
# tick label font settings
plt.xticks(fontname='Times New Roman', fontsize=tick_font_size)
plt.yticks(fontname='Times New Roman', fontsize=tick_font_size)
plt.xlabel("Threading", fontdict={'family': 'Times New Roman'}, fontsize=font_size)
plt.ylabel("Time [sec]", fontdict={'family': 'Times New Roman'}, fontsize=font_size)
# place legend below in 2x2 grid and adjust bottom margin
legend_on = True
if (legend_on):
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.25), ncol=2)
    # plt.legend(loc='upper right')
else:
    ax.get_legend().remove()
plt.tight_layout()
plt.savefig('output/speed.png', dpi=300, bbox_inches='tight')
plt.savefig('output/speed.eps', dpi=300, bbox_inches='tight')
