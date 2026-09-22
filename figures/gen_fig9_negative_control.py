"""Figure 9 (appendix): false-schema negative control against the main pools."""
import numpy as np
from paper_plot_style import *  # noqa: F401,F403

SEEDS = [101, 202, 303]
KEY = "score=single|calib=single"
# Figure 1's blue in two steps: the main pools as a light tint behind the control in the full blue.
INK1, GREY1, RULE, GRID1 = "#1F1F1F", "#6E6E6E", "#4A4A4A", "#E4E4E4"
MAIN, CONTROL = "#C4D6E9", "#2C6DB2"
NOMINAL = 0.10
fig, axes = plt.subplots(1, 3, figsize=(TEXT_WIDTH_IN, 2.3), gridspec_kw={"wspace": 0.35})
x = np.arange(len(CHECKPOINTS))
w = 0.36
for ax, (metric, getter, ylabel, ylim) in zip(axes, [
        ("top1", lambda d: d["top1_accuracy_under_strong_oracle"], "top-1 accuracy under the suite oracle", (0, 1.0)),
        ("risk", lambda d: d["cells"][KEY]["marginal_risk_strong"]["mean"], "cell A risk under the suite oracle", (0, 0.3)),
        ("answer", lambda d: d["cells"][KEY]["answer_rate"]["mean"], "cell A answer rate", (0, 1.0))]):
    main = [np.mean([getter(load(f"experiments/c4_{t}_seed{s}_results_official.json")) for s in SEEDS]) for t in CHECKPOINTS]
    ctrl = [getter(load(f"experiments/c4_{t}_falseschema_results_official.json")) for t in CHECKPOINTS]
    ax.bar(x - w / 2, main, w * 0.92, color=MAIN, linewidth=0, zorder=2, label="main pools (3-seed mean)")
    ax.bar(x + w / 2, ctrl, w * 0.92, color=CONTROL, linewidth=0, zorder=2, label="false-schema control")
    for xi, v in zip(x + w / 2, ctrl):
        y = max(v, ylim[1] * 0.02)
        if metric == "risk" and v > NOMINAL - 0.03:  # clear the nominal line
            y = max(v, NOMINAL) + 0.003
        ax.text(xi, y + ylim[1] * 0.02, f"{v:.3f}" if v < 0.1 else f"{v:.2f}", ha="center", va="bottom",
                fontsize=FONT_SIZE - 1, color=RULE, zorder=4)
    if metric == "risk":
        ax.axhline(NOMINAL, color=GREY1, linewidth=0.8, linestyle=(0, (3, 2)), zorder=3)
    ax.set_ylim(*ylim)
    ax.set_xticks(x)
    ax.set_xticklabels([CHECKPOINT_LABEL[t] for t in CHECKPOINTS], fontsize=FONT_SIZE - 1, rotation=30, ha="right")
    ax.set_ylabel(ylabel, fontsize=FONT_SIZE - 1, color=INK1)
    ax.yaxis.grid(True, color=GRID1, linewidth=0.5)
    ax.set_axisbelow(True)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GREY1)
    ax.tick_params(axis="x", length=0, pad=2, labelcolor=RULE)
    ax.tick_params(axis="y", length=0, pad=3, labelcolor=RULE)
h, l = axes[0].get_legend_handles_labels()
fig.legend(h, l, loc="lower center", bbox_to_anchor=(0.5, 0.93), ncol=2, fontsize=FONT_SIZE - 1,
           handlelength=1.2, columnspacing=2.4)
save_fig(fig, "fig9_negative_control")
