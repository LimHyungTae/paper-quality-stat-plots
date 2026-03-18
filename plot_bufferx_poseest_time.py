# Pose estimation time comparison: RANSAC vs. KISS-Matcher across five datasets.
# Y-axis is log-scaled. Uses LaTeX rendering for dataset tick labels (requires a
# LaTeX installation; set plt.rcParams['text.usetex'] = False to disable).
#
# DataFrame fed to seaborn:
#   'Dataset'      : r'\texttt{3DMatch}' | r'\texttt{ScanNet++i}' | ...   → x-axis
#   'alg_name'     : "RANSAC" | "KISS-Matcher"                            → hue
#   'PoseEst_time' : float, end-to-end pose estimation time [s]           → y-axis
#
# To use your own data, build a DataFrame with the same structure:
#   df = pd.DataFrame({
#       'Dataset':      ['DatasetA', 'DatasetA', 'DatasetB', ...],
#       'alg_name':     ['Method A', 'Method B', 'Method A', ...],
#       'PoseEst_time': [0.001, 0.0002, 0.05, ...],
#   })
# Then update files, order, hue_order, pairs, and dataset_display_map accordingly.
# If you don't need LaTeX labels, set plt.rcParams['text.usetex'] = False
# and use plain strings in order/pairs.

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from statannotations.Annotator import Annotator
from pathlib import Path

# Settings
fig_width4x4 = 4
xtick_font_size = 24
tick_font_size = 20
font_size = 26
left_margin = 0.3
right_margin = 0.3

# File Definitions
files = [
    ("data/bufferx_data/threedmatch_3DMatch_512_3_1500_12141320.txt", "3DMatch", "RANSAC"),
    ("data/bufferx_data/threedmatch_3DMatch_512_3_1500_12141105.txt", "3DMatch", "KISS-Matcher"),
    ("data/bufferx_data/threedmatch_Scannetpp_iphone_512_3_1500_12141320.txt", "Scannetpp_iphone", "RANSAC"),
    ("data/bufferx_data/threedmatch_Scannetpp_iphone_512_3_1500_12141105.txt", "Scannetpp_iphone", "KISS-Matcher"),
    ("data/bufferx_data/threedmatch_TIERS_512_3_1500_12141320.txt", "TIERS", "RANSAC"),
    ("data/bufferx_data/threedmatch_TIERS_512_3_1500_12141105.txt", "TIERS", "KISS-Matcher"),
    ("data/bufferx_data/threedmatch_KAIST_512_3_1500_12141320.txt", "KAIST", "RANSAC"),
    ("data/bufferx_data/threedmatch_KAIST_512_3_1500_12141105.txt", "KAIST", "KISS-Matcher"),
    ("data/bufferx_data/threedmatch_MIT_512_3_1500_12141320.txt", "MIT", "RANSAC"),
    ("data/bufferx_data/threedmatch_MIT_512_3_1500_12141105.txt", "MIT", "KISS-Matcher"),
]

data_list = []

# Load Data
for filepath, dataset, alg_name in files:
    if os.path.exists(filepath):
        # Read the file, skipping the first comment line only
        df = pd.read_csv(filepath, sep='\t', skiprows=[0])
        # Clean column names (remove leading '#' and whitespace)
        df.columns = df.columns.str.strip().str.lstrip('#').str.strip()
        # Extract PoseEst_time(s) column (last column)
        for time in df["PoseEst_time(s)"]:
            data_list.append({
                'Dataset': dataset,
                'alg_name': alg_name,
                'PoseEst_time': time
            })
    else:
        print(f"File {filepath} not found!")

# Create DataFrame
plot_df = pd.DataFrame(data_list)

# Map dataset names to LaTeX texttt format
dataset_display_map = {
    '3DMatch': r'\texttt{3DMatch}',
    'Scannetpp_iphone': r'\texttt{ScanNet++i}',
    'TIERS': r'\texttt{TIERS}',
    'KAIST': r'\texttt{KAIST}',
    'MIT': r'\texttt{MIT}'
}
plot_df['Dataset'] = plot_df['Dataset'].map(dataset_display_map)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(plot_df)

# Plot Configuration
sns.set(style="whitegrid")
x = "Dataset"
y = "PoseEst_time"
hue = "alg_name"
hue_order = ['RANSAC', 'KISS-Matcher']
order = [r'\texttt{3DMatch}', r'\texttt{ScanNet++i}', r'\texttt{TIERS}', r'\texttt{KAIST}', r'\texttt{MIT}']
pairs = [
    ((r'\texttt{3DMatch}', "RANSAC"), (r'\texttt{3DMatch}', "KISS-Matcher")),
    ((r'\texttt{ScanNet++i}', "RANSAC"), (r'\texttt{ScanNet++i}', "KISS-Matcher")),
    ((r'\texttt{TIERS}', "RANSAC"), (r'\texttt{TIERS}', "KISS-Matcher")),
    ((r'\texttt{KAIST}', "RANSAC"), (r'\texttt{KAIST}', "KISS-Matcher")),
    ((r'\texttt{MIT}', "RANSAC"), (r'\texttt{MIT}', "KISS-Matcher")),
]

##################################
# Important!!!
plt.rcParams['text.usetex'] = True
##################################
plt.figure(figsize=(12, fig_width4x4))
plt.gca().tick_params(axis='y', which='major', pad=-5)

ax = sns.boxplot(data=plot_df, x=x, y=y, order=order, hue=hue, hue_order=hue_order, linewidth=1.0, palette={"RANSAC": "#1f77b4", "KISS-Matcher": "#ff7f0e"})

# Set Y-axis to log scale
plt.yscale('log')
plt.ylim(top=1)  # 10^0 = 1

# Statistical Annotation
annot = Annotator(ax, pairs, data=plot_df, x=x, y=y, order=order, hue=hue, hue_order=hue_order)
annot.configure(test='Mann-Whitney', verbose=2)
annot.apply_test()
annot.annotate()

# Font & Label Configuration
plt.rcParams['font.family'] = 'Times New Roman'
plt.xticks(fontname='Times New Roman', fontsize=xtick_font_size)
plt.yticks(fontname='Times New Roman', fontsize=tick_font_size)
plt.xlabel(r"Dataset", fontdict={'family': 'Times New Roman'}, fontsize=font_size)
plt.ylabel(r"PoseEst\_time [s]", fontdict={'family': 'Times New Roman'}, fontsize=font_size)

# Legend Configuration
legend_on = True
if legend_on:
    plt.legend(loc='upper left', ncol=1, fontsize=18)
else:
    ax.get_legend().remove()

plt.tight_layout()
plt.savefig('output/bufferx_poseest_time.png', dpi=300, bbox_inches='tight')
plt.savefig('output/bufferx_poseest_time.eps', dpi=300, bbox_inches='tight')
plt.savefig('output/bufferx_poseest_time.pdf', dpi=300, bbox_inches='tight')
plt.show()
