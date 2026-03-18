# Registration success rate bar plot: FPFH vs. Faster-PFH across datasets.
# Uses sns.barplot instead of sns.boxplot — the statannotations API is identical.
#
# DataFrame fed to seaborn:
#   'Dataset'   : "KITTI (HDL-64E)" | "MulRan (OS1-64)"                    → x-axis
#   'Alg. name' : "FPFH W/o GS" | "FPFH W/ GS" | "Faster-PFH W/o GS" | "Faster-PFH W/ GS"  → hue
#   'time'      : float, success rate [%]  (variable name is reused)        → y-axis
#
# Each row is one overlap-distance bin × sequence combination.
# The bar height and error bar are computed automatically by sns.barplot (mean ± CI).
#
# To use your own data, build a DataFrame with the same structure:
#   df = pd.DataFrame({
#       'Dataset':    ['DatasetA', 'DatasetA', 'DatasetB', ...],
#       'Alg. name':  ['Method A', 'Method B', 'Method A', ...],
#       'time':       [97.5, 99.0, 85.0, ...],   # success rate [%] per trial
#   })
# Then update hue_order, order, and pairs to match your group labels.

from statannotations.Annotator import Annotator
from variables import *
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

total_num = 200.0
def load_time_data(dir, alg_name):
    if (alg_name == "fpfh"):
        data1 = np.loadtxt(dir + '/2_to_6/Quatro_success.txt')
        data2 = np.loadtxt(dir + '/6_to_10/Quatro_success.txt')
        data3 = np.loadtxt(dir + '/10_to_12/Quatro_success.txt')
    elif (alg_name == "kiss-pfh"):
        data1 = np.loadtxt(dir + '/2_to_6/Quatro_success.txt')
        data2 = np.loadtxt(dir + '/6_to_10/Quatro_success.txt')
        data3 = np.loadtxt(dir + '/10_to_12/Quatro_success.txt')
    succ1 = data1.shape[0] / total_num * 100
    succ2 = data2.shape[0] / total_num * 100
    succ3 = data3.shape[0] / total_num * 100
    return np.array([succ1, succ2, succ3])

def load_all_time_data(dir, seq_names, alg_name):
    all_data = np.array([])
    for seq_name in seq_names:
        time_data_for_each_seq = load_time_data(dir + "/" + seq_name, alg_name)
        all_data = np.concatenate((all_data, time_data_for_each_seq))

    return all_data
#######################################

data_list = []

saved_data_path = 'data/success_rate.pkl'

if not os.path.exists(saved_data_path):
    for alg_name in ["fpfh", "kiss-pfh"]:
        for ground in ["w-gs", "wo-gs"]:
            for dataset in ["KITTI (HDL-64E)", "MulRan (OS1-64)"]:
                dir = "data/240118_fpfh_vs_ours_speed/240114_i9_{}-{}-0.3-1.5-0.9-multi-thread".format(alg_name, ground)

                if (dataset == "KITTI (HDL-64E)"):
                    seq_names = ["00", "02", "05", "08"]
                else:
                    seq_names = ["DCC01", "KAIST02", "Riverside01"]
                data = load_all_time_data(dir, seq_names, alg_name)

                for time in data:
                    if (alg_name == "fpfh"):
                        saved_alg_name = "FPFH"
                    else:
                        saved_alg_name = "Faster-PFH"

                    if (ground == "w-gs"):
                        saved_alg_name += " W/ GS"
                    else:
                        saved_alg_name += " W/o GS"

                    data_list.append({'ground': ground, 'Alg. name': saved_alg_name, 'Dataset': dataset, 'time': time})

    df = pd.DataFrame(data_list)
    # df.to_pickle(saved_data_path)
else:
    df = pd.read_pickle(saved_data_path)

print(df)

sns.set(style="whitegrid")

x = "Dataset"
y = "time"
hue = "Alg. name"
hue_order = ['FPFH W/o GS', 'FPFH W/ GS', 'Faster-PFH W/o GS', 'Faster-PFH W/ GS']
order = ['KITTI (HDL-64E)', 'MulRan (OS1-64)']

pairs=[(("KITTI (HDL-64E)", "FPFH W/o GS"), ("KITTI (HDL-64E)", "FPFH W/ GS")),
       (("KITTI (HDL-64E)", "FPFH W/o GS"), ("KITTI (HDL-64E)", "Faster-PFH W/o GS")),
       (("KITTI (HDL-64E)", "FPFH W/ GS"), ("KITTI (HDL-64E)", "Faster-PFH W/ GS")),
       (("KITTI (HDL-64E)", "Faster-PFH W/o GS"), ("KITTI (HDL-64E)", "Faster-PFH W/ GS")),
       (("MulRan (OS1-64)", "FPFH W/o GS"), ("MulRan (OS1-64)", "FPFH W/ GS")),
       (("MulRan (OS1-64)", "FPFH W/o GS"), ("MulRan (OS1-64)", "Faster-PFH W/o GS")),
       (("MulRan (OS1-64)", "FPFH W/ GS"), ("MulRan (OS1-64)", "Faster-PFH W/ GS")),
       (("MulRan (OS1-64)", "Faster-PFH W/o GS"), ("MulRan (OS1-64)", "Faster-PFH W/ GS"))]

plt.figure(figsize=(fig_width4x4, fig_width4x4)) # width, height
ax = sns.barplot(data=df, x=x, y=y, order=order, hue=hue, hue_order=hue_order, linewidth=1.0)
ax.set_xlim(left=-left_margin, right=len(order)-right_margin)
ax.set_ylim(bottom=50, top=100)
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
plt.xticks(fontname='Times New Roman', fontsize=tick_font_size-1)
plt.yticks(fontname='Times New Roman', fontsize=tick_font_size)
plt.xlabel("Dataset", fontdict={'family': 'Times New Roman'}, fontsize=font_size)
plt.ylabel("Sucess rate [%]", fontdict={'family': 'Times New Roman'}, fontsize=font_size, labelpad=15)
# place legend at lower center

legend = plt.legend(loc='lower center', title=None, fontsize=font_size-2)

plt.tight_layout()
plt.savefig('output/success_rate.png', dpi=400, bbox_inches='tight')
plt.savefig('output/success_rate.eps', dpi=400, bbox_inches='tight')
