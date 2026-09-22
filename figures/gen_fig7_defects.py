"""Figure 7: (a) suspected reference-query defect cases by schema (full census); (b) semantic-error share by mechanical difference signature (disagreement census)."""
import collections
from paper_plot_style import *  # noqa: F401,F403

c7 = load("experiments/c7_semantic_audit.json")
c6 = load("experiments/c6_semantic_audit.json")
# The palette of Figure 1, whose panel (c) gives these two labels this orange and this blue.
INK1, GREY1, RULE, GRID1 = "#1F1F1F", "#6E6E6E", "#4A4A4A", "#E4E4E4"
DEFECT, SEMANTIC, TRACK = "#DC6A28", "#2C6DB2", "#DCE6F2"
MECH_TEXT = {"partial_overlap": "partial overlap", "gold_empty": "reference returns no rows",
             "gold_subset_of_rep": "reference is a subset of returned", "disjoint": "disjoint results",
             "duplicate_multiplicity_only": "duplicate multiplicity only",
             "rep_subset_of_gold": "returned is a subset of reference",
             "col_count_differs": "column count differs", "rep_empty": "returned query returns no rows",
             "row_order_only": "row order only"}

cases = collections.Counter(c["db"] for c in c7["cases"] if c["label"] == "gold_defect")
questions = collections.defaultdict(set)
for c in c7["cases"]:
    if c["label"] == "gold_defect":
        questions[c["db"]].add(c["qid"])
dbs = [d for d, _ in cases.most_common()]
mech = c6["by_mechanism"]
order = sorted(mech, key=lambda k: -mech[k]["share_semantic_error"])

W, H = TEXT_WIDTH_IN, 2.75
BOTTOM, HEIGHT = 0.42, 1.95
fig = plt.figure(figsize=(W, H))
ax1 = fig.add_axes([1.45 / W, BOTTOM / H, 1.40 / W, HEIGHT / H])
ax2 = fig.add_axes([4.95 / W, BOTTOM / H, 1.05 / W, HEIGHT / H])

for yi, d in zip(range(len(dbs) - 1, -1, -1), dbs):
    n = cases[d]
    ax1.plot([0, n], [yi, yi], color=DEFECT, linewidth=1.2, solid_capstyle="butt", zorder=2)
    ax1.plot([n], [yi], ls="none", marker="o", ms=4.6, mfc=DEFECT, mec="white", mew=0.6, zorder=3)
    ax1.text(n + 3, yi, f"{n} ({len(questions[d])})", va="center", ha="left",
             fontsize=FONT_SIZE - 1, color=RULE)
ax1.set_yticks(range(len(dbs) - 1, -1, -1))
ax1.set_yticklabels(dbs)
ax1.set_ylim(-0.6, len(dbs) - 0.4)
ax1.set_xlim(0, 80)
ax1.set_xticks([0, 20, 40, 60, 80])
ax1.set_xlabel("cases, with distinct questions in parentheses", fontsize=FONT_SIZE - 1,
               color=INK1, labelpad=3)

for yi, k in zip(range(len(order) - 1, -1, -1), order):
    m = mech[k]
    ax2.barh(yi, 100, height=0.44, color=TRACK, linewidth=0, zorder=1)
    ax2.barh(yi, m["share_semantic_error"] * 100, height=0.44, color=SEMANTIC, linewidth=0, zorder=2)
    ax2.text(104, yi, f"{m['semantic_error']} of {m['cases']}", va="center", ha="left",
             fontsize=FONT_SIZE - 1, color=RULE)
ax2.set_yticks(range(len(order) - 1, -1, -1))
ax2.set_yticklabels([MECH_TEXT[k] for k in order])
ax2.set_ylim(-0.6, len(order) - 0.4)
ax2.set_xlim(0, 100)
ax2.set_xticks([0, 25, 50, 75, 100])
ax2.set_xlabel("share of cases labelled semantic error (%)", fontsize=FONT_SIZE - 1, color=INK1,
               labelpad=3)

for ax in (ax1, ax2):
    ax.xaxis.grid(True, color=GRID1, linewidth=0.5)
    ax.set_axisbelow(True)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GREY1)
    ax.tick_params(axis="x", length=2.5, width=0.6, colors=GREY1, labelcolor=RULE,
                   labelsize=FONT_SIZE - 1)
    ax.tick_params(axis="y", length=0, pad=4, labelcolor=INK1, labelsize=FONT_SIZE - 1)

# Tag and title on one baseline, from the left edge of each panel's labels, as in Figure 1.
fig.canvas.draw()
R = fig.canvas.get_renderer()
for ax, tag, title in ((ax1, "(a)", "Suspected reference-query defects by schema"),
                       (ax2, "(b)", "Semantic errors by result difference")):
    left = min(t.get_window_extent(R).x0 for t in ax.get_yticklabels()) / fig.dpi
    y = (BOTTOM + HEIGHT + 0.16) / H
    t = fig.text(left / W, y, tag, fontsize=FONT_SIZE, fontweight="bold", color=INK1,
                 ha="left", va="baseline")
    fig.text((t.get_window_extent(R).x1 / fig.dpi + 0.06) / W, y, title, fontsize=FONT_SIZE - 0.5,
             color=INK1, ha="left", va="baseline")
save_fig(fig, "fig7_defects")
