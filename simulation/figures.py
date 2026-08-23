"""Figures for *The Baitome*. Each reads the results dict plus the raw
matrices and writes one PNG.

Palette (CVD-checked in a prior validation; line styles and direct labels as
secondary encoding): amber, green, blue, warm gray; red reserved for harm.
"""
from __future__ import annotations

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import registry as R

INK = "#1a1a1a"
GRID = "#d9d9d9"
AMBER = "#b45309"
GREEN = "#15803d"
BLUE = "#2563eb"
GRAY = "#57534e"
RED = "#b3202c"

FAM_COLOR = {"acquisition": BLUE, "conflict": RED, "identity": AMBER,
             "care": GREEN, "retention": GRAY, "extraction": "#7c3aed"}


def _style(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK)
    ax.tick_params(colors=INK, labelsize=8)
    ax.set_axisbelow(True)


def plot_table(res: dict, aux: dict, path: str) -> None:
    B, M = aux["B"], aux["M"]
    names = list(R.COMPOUNDS)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.8, 5.4),
                                   gridspec_kw={"width_ratios": [1, 1.15]})
    im = ax1.imshow(B, aspect="auto", cmap="Greens", vmin=0, vmax=1.0)
    ax1.set_xticks(range(len(R.ACTIONS)))
    ax1.set_xticklabels(R.ACTIONS, fontsize=7.5)
    ax1.set_yticks(range(len(R.ELEMENTS)))
    ax1.set_yticklabels(R.ELEMENTS, fontsize=6.5)
    row = 0
    for fam, els in R.FAMILIES.items():
        ax1.axhline(row - 0.5, color=INK, lw=0.8)
        ax1.annotate(fam, (-0.5, row + len(els) / 2 - 0.5), fontsize=7,
                     color=GRAY, ha="right", va="center", rotation=90,
                     xytext=(-38, 0), textcoords="offset points")
        row += len(els)
    ax1.set_title("the elements: 32 appraisals, 7 families,\n"
                  "action affinities (structural calibration)",
                  fontsize=9.5, color=INK)
    ax1.grid(False)
    # right: the registry incidence
    order = sorted(range(len(names)),
                   key=lambda i: (R.COMPOUND_FAMILIES.index(R.COMPOUNDS[names[i]][0]), names[i]))
    for r_, i in enumerate(order):
        fam = R.COMPOUNDS[names[i]][0]
        for e in R.COMPOUNDS[names[i]][1]:
            ax2.scatter(R.E[e], r_, s=26, c=FAM_COLOR[fam], edgecolors=INK,
                        linewidths=0.3, zorder=3)
    ax2.set_yticks(range(len(names)))
    ax2.set_yticklabels([names[i] for i in order], fontsize=6.3)
    ax2.set_xticks(range(len(R.ELEMENTS)))
    ax2.set_xticklabels(R.ELEMENTS, fontsize=6.0, rotation=90)
    ax2.invert_yaxis()
    ax2.set_title("the compounds: 40 named baits as sparse formulas\n"
                  "(colored by vernacular family)", fontsize=9.5, color=INK)
    ax2.grid(True, color=GRID, lw=0.4, alpha=0.6)
    _style(ax2)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_mendeleev(res: dict, aux: dict, path: str) -> None:
    L, M = aux["L"], aux["M"]
    names = list(R.COMPOUNDS)
    per = res["periodicity"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.4, 4.4),
                                   gridspec_kw={"width_ratios": [1, 1]})
    # left: signatures in 2D (PCA), colored by vernacular family
    Z = (L - L.mean(0)) / (L.std(0) + 1e-9)
    U, S, Vt = np.linalg.svd(Z - Z.mean(0), full_matrices=False)
    P = U[:, :2] * S[:2]
    for i, n in enumerate(names):
        fam = R.COMPOUNDS[n][0]
        ax1.scatter(P[i, 0], P[i, 1], s=42, c=FAM_COLOR[fam],
                    edgecolors=INK, linewidths=0.4, zorder=3)
    rg = names.index("ragebait")
    ax1.annotate("ragebait:\na cluster of one", (P[rg, 0], P[rg, 1]),
                 fontsize=7.5, color=RED, ha="right", xytext=(-8, 10),
                 textcoords="offset points")
    for fam, c in FAM_COLOR.items():
        ax1.scatter([], [], s=32, c=c, edgecolors=INK, linewidths=0.4,
                    label=fam)
    ax1.legend(frameon=False, fontsize=7, loc="lower right", ncol=2)
    ax1.set_xlabel("signature component 1", fontsize=8.5)
    ax1.set_ylabel("signature component 2", fontsize=8.5)
    ax1.set_title(f"behavior redraws the families: cluster purity "
                  f"{per['family_recovery_purity']:.2f}", fontsize=9.5,
                  color=INK)
    ax1.grid(True, color=GRID, lw=0.5, alpha=0.7)
    _style(ax1)
    # right: the empty cells
    realized = np.zeros((len(R.ELEMENTS), len(R.ELEMENTS)))
    for i in range(len(names)):
        f = [R.E[e] for e in R.COMPOUNDS[names[i]][1]]
        for a_ in f:
            for b_ in f:
                if a_ < b_:
                    realized[a_, b_] = 1
    for i in range(len(R.ELEMENTS)):
        for j in range(i + 1, len(R.ELEMENTS)):
            c = BLUE if realized[i, j] else GRID
            s = 12 if realized[i, j] else 4
            ax2.scatter(j, i, s=s, c=c, zorder=3)
    for k, d in enumerate(per["empty_cells_top10"][:5]):
        i, j = sorted(R.E[e] for e in d["pair"])
        ax2.scatter(j, i, s=40, facecolors="none", edgecolors=RED,
                    linewidths=1.2, zorder=4)
    for tag, key in (("VE+ER", ("VE", "ER")), ("MM+TH", ("MM", "TH"))):
        i, j = sorted(R.E[e] for e in key)
        ax2.scatter(j, i, s=40, facecolors="none", edgecolors=AMBER,
                    linewidths=1.2, zorder=4)
    ax2.set_xticks(range(len(R.ELEMENTS)))
    ax2.set_xticklabels(R.ELEMENTS, fontsize=5.6, rotation=90)
    ax2.set_yticks(range(len(R.ELEMENTS)))
    ax2.set_yticklabels(R.ELEMENTS, fontsize=5.6)
    ax2.set_title(f"the empty cells: {per['pairs_realized']} realized pairs, "
                  f"{per['pairs_empty']} unnamed\n(red: top predicted; "
                  f"amber: the seed's two proposals)", fontsize=9.5,
                  color=INK)
    ax2.grid(False)
    _style(ax2)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_ecology(res: dict, aux: dict, path: str) -> None:
    ser = aux["eco_series"]
    eco = res["ecology"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 3.9),
                                   gridspec_kw={"width_ratios": [1.35, 1]})
    t = np.arange(len(ser["engagement"]["conflict"]))
    ax1.plot(t, ser["engagement_feed"]["conflict"], "-", color=RED, lw=1.4,
             label="engagement ranking: conflict share of the feed")
    ax1.plot(t, ser["chronological"]["conflict"], "-", color=GRAY, lw=1.2,
             label="chronological: conflict share")
    nh = eco["no_habituation"]["feed_conflict_share_last100"]
    ax1.axhline(nh, color=RED, lw=1.2, ls="--")
    ax1.annotate("no habituation: the feed locks onto conflict\n"
                 f"at {nh:.2f} and never leaves", (len(t) * 0.99, nh - 0.025),
                 fontsize=7.8, color=RED, ha="right", va="top")
    ax1.set_xlabel("time step", fontsize=9)
    ax1.set_ylabel("conflict-family share", fontsize=9)
    ax1.set_title("habituation is the ecosystem's own damper",
                  fontsize=10, color=INK)
    ax1.legend(frameon=False, fontsize=7.6, loc="lower center")
    ax1.grid(True, color=GRID, lw=0.5, alpha=0.7)
    _style(ax1)
    # right: concentration and churn across arms
    arms = ["engagement", "chronological", "no_habituation"]
    labels = ["engagement\nranking", "chronological", "engagement,\nno habituation"]
    ent = [eco[a]["entropy_mean_last100"] for a in arms]
    sw = [eco[a]["dominance_switches_2nd_half"] for a in arms]
    colors = [RED, GRAY, AMBER]
    ax2.bar(range(3), ent, color=colors, width=0.55)
    for i, (e, s) in enumerate(zip(ent, sw)):
        ax2.annotate(f"entropy {e:.2f}\n{s} switches", (i, e), fontsize=7.8,
                     ha="center", va="bottom", color=INK, xytext=(0, 3),
                     textcoords="offset points")
    ax2.set_xticks(range(3))
    ax2.set_xticklabels(labels, fontsize=8)
    ax2.set_ylabel("production diversity (entropy)", fontsize=9)
    ax2.set_ylim(0, max(ent) * 1.3)
    ax2.set_title("diversity and churn by regime", fontsize=10, color=INK)
    ax2.grid(True, color=GRID, lw=0.5, alpha=0.7)
    _style(ax2)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
