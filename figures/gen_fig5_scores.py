"""Figure 5: what the certificate reports and what it carries, for six confidence scores."""
import numpy as np
from matplotlib.lines import Line2D
from paper_plot_style import *  # noqa: F401,F403

S = load("experiments/c8_baselines.json")["summary"]
BAND = "#f4f4f2"
ROWS = (("question", 0.115, 0.200, 21, True), ("database", -0.150, 0.085, 14, False))
fig, axes = plt.subplots(1, 4, figsize=(TEXT_WIDTH_IN, 2.7), sharey=True,
                         gridspec_kw={"wspace": 0.08})
y = np.arange(len(SCORES))[::-1]
for ax, t in zip(axes, CHECKPOINTS):
    for yi, sc in zip(y, SCORES):
        if yi % 2 == 0:
            ax.axhspan(yi - 0.5, yi + 0.5, color=BAND, linewidth=0, zorder=0)
        for sp, off, h, ms, solid in ROWS:
            e = S[f"{t}|{sp}"]
            fit, a = e[f"{sc}|risk_A_fit"] * 100, e[f"{sc}|risk_A_strong"] * 100
            ax.barh(yi + off, a - fit, left=fit, height=h, color=BLUE, linewidth=0, zorder=3)
            ax.scatter([e[f"{sc}|risk_D_strong"] * 100], [yi + off], s=ms, zorder=4,
                       color=ORANGE if solid else SURFACE, edgecolor=SURFACE if solid else ORANGE,
                       linewidth=0.7 if solid else 0.9)
    ax.axvline(10, color=INK2, linewidth=0.7, linestyle=(0, (2.5, 2)), zorder=5)
    ax.xaxis.grid(True, color="#e8e8e5", linewidth=0.5, zorder=1)
    ax.set_axisbelow(False)
    ax.set_xlim(3.5, 21.5)
    ax.set_xticks([5, 10, 15, 20])
    ax.set_ylim(-0.5, len(SCORES) + 0.3)
    ax.set_title(CHECKPOINT_LABEL[t], loc="left", fontsize=FONT_SIZE - 0.5, color=INK,
                 fontweight="bold", pad=5)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(BASELINE)
    ax.tick_params(axis="x", length=2.5, width=0.6, colors=INK2, labelsize=FONT_SIZE - 1)
    ax.tick_params(axis="y", length=0, pad=4)
axes[0].set_yticks(y)
axes[0].set_yticklabels([SCORE_LABEL[s] for s in SCORES])
axes[0].text(10.5, len(SCORES) - 0.18, "nominal 10", ha="left", va="center",
             fontsize=FONT_SIZE - 1, color=INK2, style="italic")
fig.supxlabel("held-out risk (percent of questions) at nominal $\\alpha = 0.10$",
              fontsize=FONT_SIZE, y=-0.02)
handles = [Line2D([], [], color=BLUE, linewidth=4.5, solid_capstyle="butt"),
           Line2D([], [], ls="none", marker="o", markersize=4.2, color=ORANGE,
                  markeredgecolor=SURFACE, markeredgewidth=0.7)]
fig.legend(handles, ["cell A, from the risk it reports to the risk it carries",
                     "cell D under the suite oracle"],
           loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.15), fontsize=FONT_SIZE - 1,
           handletextpad=0.5, columnspacing=2.4, handlelength=1.5)
save_fig(fig, "fig5_scores")
