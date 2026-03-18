# Translation error box plot: FPFH vs. Faster-PFH across KITTI and MulRan datasets.
# Set `consider_only_succeeded = True` to plot only successful registrations.
#
# DataFrame fed to seaborn:
#   'Dataset'  : "KITTI" | "MulRan"                                       → x-axis
#   'alg_name' : "FPFH W/o GS" | "FPFH W/ GS" | "Faster-PFH W/o GS" | "Faster-PFH W/ GS"  → hue
#   'time'     : float, translation error [m]  (variable name is reused)  → y-axis
#
# To use your own data, build a DataFrame with the same structure:
#   df = pd.DataFrame({
#       'Dataset':  ['DatasetA', 'DatasetA', 'DatasetB', ...],
#       'alg_name': ['Method A', 'Method B', 'Method A', ...],
#       'time':     [0.05, 0.12, 0.08, ...],   # your error values
#   })
# Then update hue_order, order, and pairs to match your group labels.

from statannotations.Annotator import Annotator
from variables import *
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

target = "trans" # trans or rot
consider_only_succeeded = True
def load_time_data(dir, alg_name):
    if (consider_only_succeeded):
        if (alg_name == "fpfh"):
            data1 = np.loadtxt(dir + '/2_to_6/Quatro_success.txt')
            data2 = np.loadtxt(dir + '/6_to_10/Quatro_success.txt')
            data3 = np.loadtxt(dir + '/10_to_12/Quatro_success.txt')
        elif (alg_name == "kiss-pfh"):
            data1 = np.loadtxt(dir + '/2_to_6/Quatro_success.txt')
            data2 = np.loadtxt(dir + '/6_to_10/Quatro_success.txt')
            data3 = np.loadtxt(dir + '/10_to_12/Quatro_success.txt')
    else:
        if (alg_name == "fpfh"):
            data1 = np.loadtxt(dir + '/2_to_6/Quatro_abs_errors.txt')
            data2 = np.loadtxt(dir + '/6_to_10/Quatro_abs_errors.txt')
            data3 = np.loadtxt(dir + '/10_to_12/Quatro_abs_errors.txt')
        elif (alg_name == "kiss-pfh"):
            data1 = np.loadtxt(dir + '/2_to_6/Quatro_abs_errors.txt')
            data2 = np.loadtxt(dir + '/6_to_10/Quatro_abs_errors.txt')
            data3 = np.loadtxt(dir + '/10_to_12/Quatro_abs_errors.txt')

    if (target == "trans"):
       return np.concatenate((data1[:, 4], data2[:, 4], data3[:, 4]))
    else:
        rotation = np.concatenate((data1[:, 5], data2[:, 5], data3[:, 5]))
        return rotation[rotation < 8.0]


def load_all_time_data(dir, seq_names, alg_name):
    all_data = np.array([])
    for seq_name in seq_names:
        time_data_for_each_seq = load_time_data(dir + "/" + seq_name, alg_name)
        all_data = np.concatenate((all_data, time_data_for_each_seq))

    return all_data
#######################################

data_list = []

saved_data_path = 'data/pose_error.pkl'

if not os.path.exists(saved_data_path):
    for alg_name in ["fpfh", "kiss-pfh"]:
        for ground in ["w-gs", "wo-gs"]:
            for dataset in ['KITTI', 'MulRan']:
                dir = "data/240118_fpfh_vs_ours_speed/240114_i9_{}-{}-0.3-1.5-0.9-multi-thread".format(alg_name, ground)

                if (dataset == 'KITTI'):
                    seq_names = ["00", "02", "05", "08"]
                else:
                    seq_names = ["DCC01", "KAIST02", "Riverside01"]
                data = load_all_time_data(dir, seq_names, alg_name)

                # Actually, it's not time
                for time in data:
                    if (alg_name == "fpfh"):
                        saved_alg_name = "FPFH"
                    else:
                        saved_alg_name = "Faster-PFH"

                    if (ground == "w-gs"):
                        saved_alg_name += " W/ GS"
                    else:
                        saved_alg_name += " W/o GS"

                    data_list.append({'ground': ground, 'alg_name': saved_alg_name, 'Dataset': dataset, 'time': time})

    df = pd.DataFrame(data_list)
    # df.to_pickle(saved_data_path)
else:
    df = pd.read_pickle(saved_data_path)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df)

sns.set(style="whitegrid")

x = "Dataset"
y = "time"
hue = "alg_name"
hue_order = ['FPFH W/o GS', 'FPFH W/ GS', 'Faster-PFH W/o GS', 'Faster-PFH W/ GS']
order = ['KITTI', 'MulRan']

pairs=[(("KITTI", "FPFH W/o GS"), ("KITTI", "FPFH W/ GS")),
       (("KITTI", "FPFH W/o GS"), ("KITTI", "Faster-PFH W/o GS")),
       (("KITTI", "FPFH W/ GS"), ("KITTI", "Faster-PFH W/ GS")),
       (("KITTI", "Faster-PFH W/o GS"), ("KITTI", "Faster-PFH W/ GS")),
       (("MulRan", "FPFH W/o GS"), ("MulRan", "FPFH W/ GS")),
       (("MulRan", "FPFH W/o GS"), ("MulRan", "Faster-PFH W/o GS")),
       (("MulRan", "FPFH W/ GS"), ("MulRan", "Faster-PFH W/ GS")),
       (("MulRan", "Faster-PFH W/o GS"), ("MulRan", "Faster-PFH W/ GS"))]

plt.figure(figsize=(fig_width4x4, fig_height4x4)) # width, height
# plt.gca().tick_params(axis='y', which='major', pad=10) # increase pad when tick numbers grow large
ax = sns.boxplot(data=df, x=x, y=y, order=order, hue=hue, hue_order=hue_order, linewidth=1.0)
ax.set_xlim(left=-left_margin, right=len(order)-right_margin)
# Log scale should be place here!!
# plt.yscale('log')
# annot = Annotator(ax, pairs, data=df, x=x, y=y, order=order, hue=hue, hue_order=hue_order)
# annot.new_plot(ax, pairs, data=df, x=x, y=y, order=order, hue=hue, hue_order=hue_order)
# annot.configure(test='Mann-Whitney', verbose=2)
# annot.apply_test()
# annot.annotate()

plt.rcParams['font.family'] = 'Times New Roman'
# plt.rcParams['font.size'] = 12
# tick label font settings
plt.xticks(fontname='Times New Roman', fontsize=tick_font_size)
plt.yticks(fontname='Times New Roman', fontsize=tick_font_size)
plt.xlabel("Dataset", fontdict={'family': 'Times New Roman'}, fontsize=font_size)
if (target == "trans"):
    plt.ylabel("Translation error [m]", fontdict={'family': 'Times New Roman'}, fontsize=font_size, labelpad=15)
else:
    plt.ylabel("Rotation error [deg]", fontdict={'family': 'Times New Roman'}, fontsize=font_size, labelpad=15)
# place legend below in 2x2 grid and adjust bottom margin
if (legend_on):
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.13), ncol=2)
else:
    ax.get_legend().remove()

plt.tight_layout()
if (target == "trans"):
    plt.savefig('output/trans_error.png', dpi=300, bbox_inches='tight')
    plt.savefig('output/trans_error.eps', dpi=300, bbox_inches='tight')
else:
    plt.savefig('output/rot_error.png', dpi=300, bbox_inches='tight')
    plt.savefig('output/rot_error.eps', dpi=300, bbox_inches='tight')
