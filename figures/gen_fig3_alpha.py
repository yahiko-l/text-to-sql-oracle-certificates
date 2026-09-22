"""Figure 3: suite-oracle risk of cells A and D against nominal alpha, one panel per checkpoint."""
import numpy as np
from paper_plot_style import *  # noqa: F401,F403

curve = load("experiments/c4_alpha_curve.json")["alpha_curve"]
alphas = [0.05, 0.1, 0.15, 0.2]
fig, axes2 = plt.subplots(2, 4, figsize=(TEXT_WIDTH_IN, 4.39), sharex=True, sharey="row", gridspec_kw={"wspace": 0.12, "hspace": 0.18, "height_ratios": [1.3, 1.0]})
fig.subplots_adjust(left=0.075, right=0.995, top=0.95, bottom=0.145)
axes = axes2[0]
for ax, axr, t in zip(axes, axes2[1], CHECKPOINTS):
    Dans = [curve[f"{t}|question|alpha={a}"]["D_answer_rate"] for a in alphas]
    A = [curve[f"{t}|question|alpha={a}"]["A_risk_strong"] for a in alphas]
    D = [curve[f"{t}|question|alpha={a}"]["D_risk_strong"] for a in alphas]
    Aans = [curve[f"{t}|question|alpha={a}"]["A_answer_rate"] for a in alphas]
    ax.plot([0, 0.25], [0, 0.25], color=BASELINE, linewidth=0.8, zorder=0)
    ax.plot(alphas, A, marker="o", color=BLUE, label="cell A (current practice)" if t == CHECKPOINTS[0] else None, markeredgecolor=SURFACE, markeredgewidth=0.6)
    ax.plot(alphas, D, marker="s", linestyle="--", color=ORANGE, label="cell D (multi-instance)" if t == CHECKPOINTS[0] else None, markeredgecolor=SURFACE, markeredgewidth=0.6)
    sat = [(a, v) for a, v, ar in zip(alphas, A, Aans) if ar >= 0.999]
    if sat:
        ax.scatter([p[0] for p in sat], [p[1] for p in sat], s=34, facecolor=SURFACE, edgecolor=BLUE, linewidth=1.0, zorder=4,
                   label="cell A answers every question" if t == CHECKPOINTS[0] else None)
    ax.set_xticks(alphas)
    ax.set_xticklabels(["0.05", "0.10", "0.15", "0.20"])
    if t != CHECKPOINTS[0]:
        ax.tick_params(labelleft=False)
    ax.set_xlim(0.03, 0.22)
    ax.set_ylim(0, 0.29)
    ax.set_title(CHECKPOINT_LABEL[t], loc="left", fontsize=FONT_SIZE - 0.5, color=INK2)
    style_axes(ax)
    axr.plot(alphas, [curve[f"{t}|question|alpha={a}"]["A_answer_rate"] for a in alphas], marker="o", color=BLUE, markeredgecolor=SURFACE, markeredgewidth=0.6)
    axr.plot(alphas, Dans, marker="s", linestyle="--", color=ORANGE, markeredgecolor=SURFACE, markeredgewidth=0.6)
    axr.set_ylim(-0.03, 1.05)
    axr.set_xlabel("nominal $\\alpha$", fontsize=FONT_SIZE - 0.5)
    style_axes(axr)
    if t != CHECKPOINTS[0]:
        axr.tick_params(labelleft=False)
axes[0].set_ylabel("risk under the suite oracle", fontsize=FONT_SIZE - 0.5)
axes2[1][0].set_ylabel("answer rate", fontsize=FONT_SIZE - 0.5)
h, l = axes[0].get_legend_handles_labels()
fig.legend(h, l, loc="lower center", ncol=3, bbox_to_anchor=(0.5, 0.0), fontsize=FONT_SIZE - 1, handlelength=1.4)
save_fig(fig, "fig3_alpha")
