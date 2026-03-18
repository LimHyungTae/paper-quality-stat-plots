# ATE comparison: SLAM w/ vs. w/o loop closure across different window sizes.
# Uses only the "Average" row from each CSV (one scalar per condition per run).
# Uncomment the first load block to use per-dataset rows instead of the average.
#
# DataFrame fed to seaborn:
#   'Window size' : "8" | "16" | "32"         → x-axis (categorical string)
#   'alg_name'    : "W/o LC" | "W/ LC"        → hue
#   'time'        : float, ATE [m]            → y-axis
#
# Each row is one run's average ATE for a given window size and condition.
# The box spans the distribution over multiple runs.
#
# To use your own data, build a DataFrame with the same structure:
#   df = pd.DataFrame({
#       'Window size': ['8', '8', '16', '16', ...],
#       'alg_name':   ['W/o LC', 'W/ LC', 'W/o LC', 'W/ LC', ...],
#       'time':       [0.28, 0.12, 0.17, 0.09, ...],   # ATE [m] per run
#   })
# Then update order, hue_order, and pairs to match your group labels.

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from statannotations.Annotator import Annotator
from pathlib import Path

# Settings
fig_width4x4 = 4  # You can adjust this based on your plot size preferences
tick_font_size = 20
font_size = 26
left_margin = 0.3
right_margin = 0.3

# File Definitions
files = [
    ("tum_results_8_wo_lc.txt", 8, "W/o LC"),
    ("tum_results_w8.txt", 8, "W/ LC"),
    ("tum_results_16_wo_lc.txt", 16, "W/o LC"),
    ("tum_results_w16.txt", 16, "W/ LC"),
    ("tum_results_32_wo_lc.txt", 32, "W/o LC"),
    ("tum_results_w32.txt", 32, "W/ LC"),
]

data_list = []

# Load Data
# for filename, window_size, alg_name in files:
#     filepath = "data/250514_w_wo_lc/" + filename
#     if os.path.exists(filepath):
#         df = pd.read_csv(filepath)
#         # Exclude the 'Average' rows for the boxplot
#         df = df[df["Dataset"] != "Average"]
#         for time in df["RMSE"]:
#             data_list.append({
#                 'Window size': str(window_size),
#                 'alg_name': alg_name,
#                 'time': time
#             })
#     else:
#         print(f"File {filepath} not found!")

for filename, window_size, alg_name in files:
    filepath = "data/250514_w_wo_lc/" + filename
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        avg_rows = df[df["Dataset"] == "Average"]
        if not avg_rows.empty:
            for avg_time in avg_rows["RMSE"].values:
                data_list.append({
                    'Window size': str(window_size),
                    'alg_name': alg_name,
                    'time': avg_time
                })
        else:
            print(f"No 'Average' row found in {filepath}!")
    else:
        print(f"File {filepath} not found!")

# Create DataFrame
plot_df = pd.DataFrame(data_list)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(plot_df)

# Plot Configuration
sns.set(style="whitegrid")
x = "Window size"
y = "time"
hue = "alg_name"
hue_order = ['W/o LC', 'W/ LC']
order = ['8', '16', '32']
pairs = [
    (("8", "W/o LC"), ("8", "W/ LC")),
    (("16", "W/o LC"), ("16", "W/ LC")),
    (("32", "W/o LC"), ("32", "W/ LC")),
]

##################################
# Important!!!
plt.rcParams['text.usetex'] = True
##################################
plt.figure(figsize=(3.75, fig_width4x4))
plt.gca().tick_params(axis='y', which='major', pad=-5)
# plt.ylim(0, 0.8)  # Adjust as needed based on your data
# plt.yticks([0.0, 0.2, 0.4, 0.6, 0.8])

ax = sns.boxplot(data=plot_df, x=x, y=y, order=order, hue=hue, hue_order=hue_order, linewidth=1.0, palette={"W/o LC": "#1f77b4", "W/ LC": "#ff7f0e"})
# ax.set_xlim(left=-left_margin, right=len(order) - right_margin)

# Statistical Annotation
annot = Annotator(ax, pairs, data=plot_df, x=x, y=y, order=order, hue=hue, hue_order=hue_order)
annot.configure(test='Mann-Whitney', verbose=2)
annot.apply_test()
annot.annotate()

# Font & Label Configuration
plt.rcParams['font.family'] = 'Times New Roman'
plt.xticks(fontname='Times New Roman', fontsize=tick_font_size)
plt.yticks(fontname='Times New Roman', fontsize=tick_font_size)
plt.xlabel(r"Window size, $w$", fontdict={'family': 'Times New Roman'}, fontsize=font_size)
plt.ylabel(r"ATE [m]", fontdict={'family': 'Times New Roman'}, fontsize=font_size)
plt.ylim(0, 0.4)
plt.yticks([0, 0.1, 0.2, 0.3, 0.4])
# Legend Configuration
legend_on = True
if legend_on:
    plt.legend(loc='upper center', bbox_to_anchor=(0.63, 1.01), ncol=1, fontsize=18)
else:
    ax.get_legend().remove()

plt.tight_layout()
plt.savefig('output/vggt_w_and_wo_lc.png', dpi=300, bbox_inches='tight')
plt.savefig('output/vggt_w_and_wo_lc.eps', dpi=300, bbox_inches='tight')
plt.show()
