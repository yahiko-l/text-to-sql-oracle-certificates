"""Figure 2: suite-oracle risk and answer rate of the four cells per checkpoint, both split schemes."""
from functools import lru_cache

import numpy as np
from paper_plot_style import *  # noqa: F401,F403

SEEDS = [101, 202, 303]
SHORT = {"kwai-autosql-32b": "Kwai-32B", "kwai-autosql-14b": "Kwai-14B", "omnisql-32b": "Omni-32B", "xiyansql-32b": "XiYan-32B"}
SPLITS = [("question", "results_official"), ("database", "results_official_dbsplit")]
METRICS = [("marginal_risk_strong", "risk under the suite oracle", 0.25, [0, 0.05, 0.10, 0.15, 0.20, 0.25]),
           ("answer_rate", "answer rate", 1.0, [0, 0.2, 0.4, 0.6, 0.8, 1.0])]
INK1, GREY1, RULE, GRID1 = "#1F1F1F", "#6E6E6E", "#4A4A4A", "#E4E4E4"
# The blue and orange of Figure 1 for cells A and D, and a lighter step of each for the cell that keeps
# the same partition: B the original-database partition, C the suite partition.
CELLS = [("A", "score=single|calib=single", "#2C6DB2"), ("B", "score=single|calib=multi", "#86A9D6"),
         ("C", "score=multi|calib=single", "#F2B48C"), ("D", "score=multi|calib=multi", "#DC6A28")]
W = 0.19
NOMINAL = 0.10


@lru_cache(maxsize=None)
def cells(tag, suffix, seed):
    return load(f"experiments/c4_{tag}_seed{seed}_{suffix}.json")["cells"]


fig, axes = plt.subplots(2, 2, figsize=(TEXT_WIDTH_IN, 4.3), gridspec_kw={"hspace": 0.48, "wspace": 0.2})
fig.subplots_adjust(left=0.075, right=0.995, top=0.875, bottom=0.06)
x = np.arange(len(CHECKPOINTS))
for r, (split, suffix) in enumerate(SPLITS):
    for c, (metric, ylabel, ymax, yticks) in enumerate(METRICS):
        ax = axes[r, c]
        for i, (name, key, color) in enumerate(CELLS):
            v = np.array([[cells(t, suffix, s)[key][metric]["mean"] for s in SEEDS] for t in CHECKPOINTS])
            mean, xs = v.mean(axis=1), x + (i - 1.5) * W
            ax.bar(xs, mean, W, color=color, edgecolor="white", linewidth=0.8, zorder=2, label=f"cell {name}")
            ax.errorbar(xs, mean, yerr=[mean - v.min(axis=1), v.max(axis=1) - mean], fmt="none", ecolor=RULE,
                        elinewidth=0.7, zorder=3)
        if metric == "marginal_risk_strong":
            ax.axhline(NOMINAL, color=GREY1, linewidth=0.9, linestyle=(0, (3, 2)), zorder=4)
            ax.text(len(CHECKPOINTS) - 0.42, NOMINAL + 0.004, r"$\alpha$", ha="right", va="bottom",
                    fontsize=FONT_SIZE - 1, color=GREY1)
        ax.set_xlim(-0.5, len(CHECKPOINTS) - 0.4)
        ax.set_ylim(0, ymax)
        ax.set_yticks(yticks)
        ax.set_xticks(x)
        ax.set_xticklabels([SHORT[t] for t in CHECKPOINTS])
        ax.yaxis.grid(True, color=GRID1, linewidth=0.5)
        ax.set_axisbelow(True)
        for side in ("left", "right", "top"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(GREY1)
        ax.tick_params(axis="x", length=0, pad=4, labelcolor=INK1, labelsize=FONT_SIZE - 1)
        ax.tick_params(axis="y", length=0, pad=3, labelcolor=RULE, labelsize=FONT_SIZE - 1)
        ax.set_ylabel(ylabel, fontsize=FONT_SIZE - 0.5, color=INK1)
        ax.set_title(f"{split} splits", loc="left", fontsize=FONT_SIZE - 0.5, color=INK1, pad=6)
h, l = axes[0, 0].get_legend_handles_labels()
fig.legend(h, l, loc="lower center", bbox_to_anchor=(0.5, 0.935), ncol=4, fontsize=FONT_SIZE - 1,
           handlelength=1.0, handleheight=1.0, handletextpad=0.45, columnspacing=1.8)
save_fig(fig, "fig2_cells")
