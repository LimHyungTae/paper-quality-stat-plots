# statannotations Examples

Real-world examples of statistical annotation on publication-quality plots using [statannotations](https://github.com/trevismd/statannotations), drawn from figures published in the [KISS-Matcher paper](https://arxiv.org/abs/2409.15615) (RA-L 2025).

Each script is self-contained: load data → draw a seaborn plot → annotate with `statannotations`.

---

## Installation

```bash
pip install statannotations seaborn matplotlib pandas numpy
```

---

## Quick Start

The simplest usage — no `hue`, annotations placed inside the plot:

```python
from statannotations.Annotator import Annotator
import matplotlib.pyplot as plt
import seaborn as sns

df = sns.load_dataset("tips")
x, y = "day", "total_bill"
order = ['Sun', 'Thur', 'Fri', 'Sat']

ax = sns.boxplot(data=df, x=x, y=y, order=order)

annot = Annotator(ax, [("Thur", "Fri"), ("Thur", "Sat"), ("Fri", "Sun")],
                  data=df, x=x, y=y, order=order)
annot.configure(test='Mann-Whitney', text_format='star', loc='inside', verbose=2)
annot.apply_test()
ax, test_results = annot.annotate()

plt.savefig('example_basic.png', dpi=300, bbox_inches='tight')
```

```bash
python3 example_basic_boxplot.py
```

![Basic boxplot with statannotations](figs/example_basic.png)

---

## Examples

### 1. Box plot — with `hue` (multi-group comparison)

**Script:** `plot_speed.py`

Compares feature extraction time of FPFH vs. Faster-PFH under single/multi-thread and w/ or w/o ground segmentation. Demonstrates annotations across `hue` groups using `hue_order` and grouped `pairs`.

```python
annot = Annotator(ax, pairs, data=df, x=x, y=y, order=order, hue=hue, hue_order=hue_order)
annot.new_plot(ax, pairs, data=df, x=x, y=y, order=order, hue=hue, hue_order=hue_order)
annot.configure(test='Mann-Whitney', verbose=2)
annot.apply_test()
annot.annotate()
```

```bash
python3 plot_speed.py
```

![Speed comparison](figs/speed_v2.png)

---

### 2. Box plot — log scale + `hue`

**Script:** `plot_bufferx_poseest_time.py`

Compares pose estimation time of RANSAC vs. KISS-Matcher across five datasets. Shows how to combine a **log-scale y-axis** with statannotations and LaTeX tick labels.

```python
plt.rcParams['text.usetex'] = True   # enable LaTeX rendering
ax = sns.boxplot(..., palette={"RANSAC": "#1f77b4", "KISS-Matcher": "#ff7f0e"})
plt.yscale('log')

annot = Annotator(ax, pairs, data=df, x=x, y=y, order=order, hue=hue, hue_order=hue_order)
annot.configure(test='Mann-Whitney', verbose=2)
annot.apply_test()
annot.annotate()
```

```bash
python3 plot_bufferx_poseest_time.py
```

![BufferX pose estimation time](figs/bufferx_poseest_time.png)

---

### 3. Box plot — pose errors (translation & rotation)

**Scripts:** `plot_trans_error.py` / `plot_rot_error.py`

Translation error [m] and rotation error [deg] across KITTI and MulRan datasets.

```bash
python3 plot_trans_error.py
python3 plot_rot_error.py
```

| Translation error | Rotation error |
|:-:|:-:|
| ![Translation error](figs/trans_error_v2.png) | ![Rotation error](figs/rot_error_v2.png) |

---

### 4. Box plot — two-group comparison

**Script:** `plot_vggt_slam_lc.py`

Compares ATE [m] with and without loop closure (LC) across different window sizes. A clean two-group example.

```bash
python3 plot_vggt_slam_lc.py
```

![VGGT SLAM with/without loop closure](figs/vggt_w_and_wo_lc.png)

---

### 5. Bar plot — success rate

**Script:** `plot_success_rate.py`

Uses `sns.barplot` instead of `sns.boxplot`. The statannotations API is identical — just swap the plot type.

```bash
python3 plot_success_rate.py
```

![Success rate](figs/success_rate.png)

---

### 6. Heatmap — radii sensitivity analysis

**Script:** `plot_radii_heatmap.py`

Uses `sns.heatmap` to visualize success rate and computation time across a grid of normal radius vs. FPFH radius hyperparameters. No statannotations here — included as a seaborn heatmap reference alongside the other examples.

```bash
python3 plot_radii_heatmap.py
```

![Radii analysis heatmap](figs/heatmap_0_3_succ.png)

---

## File Structure

```
.
├── example_basic_boxplot.py      # Minimal statannotations example (seaborn tips dataset)
├── plot_speed.py                 # Box plot: speed comparison, multi-hue
├── plot_bufferx_poseest_time.py  # Box plot: log scale + multi-dataset
├── plot_trans_error.py           # Box plot: translation error
├── plot_rot_error.py             # Box plot: rotation error w/ sensor config
├── plot_success_rate.py          # Bar plot: success rate
├── plot_vggt_slam_lc.py          # Box plot: w/ vs. w/o loop closure
├── plot_radii_heatmap.py         # Heatmap: hyperparameter sensitivity
├── variables.py                  # Shared plot styling constants
├── data/                         # Input data (raw txt files, pkl caches)
├── figs/                         # Representative output figures (for this README)
└── output/                       # Generated plots (gitignored)
```

---

## Key Pattern

Every script follows the same three-step pattern:

```python
# 1. Draw the seaborn plot
ax = sns.boxplot(data=df, x=x, y=y, hue=hue, ...)

# 2. Create the annotator with the same arguments
annot = Annotator(ax, pairs, data=df, x=x, y=y, hue=hue, ...)

# 3. Run the test and annotate
annot.configure(test='Mann-Whitney', verbose=2)
annot.apply_test()
annot.annotate()
```

`pairs` is a list of group tuples to compare. With `hue`, each element is a `(x_val, hue_val)` tuple:

```python
# Without hue
pairs = [("Thur", "Fri"), ("Thur", "Sat")]

# With hue
pairs = [
    (("Single-thread", "FPFH w/o GS"), ("Single-thread", "Faster-PFH w/o GS")),
    (("Multi-thread",  "FPFH w/ GS"),  ("Multi-thread",  "Faster-PFH w/ GS")),
]
```

---

## Reference

If you find these examples useful, please consider citing:

```bibtex
@article{lim2025kissmatcher,
  title   = {KISS-Matcher: Fast and Robust Point Cloud Registration Revisited},
  author  = {Lim, Hyungtae and Shi, Daebeom and Kim, Gunhee and Kim, Seungwon and Lu, Fan and Chen, Guang and Spring, Julien and Siegwart, Roland and Pfändtner, Jens and Schindler, Konrad and others},
  journal = {IEEE Robotics and Automation Letters},
  year    = {2025}
}
```
