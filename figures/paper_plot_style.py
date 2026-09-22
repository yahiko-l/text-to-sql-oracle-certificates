"""Shared matplotlib style for every paper figure.

Palette: the validated reference categorical palette (light surface), checked with
the dataviz validator on a white surface. Four checkpoints are never placed as four
adjacent colours on an all-pairs form; they are facets. Within a panel at most five
adjacent series are used, always with a legend and selective direct labels.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

FONT_SIZE = 9
DPI = 300
FORMAT = "pdf"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(ROOT, "figures")

TEXT_WIDTH_IN = 6.5   # arxiv.sty text width
HALF_WIDTH_IN = 3.15

matplotlib.rcParams.update({
    "font.size": FONT_SIZE,
    "font.family": "serif",
    "font.serif": ["Liberation Serif", "Nimbus Roman", "Times New Roman", "Times", "STIXGeneral", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "axes.labelsize": FONT_SIZE,
    "axes.titlesize": FONT_SIZE,
    "xtick.labelsize": FONT_SIZE - 1,
    "ytick.labelsize": FONT_SIZE - 1,
    "legend.fontsize": FONT_SIZE - 1,
    "legend.frameon": False,
    "figure.dpi": DPI,
    "savefig.dpi": DPI,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
    "axes.grid": False,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#c3c2b7",
    "axes.linewidth": 0.6,
    "xtick.color": "#52514e",
    "ytick.color": "#52514e",
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.major.size": 2.5,
    "ytick.major.size": 2.5,
    "axes.labelcolor": "#0b0b0b",
    "text.color": "#0b0b0b",
    "lines.linewidth": 1.4,
    "lines.markersize": 4.5,
    "patch.linewidth": 0,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

# Categorical slots, fixed order (validated adjacent on white; first three validated all-pairs).
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = SERIES
# Sequential blue ramp (steps 100 to 700).
SEQ_BLUE = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5",
            "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
ORDINAL_BLUE3 = ["#86b6ef", "#2a78d6", "#104281"]   # steps 250, 450, 650
NEUTRAL_MID = "#f0efec"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
GRAY_DARK = "#6f6e69"
GRAY_LIGHT = "#b9b8b1"
SURFACE = "#ffffff"

CHECKPOINTS = ["kwai-autosql-32b", "kwai-autosql-14b", "omnisql-32b", "xiyansql-32b"]
CHECKPOINT_LABEL = {
    "kwai-autosql-32b": "Kwai-32B",
    "kwai-autosql-14b": "Kwai-14B",
    "omnisql-32b": "Omni-32B",
    "xiyansql-32b": "XiYan-32B",
}
CHECKPOINT_SHORT = {
    "kwai-autosql-32b": "Kwai-32B",
    "kwai-autosql-14b": "Kwai-14B",
    "omnisql-32b": "Omni-32B",
    "xiyansql-32b": "XiYan-32B",
}
SCORES = ["top_class_mass", "discrete_semantic_entropy", "lin_deg", "lin_numsets",
          "mean_seq_logprob", "max_seq_logprob"]
SCORE_LABEL = {
    "top_class_mass": "top-class mass",
    "discrete_semantic_entropy": "discrete semantic entropy",
    "lin_deg": "degree measure",
    "lin_numsets": "set count",
    "mean_seq_logprob": "mean seq. log-prob",
    "max_seq_logprob": "max seq. log-prob",
}
LABELS5 = ["semantic_error", "gold_defect", "underspecified", "instance_defect", "comparator_artifact"]
LABEL_TEXT = {
    "semantic_error": "semantic error",
    "gold_defect": "suspected reference defect",
    "underspecified": "underspecified question",
    "instance_defect": "synthetic-instance defect",
    "comparator_artifact": "comparator artefact",
}


def load(rel_path):
    with open(os.path.join(ROOT, rel_path)) as f:
        return json.load(f)


def style_axes(ax, ygrid=True):
    ax.spines["left"].set_color(BASELINE)
    ax.spines["bottom"].set_color(BASELINE)
    if ygrid:
        ax.yaxis.grid(True, color=GRID, linewidth=0.5, linestyle="-")
        ax.set_axisbelow(True)
    ax.tick_params(length=2.5, width=0.6, colors=INK2)


def save_fig(fig, name, fmt=FORMAT):
    os.makedirs(FIG_DIR, exist_ok=True)
    path = os.path.join(FIG_DIR, f"{name}.{fmt}")
    fig.savefig(path)
    print(f"Saved: figures/{name}.{fmt}")
    return path
