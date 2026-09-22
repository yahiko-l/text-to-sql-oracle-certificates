#!/usr/bin/env python3
"""Figure 1, version 2, of "Certified Against Which Oracle?".

(a) Held-out risk of the current-practice certificate at nominal alpha = 0.10 on the two checkpoints
    the experts audited on both sides of the suite oracle: under its own labels, under the suite
    oracle and under the expert labels (Section 7.1 and Table A11; seed 101, post hoc).
(b) GAP = risk under a yardstick minus the risk the certificate reports on its own labels,
    alpha = 0.10, question splits: three-seed means under the preregistered suite labels and the
    rejected-side relabellings of Table A4, and the expert labels of (a) on the two checkpoints
    they judged (Table A11; seed 101). All but the first yardstick are post hoc.
(c) Labels of every answer the suite oracle rejects (Table A3; AI audit, post hoc).

Outputs figure1_v2.pdf (vector, TrueType fonts, no Type 3) and figure1_v2.png (300 dpi).
Drawn at the 6.5 in text width: \\includegraphics[width=\\textwidth]{figure1_v2.pdf}.
"""
from decimal import ROUND_HALF_UP, Decimal

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon, Rectangle
from matplotlib.transforms import blended_transform_factory

mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Liberation Serif", "Times New Roman", "Nimbus Roman", "STIXGeneral"],
    "mathtext.fontset": "stix",
    "font.size": 8,
    "axes.linewidth": 0.6,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "savefig.dpi": 300,
})
MINUS = "\u2212"

# ================================================================================= data
# (a) Section 7.1 levels and Table A11, question splits, seed 101, percent of held-out questions.
RISK_MODELS = ["Kwai-32B", "XiYan-32B"]
RISK_REPORTED = [9.84, 9.89]      # under the certificate's own shipped-database labels
RISK_SUITE = [20.25, 12.96]       # under the suite oracle
RISK_EXPERT = [17.21, 19.99]      # under the expert labels (suite-label fallback for unjudged items)
RISK_GAP_RANGE = [(6.19, 7.94), (9.25, 11.93)]  # expert GAP over the nine conventions of Table A11

# (b) Table A4, question splits, alpha = 0.10, points, three-seed means.
MODELS = ["Kwai-32B", "Kwai-14B", "Omni-32B", "XiYan-32B"]
GAP = {
    "prereg": [10.23, 8.08, 9.50, 3.11],     # preregistered suite labels
    "disagr": [2.26, 2.37, 2.54, 1.00],      # rejected side relabelled, disagreement census (narrow)
    "full":   [-4.99, -3.37, -4.25, -4.22],  # rejected side relabelled, full census (narrow)
    "expert": [7.37, None, None, 10.10],     # Table A11, seed 101, suite-label fallback for unjudged items
}
# Expert GAP over the nine conventions of Table A11, on the two checkpoints the experts judged.
EXPERT_RANGE = [RISK_GAP_RANGE[0], None, None, RISK_GAP_RANGE[1]]

# (c) Table A3, answer occurrences; cases and questions from Table 3.
CATS = ["semantic error", "suspected reference defect", "underspecified question",
        "synthetic-instance defect", "comparator artefact"]
POPS = [  # name, answers, distinct cases, questions, answer counts in CATS order
    ("Disagreement census", 521, 240, 99, [136, 107, 195, 83, 0]),
    ("Full census", 2779, 742, 203, [972, 887, 723, 161, 36]),
]
for _, n, _, _, c in POPS:
    assert sum(c) == n

# Optional split of the orange segment: number of suspected-reference-defect ANSWERS whose
# question the blinded expert audit judged defective (Appendix G). Fill in from the audit key,
# e.g. {"Disagreement census": 64, "Full census": 512}; None draws the segment whole.
REF_CONFIRMED = None

# ================================================================================= style
INK, GREY, DARK = "#1F1F1F", "#6E6E6E", "#3A3A3A"
BLUE, ORANGE, RED = "#2C6DB2", "#DC6A28", "#B2182B"
ORANGE_LIGHT = "#F2B48C"
CAT_COLORS = [BLUE, ORANGE, "#B9D5BF", "#EEDBA4", "#B784A8"]
CAT_TEXT = ["white", "white", INK, INK, INK]
BAND_ALPHA = [0.20, 0.20, 0.45, 0.55, 0.35]
FS_TITLE, FS_LABEL, FS_NOTE, FS_VALUE = 8.5, 8.0, 7.2, 6.6

SERIES = [  # key, legend label, marker, stem colour, stem linestyle, print value?
    ("prereg", "preregistered suite labels",
     dict(marker="o", ms=5.0, mfc=DARK, mec=DARK), "#A0A0A0", "-", True),
    ("disagr", "rejected side relabelled: disagreement census",
     dict(marker="s", ms=4.5, mfc="white", mec=BLUE, mew=1.1), "#86A9D6", "-", True),
    ("full", "rejected side relabelled: full census",
     dict(marker="s", ms=4.5, mfc=BLUE, mec=BLUE), BLUE, "-", True),
    ("expert", "two SQL experts (seed 101, range)",
     dict(marker="*", ms=8.5, mfc=RED, mec=RED), RED, "-", True),
]
OFFSETS = [0.30, 0.10, -0.10, -0.30]


def fmt(v, signed=True, nd=1):
    """Round half away from zero, as in the paper's tables (20.25 -> 20.3), with a true minus."""
    q = Decimal(str(v)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
    return (f"{q:+}" if signed else f"{q}").replace("-", MINUS)


# ================================================================================= layout
# All positions in inches from the lower left corner of the figure.
W, H = 6.5, 4.30
fig = plt.figure(figsize=(W, H))
R = fig.canvas.get_renderer()

TAG_LEFT = 0.22
TOP_TITLE_Y = H - 0.17
A_LEFT, A_RIGHT, A_TOP, A_BOTTOM = 0.52, 2.40, H - 0.90, 0.42
RC_LEFT, RC_RIGHT = 3.30, 6.42          # axes of (b); (c) runs from the labels of (b) to RC_RIGHT
B_TOP, B_BOTTOM = H - 0.57, 2.05
C_TITLE_Y = 1.42
C_BAR_RIGHT = 6.12                      # leaves room to label the comparator sliver beside the bar
C_BAR_H = 0.15
C_BAR_Y = [0.72, 0.32]                  # bottoms of the disagreement-census and full-census bars


def axes_in(left, bottom, width, height):
    return fig.add_axes([left / W, bottom / H, width / W, height / H])


def text_end(t):
    return t.get_window_extent(R).x1 / fig.dpi


def panel_title(left_in, y_in, tag, text):
    """Bold tag and title on one baseline; returns where the title text starts."""
    t = fig.text(left_in / W, y_in / H, tag, fontsize=FS_TITLE + 0.5, fontweight="bold",
                 ha="left", va="baseline")
    x_text = text_end(t) + 0.06
    fig.text(x_text / W, y_in / H, text, fontsize=FS_TITLE, ha="left", va="baseline")
    return x_text


# ================================================================================= (a)
axA = axes_in(A_LEFT, A_BOTTOM, A_RIGHT - A_LEFT, A_TOP - A_BOTTOM)
for g, (rep, sui, exp_, (glo, ghi)) in enumerate(zip(RISK_REPORTED, RISK_SUITE, RISK_EXPERT,
                                                     RISK_GAP_RANGE)):
    lo, hi = rep + glo, rep + ghi
    axA.plot([g, g], [min(rep, sui, lo), max(sui, hi)], color="#D0D0D0", lw=1.0, zorder=1)
    axA.plot([g, g], [lo, hi], color=RED, lw=1.8, alpha=0.45, solid_capstyle="butt", zorder=2)
    for ye in (lo, hi):
        axA.plot([g - 0.07, g + 0.07], [ye, ye], color=RED, lw=0.9, alpha=0.6, zorder=2)
    axA.plot([g], [rep], ls="none", marker="o", ms=6.0, mfc="white", mec=DARK, mew=1.1, zorder=3)
    axA.plot([g], [sui], ls="none", marker="o", ms=5.8, mfc=DARK, mec=DARK, zorder=3)
    axA.plot([g], [exp_], ls="none", marker="*", ms=11.0, mfc=RED, mec=RED, zorder=4)
    axA.text(g, rep - 0.8, fmt(rep, signed=False), ha="center", va="top", fontsize=7.2,
             color="#4A4A4A")
    axA.text(g + 0.14, sui, fmt(sui, signed=False), ha="left", va="center", fontsize=7.2,
             color="#4A4A4A")
    axA.text(g + 0.17, exp_, fmt(exp_, signed=False), ha="left", va="center", fontsize=7.2,
             color=RED, fontweight="bold")

axA.axhline(10, color=GREY, lw=0.8, ls=(0, (3, 2)), zorder=1)
axA.text(1.72, 9.45, r"nominal $\alpha$", ha="right", va="top", fontsize=6.6, color=GREY,
         style="italic")
axA.set_xlim(-0.55, 1.75)
axA.set_ylim(0, 25)
axA.set_yticks([0, 5, 10, 15, 20, 25])
axA.set_xticks(range(len(RISK_MODELS)))
axA.set_xticklabels(RISK_MODELS, fontsize=FS_LABEL)
axA.tick_params(axis="x", length=0, pad=4)
axA.tick_params(axis="y", length=0, labelsize=7.5, pad=3)
axA.grid(axis="y", color="#E4E4E4", lw=0.5)

# ================================================================================= (b)
axB = axes_in(RC_LEFT, B_BOTTOM, RC_RIGHT - RC_LEFT, B_TOP - B_BOTTOM)
n_rows = len(MODELS)
for i in range(n_rows):
    yc = n_rows - 1 - i
    if i % 2 == 0:
        axB.axhspan(yc - 0.5, yc + 0.5, color="#F3F4F6", lw=0, zorder=0)
    for (key, _, mstyle, stem, ls, show), off in zip(SERIES, OFFSETS):
        v, y = GAP[key][i], yc + off
        if v is None:
            continue
        if key == "expert":  # drawn as in (a): the star on its range over the nine conventions
            lo, hi = EXPERT_RANGE[i]
            axB.plot([0, lo], [y, y], color=RED, lw=1.0, alpha=0.5, solid_capstyle="butt", zorder=2)
            axB.plot([lo, hi], [y, y], color=RED, lw=1.8, alpha=0.45, solid_capstyle="butt", zorder=2)
            for xe in (lo, hi):
                axB.plot([xe, xe], [y - 0.07, y + 0.07], color=RED, lw=0.9, alpha=0.6, zorder=2)
            axB.plot([v], [y], ls="none", zorder=4, **mstyle)
            axB.text(hi + 0.42, y, fmt(v), va="center", ha="left", fontsize=FS_VALUE, color=RED,
                     fontweight="bold")
            continue
        axB.plot([0, v], [y, y], color=stem, lw=1.0, ls=ls, solid_capstyle="butt", zorder=2)
        axB.plot([v], [y], ls="none", zorder=3, **mstyle)
        if show:
            axB.text(v + (0.42 if v >= 0 else -0.42), y, fmt(v), va="center",
                     ha="left" if v >= 0 else "right", fontsize=FS_VALUE, color="#4A4A4A")

axB.axvline(0, color="#4A4A4A", lw=0.8, zorder=1)
axB.set_xlim(-7.3, 14.4)
axB.set_ylim(-0.5, n_rows - 0.5)
axB.set_xticks([-5, 0, 5, 10])
axB.set_xticklabels([fmt(t, signed=False, nd=0) for t in [-5, 0, 5, 10]])
axB.set_yticks(range(n_rows))
axB.set_yticklabels(MODELS[::-1], fontsize=FS_LABEL)
axB.tick_params(axis="y", length=0, pad=4)
axB.tick_params(axis="x", length=2.5, width=0.6, color=GREY, labelsize=7.5, pad=2)
axB.grid(axis="x", color="#E4E4E4", lw=0.5)

trans = blended_transform_factory(axB.transData, axB.transAxes)
axB.text(-0.35, -0.155, "\u2190 certificate overstates", transform=trans, ha="right",
         va="top", fontsize=FS_NOTE, color=GREY, style="italic")
axB.text(0.35, -0.155, "certificate understates \u2192", transform=trans, ha="left",
         va="top", fontsize=FS_NOTE, color=GREY, style="italic")

for ax in (axA, axB):
    ax.set_axisbelow(True)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GREY)

# (b) and (c) share a left text edge: where the checkpoint names of (b) start.
fig.canvas.draw()
rc_text_left = min(t.get_window_extent(R).x0 for t in axB.get_yticklabels()) / fig.dpi

# ================================================================================= (c)
axC = axes_in(rc_text_left, 0.0, C_BAR_RIGHT - rc_text_left, C_TITLE_Y - 0.25)
axC.set_xlim(0, 100)
axC.set_ylim(0, C_TITLE_Y - 0.25)       # data y is inches from the bottom of the figure
axC.axis("off")

cums = []
for yb, (name, n, _, _, counts) in zip(C_BAR_Y, POPS):
    lo, cum = 0.0, [0.0]
    for k, (c, col, tcol) in enumerate(zip(counts, CAT_COLORS, CAT_TEXT)):
        share = 100 * c / n
        if share > 0:
            if k == 1 and REF_CONFIRMED:
                conf = 100 * REF_CONFIRMED[name] / n
                axC.add_patch(Rectangle((lo, yb), conf, C_BAR_H, facecolor=ORANGE,
                                        edgecolor="white", lw=0.9, zorder=2))
                axC.add_patch(Rectangle((lo + conf, yb), share - conf, C_BAR_H,
                                        facecolor=ORANGE_LIGHT, edgecolor="white", lw=0.9, zorder=2))
                # print the segment total inside the larger of the two parts, not across the seam
                x_txt, tcol = ((lo + conf / 2, "white") if conf >= share - conf
                               else (lo + conf + (share - conf) / 2, INK))
            else:
                axC.add_patch(Rectangle((lo, yb), share, C_BAR_H, facecolor=col,
                                        edgecolor="white", lw=0.9, zorder=2))
                x_txt = lo + share / 2
            if share >= 4.5:
                axC.text(x_txt, yb + C_BAR_H / 2, f"{share:.1f}%", ha="center", va="center",
                         color=tcol, fontsize=7.2 if share >= 9 else 5.8, zorder=3)
            else:  # only the last segment is this narrow: label it beside the end of the bar
                axC.text(100.8, yb + C_BAR_H / 2, f"{share:.1f}%", ha="left", va="center",
                         color=INK, fontsize=6.4, zorder=3)
        lo += share
        cum.append(lo)
    cums.append(cum)

y_top, y_bot = C_BAR_Y[0], C_BAR_Y[1] + C_BAR_H
for k, (col, alpha) in enumerate(zip(CAT_COLORS, BAND_ALPHA)):   # link each label across bars
    (a0, a1), (b0, b1) = cums[0][k:k + 2], cums[1][k:k + 2]
    axC.add_patch(Polygon([[a0, y_top], [a1, y_top], [b1, y_bot], [b0, y_bot]], closed=True,
                          facecolor=col, alpha=alpha, edgecolor="none", zorder=1))
for t in axC.texts:
    t.set_clip_on(False)


def census_label(y_in, name, n, ncase, nq):
    t = fig.text(rc_text_left / W, y_in / H, name, fontsize=FS_LABEL, color=INK, ha="left",
                 va="baseline")
    fig.text((text_end(t) + 0.08) / W, y_in / H, f"{n:,} answers, {ncase} cases, {nq} questions",
             fontsize=6.8, color=GREY, ha="left", va="baseline")


census_label(C_BAR_Y[0] + C_BAR_H + 0.06, *POPS[0][:4])
census_label(C_BAR_Y[1] - 0.12, *POPS[1][:4])


def swatch_row(y_in, items):
    """A legend row of colour swatches, laid out from the left text edge of (c)."""
    x = rc_text_left
    for label, col in items:
        fig.add_artist(Rectangle((x / W, (y_in - 0.045) / H), 0.09 / W, 0.09 / H,
                                 transform=fig.transFigure, facecolor=col, edgecolor="none"))
        t = fig.text((x + 0.13) / W, y_in / H, label, fontsize=FS_NOTE, color=INK, ha="left",
                     va="center")
        x = text_end(t) + 0.22
    return x


swatch_row(1.25, list(zip(CATS[:3], CAT_COLORS[:3])))
x_note = swatch_row(1.11, list(zip(CATS[3:], CAT_COLORS[3:])))
if REF_CONFIRMED:
    fig.text(x_note / W, 1.11 / H, "solid: question confirmed by blinded experts", fontsize=6.4,
             color=GREY, style="italic", ha="left", va="center")

# ================================================================================= titles, legends
leg_kw = dict(frameon=False, fontsize=FS_NOTE, handlelength=1.0, handletextpad=0.45,
              labelspacing=0.3, borderaxespad=0, borderpad=0)

a_text = panel_title(TAG_LEFT, TOP_TITLE_Y, "(a)", r"Held-out risk at nominal $\alpha = 0.10$")
fig.text(a_text / W, (TOP_TITLE_Y - 0.15) / H, "(%, seed 101)", fontsize=FS_TITLE, ha="left",
         va="baseline")
panel_title(rc_text_left, TOP_TITLE_Y, "(b)",
            r"GAP = risk under the yardstick $-$ reported risk (points)")
panel_title(rc_text_left, C_TITLE_Y, "(c)", "Labels of suite-rejected answers (AI audit)")

hA = [Line2D([], [], ls="none", marker="o", ms=6.0, mfc="white", mec=DARK, mew=1.1),
      Line2D([], [], ls="none", marker="o", ms=5.8, mfc=DARK, mec=DARK),
      Line2D([], [], ls="-", lw=1.3, color=RED, marker="*", ms=9.0, mfc=RED, mec=RED)]
lA = ["reported on its own labels", "suite oracle", "two SQL experts (range)"]
legA = fig.legend(hA, lA, ncol=1, loc="upper left",
                  bbox_to_anchor=(TAG_LEFT / W, (TOP_TITLE_Y - 0.27) / H), **leg_kw)

frac = (rc_text_left - RC_LEFT) / (RC_RIGHT - RC_LEFT)
hB = [Line2D([], [], ls="-", lw=1.3, color=RED, marker="*", ms=8.0, mfc=RED, mec=RED)
      if s[0] == "expert" else Line2D([], [], ls="none", **s[2]) for s in SERIES]
lB = [s[1] for s in SERIES]
order = [0, 2, 1, 3]  # legend fills columns first; this reads row-wise in the row order
legB = axB.legend([hB[j] for j in order], [lB[j] for j in order], ncol=2, columnspacing=1.4,
                  loc="lower left", bbox_to_anchor=(frac, 1.015), **leg_kw)

fig.canvas.draw()
for name, leg in (("(a)", legA), ("(b)", legB)):
    bb = leg.get_window_extent(R)
    print(f"legend {name}: {bb.x0 / fig.dpi:.2f}-{bb.x1 / fig.dpi:.2f} in, "
          f"{bb.y0 / fig.dpi:.2f}-{bb.y1 / fig.dpi:.2f} in high")
print(f"(a) axes top {A_TOP:.2f} in; (c) text edge {rc_text_left:.2f} in")
fig.savefig("figure1_v2.pdf")
fig.savefig("figure1_v2.png", dpi=300)
