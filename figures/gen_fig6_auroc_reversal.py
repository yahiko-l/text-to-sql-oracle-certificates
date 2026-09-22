"""Figure 6: the AUROC drop from weak to suite labels, for each score built on cell A and on cell D."""
from matplotlib.legend_handler import HandlerBase
from matplotlib.lines import Line2D
from paper_plot_style import *  # noqa: F401,F403

S = load("experiments/c8_baselines.json")["summary"]
# The palette of Figure 1, so the two cells wear the same blue and orange there and here.
INK1, GREY1, RULE = "#1F1F1F", "#6E6E6E", "#4A4A4A"
CELL_BLUE, CELL_ORANGE = "#2C6DB2", "#DC6A28"
BAND, GRID1 = "#F3F4F6", "#E4E4E4"
DOT = dict(ls="none", marker="o", ms=5, mec="white", mew=0.6)
# The four consistency scores, then the two likelihood scores below a gap.
Y = dict(zip(SCORES, [5.5, 4.5, 3.5, 2.5, 1.0, 0.0]))
CELLS = (("auroc_drop", 0.15, CELL_BLUE), ("auroc_drop_D", -0.15, CELL_ORANGE))


class Lollipop(HandlerBase):
    """Legend key drawn as the mark itself: a line from zero ending in a dot."""

    def create_artists(self, legend, orig, xdescent, ydescent, width, height, fontsize, trans):
        x0, x1, y = -xdescent, width - xdescent, height / 2 - ydescent
        color = orig.get_color()
        return [Line2D([x0, x1], [y, y], color=color, linewidth=1.2, transform=trans),
                Line2D([x1], [y], mfc=color, transform=trans, **DOT)]


fig, axes = plt.subplots(1, 4, figsize=(TEXT_WIDTH_IN, 2.4), sharey=True,
                         gridspec_kw={"wspace": 0.08})
for ax, t in zip(axes, CHECKPOINTS):
    e = S[f"{t}|question"]  # AUROC does not depend on the split scheme
    for i, sc in enumerate(SCORES):
        if i % 2 == 1:
            ax.axhspan(Y[sc] - 0.5, Y[sc] + 0.5, color=BAND, linewidth=0, zorder=0)
        for key, off, color in CELLS:
            v, y = e[f"{sc}|{key}"] * 100, Y[sc] + off
            ax.plot([0, v], [y, y], color=color, linewidth=1.2, solid_capstyle="butt", zorder=2)
            ax.plot([v], [y], mfc=color, zorder=4, **DOT)
    ax.axvline(0, color=RULE, linewidth=0.8, zorder=1.5)
    ax.xaxis.grid(True, color=GRID1, linewidth=0.5)
    ax.set_axisbelow(True)
    ax.set_xlim(-8.5, 11.5)
    ax.set_xticks([-5, 0, 5, 10])
    ax.set_ylim(-0.5, 6.05)
    ax.set_title(CHECKPOINT_LABEL[t], loc="left", fontsize=FONT_SIZE - 0.5, color=INK1, pad=4)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GREY1)
    ax.tick_params(axis="x", length=2.5, width=0.6, colors=GREY1, labelcolor=RULE,
                   labelsize=FONT_SIZE - 1)
    ax.tick_params(axis="y", length=0, pad=4, labelcolor=INK1)
axes[0].set_yticks([Y[s] for s in SCORES])
axes[0].set_yticklabels([SCORE_LABEL[s] for s in SCORES])
fig.supxlabel("drop in AUROC when the labels switch from weak to suite (points)",
              fontsize=FONT_SIZE - 0.5, color=INK1, y=-0.02)
fig.legend([Line2D([], [], color=c) for _, _, c in CELLS],
           ["cell A, built on the original-database partition",
            "cell D, built on the suite partition"],
           handler_map={Line2D: Lollipop()}, loc="lower center", ncol=2,
           bbox_to_anchor=(0.5, -0.15), fontsize=FONT_SIZE - 1, handletextpad=0.6,
           columnspacing=2.4, handlelength=1.8)
save_fig(fig, "fig6_auroc_reversal")
