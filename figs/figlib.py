"""Small drawing helpers for the report's architecture diagrams (matplotlib, 600 DPI)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Polygon

from matplotlib import font_manager

# Use the first available font with Arial metrics (Arial on Windows, Liberation Sans on Linux)
_AVAILABLE = {f.name for f in font_manager.fontManager.ttflist}
FONT = next((f for f in ["Arial", "Liberation Sans", "Helvetica", "DejaVu Sans"] if f in _AVAILABLE), "DejaVu Sans")

plt.rcParams.update({
    "font.family": FONT, "font.size": 6.5, "axes.titlesize": 7.5,
    "axes.labelsize": 7, "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
    "legend.fontsize": 6.2, "axes.linewidth": 0.6, "lines.linewidth": 1.1,
    "savefig.dpi": 600, "figure.dpi": 150,
})

OUT = os.environ.get("FIG_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "diagrams"))
os.makedirs(OUT, exist_ok=True)

NAVY, BLUE, TEAL, ORANGE, AMBER = "#1F3B73", "#00629B", "#2A9D8F", "#D1603D", "#E9A23B"
GREEN, PURPLE, RED, GRAY, DARK = "#3A7D44", "#6A4C93", "#B23A48", "#6C757D", "#222222"
L = {  # light fills
    NAVY: "#DDE4F2", BLUE: "#D6EAF5", TEAL: "#D8F0EC", ORANGE: "#F8E0D7", AMBER: "#FBEFD5",
    GREEN: "#DCEFDF", PURPLE: "#E6DFF0", RED: "#F3DADF", GRAY: "#ECEDEF",
}
W = 3.45  # IEEE single-column width (in)


def canvas(h, w=W):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100); ax.set_ylim(0, 100 * h / w); ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text="", c=BLUE, fill=None, fs=6.2, bold=False, tc=DARK, r=1.2,
        lw=0.7, ls="-", ha="center", va="center", solid=False, z=2):
    fc = c if solid else (fill or L.get(c, "#FFFFFF"))
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       fc=fc, ec=c, lw=lw, ls=ls, zorder=z)
    ax.add_patch(p)
    if text:
        tx = x + w / 2 if ha == "center" else x + 1.2
        ty = y + h / 2 if va == "center" else y + h - 1.2
        ax.text(tx, ty, text, ha=ha, va=va, fontsize=fs, color="white" if solid else tc,
                fontweight="bold" if bold else "normal", zorder=z + 1, linespacing=1.15)
    return (x, y, w, h)


def arrow(ax, p1, p2, c=DARK, lw=0.8, style="-|>", ls="-", rad=0.0, text=None, fs=5.6,
          toff=(0, 1.2), ms=6, z=1):
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=ms, color=c, lw=lw, ls=ls,
                        connectionstyle=f"arc3,rad={rad}", zorder=z, shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    if text:
        ax.text((p1[0] + p2[0]) / 2 + toff[0], (p1[1] + p2[1]) / 2 + toff[1], text,
                ha="center", va="bottom", fontsize=fs, color=c, zorder=5,
                bbox=dict(fc="white", ec="none", pad=0.3, alpha=0.85))


def label(ax, x, y, text, fs=6.2, c=DARK, bold=False, ha="center", va="center", it=False, rot=0):
    ax.text(x, y, text, fontsize=fs, color=c, ha=ha, va=va, rotation=rot,
            fontweight="bold" if bold else "normal", fontstyle="italic" if it else "normal",
            zorder=6, linespacing=1.15)


def band(ax, y, h, title, c, x=1, w=98, fs=6.4):
    box(ax, x, y, w, h, c=c, r=1.5, lw=0.6)
    box(ax, x, y, 13, h, title, c=c, solid=True, fs=fs - 0.4, bold=True, r=1.5)


def circle(ax, x, y, r, text="", c=BLUE, fs=6, solid=False):
    ax.add_patch(Circle((x, y), r, fc=c if solid else L.get(c, "#fff"), ec=c, lw=0.7, zorder=2))
    if text:
        label(ax, x, y, text, fs=fs, c="white" if solid else DARK)


def save(fig, num, name):
    fn = os.path.join(OUT, f"Fig {num:02d} {name}.png")
    fig.savefig(fn, dpi=600, facecolor="white")
    plt.close(fig)
    return fn