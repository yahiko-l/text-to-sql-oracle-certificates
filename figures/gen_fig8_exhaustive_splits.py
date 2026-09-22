"""Figure 8 (appendix): GAP and D-minus-A over all 92,378 schema-disjoint database splits, per checkpoint and seed."""
import numpy as np
from paper_plot_style import *  # noqa: F401,F403

E = load("experiments/c4_exhaustive_db_splits.json")["models"]
fig, axes = plt.subplots(1, 2, figsize=(TEXT_WIDTH_IN, 2.82), sharey=True, gridspec_kw={"wspace": 0.08})
fig.subplots_adjust(left=0.165, right=0.995, top=0.915, bottom=0.255)
y = np.arange(len(CHECKPOINTS))[::-1]
for ax, (metric, title) in zip(axes, [("GAP", "GAP (points)"), ("REPAIR", "D minus A (points)")]):
    for yi, t in zip(y, CHECKPOINTS):
        per = E[f"{t}|tie=first"]["per_seed"]
        for k, (seed, v) in enumerate(sorted(per.items())):
            off = (k - 1) * 0.22
            lo, hi, m = v[f"{metric}_p2.5"] * 100, v[f"{metric}_p97.5"] * 100, v[f"{metric}_mean"] * 100
            col = ORDINAL_BLUE3[k]
            ax.plot([lo, hi], [yi + off, yi + off], color=col, linewidth=1.2, linestyle=["-", "--", ":"][k], solid_capstyle="round",
                    label=f"seed {seed}" if (yi == y[0] and metric == "GAP") else None)
            ax.scatter([m], [yi + off], s=18, marker=["o", "s", "^"][k], color=col, zorder=3, edgecolor=SURFACE, linewidth=0.6)
        fk = f"{metric}_positive_fraction" if metric == "GAP" else f"{metric}_negative_fraction"
        fr = [per[s][fk] * 100 for s in sorted(per)]
        ax.text(0.99, yi, f"{min(fr):.1f}\u2013{max(fr):.1f}% same sign", va="center", ha="right", fontsize=FONT_SIZE - 1, color=INK2,
                transform=ax.get_yaxis_transform())
    ax.axvline(0, color=BASELINE, linewidth=0.8, zorder=0)
    ax.set_title(title, loc="left", fontsize=FONT_SIZE - 0.5, color=INK2)
    style_axes(ax, ygrid=False)
# Each panel runs far enough right that its share labels clear every interval and the zero line.
axes[0].set_xlim(-2, 30)
axes[1].set_xlim(-21, 24)
axes[0].set_yticks(y)
axes[0].set_yticklabels([CHECKPOINT_LABEL[t] for t in CHECKPOINTS])
mid = (axes[0].get_position().x0 + axes[1].get_position().x1) / 2
fig.supxlabel("2.5th to 97.5th percentile over splits, mean marked", x=mid, y=0.105, fontsize=FONT_SIZE - 0.5)
h, l = axes[0].get_legend_handles_labels()
fig.legend(h, l, loc="lower center", ncol=3, bbox_to_anchor=(mid, 0.0), fontsize=FONT_SIZE - 1, handlelength=1.4)
save_fig(fig, "fig8_exhaustive_splits")
