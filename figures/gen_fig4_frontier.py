"""Figure 4: highest answer rate reachable by cells B and D under a common empirical risk ceiling."""
import numpy as np
from matplotlib.lines import Line2D
from paper_plot_style import *  # noqa: F401,F403

fr = load("experiments/c4_frontier.json")["frontier_B_vs_D_common_risk_ceiling"]
CEILINGS = [0.025, 0.05, 0.075, 0.10, 0.125, 0.15]
X_MAX = 0.155
CELLS = [("B", "cell B (suite labels, original partition)", dict(color=GRAY_DARK, linestyle="--"), "s"),
         ("D", "cell D (suite labels, suite partition)", dict(color=BLUE, linestyle="-"), "o")]


def mean_frontier(stairs, cell, xs):
    """Three-seed mean of the highest answer rate among a cell's frontier corners with risk at most x."""
    return np.mean([[max(answered / s["n"] for wrong, answered in s[cell] if wrong / s["n"] <= x) for x in xs]
                    for s in stairs.values()], axis=0)


fig, axes = plt.subplots(1, 4, figsize=(TEXT_WIDTH_IN, 2.70), sharey=True, gridspec_kw={"wspace": 0.12})
fig.subplots_adjust(left=0.07, right=0.995, top=0.92, bottom=0.215)
for ax, t in zip(axes, CHECKPOINTS):
    stairs = fr[t]["staircase_by_seed"]
    for cell, _, line, marker in CELLS:
        # The mean frontier moves only where some seed's frontier has a corner.
        xs = sorted({0.0, X_MAX} | {wrong / s["n"] for s in stairs.values() for wrong, _ in s[cell] if wrong / s["n"] <= X_MAX})
        ax.step(xs, mean_frontier(stairs, cell, xs), where="post", **line)
        ax.plot(CEILINGS, mean_frontier(stairs, cell, CEILINGS), ls="none", marker=marker, color=line["color"],
                markeredgecolor=SURFACE, markeredgewidth=0.6)
    ax.set_xlim(0, X_MAX)
    ax.set_xticks([0, 0.05, 0.10, 0.15])
    ax.set_xticklabels(["0", "0.05", "0.10", "0.15"])
    ax.set_ylim(-0.03, 1.03)
    ax.set_title(CHECKPOINT_LABEL[t], loc="left", fontsize=FONT_SIZE - 0.5, color=INK2)
    ax.set_xlabel("empirical risk ceiling", fontsize=FONT_SIZE - 0.5)
    style_axes(ax)
axes[0].set_ylabel("highest answer rate", fontsize=FONT_SIZE - 0.5)
handles = [Line2D([], [], marker=marker, markeredgecolor=SURFACE, markeredgewidth=0.6, **line) for _, _, line, marker in CELLS]
fig.legend(handles, [label for _, label, _, _ in CELLS], loc="lower center", ncol=2, bbox_to_anchor=(0.5, 0.0),
           fontsize=FONT_SIZE - 1, handlelength=1.4)
save_fig(fig, "fig4_frontier")
