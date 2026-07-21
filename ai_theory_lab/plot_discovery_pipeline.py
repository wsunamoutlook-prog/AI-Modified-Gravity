#!/usr/bin/env python3
"""Draw the publication flowchart for the autonomous discovery pipeline."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIRS = [
    ROOT / "paper_figures",
    ROOT / "overleaf_cmp1500_agent_results_v1" / "figures",
]


COLORS = {
    "ink": "#172434",
    "muted": "#647484",
    "line": "#C8D1D8",
    "agent": "#246D9B",
    "agent_dark": "#174E75",
    "agent_mid": "#75B4D8",
    "agent_soft": "#E9F4FB",
    "physics": "#2D8068",
    "physics_mid": "#68AA95",
    "physics_soft": "#EAF5F1",
    "score": "#C67C12",
    "score_mid": "#E5B252",
    "score_soft": "#FFF2D7",
    "white": "#FFFFFF",
}


def arrow(
    ax,
    start,
    end,
    *,
    color,
    linewidth=1.8,
    rad=0.0,
    mutation_scale=15,
    zorder=3,
):
    patch = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=mutation_scale,
        linewidth=linewidth,
        color=color,
        connectionstyle=f"arc3,rad={rad}",
        shrinkA=2,
        shrinkB=2,
        zorder=zorder,
    )
    ax.add_patch(patch)
    return patch


def layer_heading(ax, y, title, color):
    ax.text(
        0.055,
        y,
        title,
        ha="left",
        va="center",
        fontsize=11.6,
        color=color,
        weight="bold",
    )
    ax.plot([0.055, 0.945], [y - 0.035, y - 0.035], color=COLORS["line"], linewidth=0.9)
    ax.plot(
        [0.055, 0.185],
        [y - 0.035, y - 0.035],
        color=color,
        linewidth=3.0,
        solid_capstyle="round",
    )


def draw_document(ax, x, y, width, height):
    """Folded document containing the proposed covariant Lagrangian."""
    fold = 0.035
    shadow = [(x + 0.008, y - 0.012), (x + width + 0.008, y - 0.012)]
    ax.plot(
        [p[0] for p in shadow],
        [p[1] for p in shadow],
        color=COLORS["agent_soft"],
        linewidth=8.0,
        solid_capstyle="round",
        zorder=1,
    )
    vertices = [
        (x, y),
        (x + width, y),
        (x + width, y + height - fold),
        (x + width - fold, y + height),
        (x, y + height),
    ]
    ax.add_patch(
        Polygon(
            vertices,
            closed=True,
            facecolor=COLORS["agent_soft"],
            edgecolor=COLORS["agent"],
            linewidth=1.7,
            joinstyle="round",
            zorder=3,
        )
    )
    ax.plot(
        [x + width - fold, x + width - fold, x + width],
        [y + height, y + height - fold, y + height - fold],
        color=COLORS["agent"],
        linewidth=1.25,
        zorder=4,
    )
    ax.text(
        x + width / 2 - 0.004,
        y + height * 0.67,
        "Candidate theory",
        ha="center",
        va="center",
        fontsize=10.5,
        color=COLORS["ink"],
        weight="bold",
        zorder=5,
    )
    ax.text(
        x + width / 2 - 0.004,
        y + height * 0.37,
        r"$\mathcal{L}=\sqrt{-g}\sum_I c_I\mathcal{O}_I$",
        ha="center",
        va="center",
        fontsize=12.0,
        color=COLORS["agent_dark"],
        zorder=5,
    )


def draw_memory(ax, x, y, width, height):
    """Layered current-run memory with compact scientific state."""
    for offset, alpha in ((0.022, 0.45), (0.011, 0.72), (0.0, 1.0)):
        ax.add_patch(
            FancyBboxPatch(
                (x + offset, y + offset),
                width,
                height,
                boxstyle="round,pad=0.008,rounding_size=0.018",
                linewidth=1.35,
                edgecolor=COLORS["agent"],
                facecolor=COLORS["agent_soft"],
                alpha=alpha,
                zorder=2 + int((0.022 - offset) * 100),
            )
        )
    ax.text(
        x + width / 2,
        y + height * 0.65,
        "Current-run memory",
        ha="center",
        va="center",
        fontsize=10.4,
        color=COLORS["ink"],
        weight="bold",
        zorder=7,
    )
    ax.text(
        x + width / 2,
        y + height * 0.33,
        r"$\{\mathcal{L},\vartheta,\chi^2,\mathrm{status}\}$",
        ha="center",
        va="center",
        fontsize=10.8,
        color=COLORS["agent_dark"],
        zorder=7,
    )


def draw_langgraph(ax, center, width, height):
    """Hexagonal LangGraph orchestration hub."""
    x, y = center
    dx = width / 2
    dy = height / 2
    cut = width * 0.16
    vertices = [
        (x - dx + cut, y - dy),
        (x + dx - cut, y - dy),
        (x + dx, y),
        (x + dx - cut, y + dy),
        (x - dx + cut, y + dy),
        (x - dx, y),
    ]
    halo = [(px + (px - x) * 0.08, py + (py - y) * 0.12) for px, py in vertices]
    ax.add_patch(
        Polygon(halo, closed=True, facecolor=COLORS["agent_soft"], edgecolor="none", zorder=1)
    )
    ax.add_patch(
        Polygon(
            vertices,
            closed=True,
            facecolor=COLORS["agent_dark"],
            edgecolor=COLORS["agent_dark"],
            linewidth=1.2,
            joinstyle="round",
            zorder=3,
        )
    )

    graph_points = [(x - 0.035, y + 0.035), (x + 0.035, y + 0.035), (x, y - 0.004)]
    for a, b in ((0, 1), (1, 2), (2, 0)):
        ax.plot(
            [graph_points[a][0], graph_points[b][0]],
            [graph_points[a][1], graph_points[b][1]],
            color=COLORS["agent_mid"],
            linewidth=1.35,
            zorder=4,
        )
    for px, py in graph_points:
        ax.add_patch(
            Ellipse(
                (px, py),
                0.012,
                0.020,
                facecolor=COLORS["white"],
                edgecolor="none",
                zorder=5,
            )
        )
    ax.text(
        x,
        y - 0.047,
        "LangGraph",
        ha="center",
        va="center",
        fontsize=11.2,
        weight="bold",
        color=COLORS["white"],
        zorder=5,
    )
    ax.text(
        x,
        y - 0.078,
        r"propose  $\rightarrow$  validate  $\rightarrow$  learn",
        ha="center",
        va="center",
        fontsize=8.5,
        color="#D8ECF7",
        zorder=5,
    )


def draw_grammar(ax, center):
    x, y = center
    width, height = 0.195, 0.235
    dx, dy = width / 2, height / 2
    cut = 0.025
    vertices = [
        (x - dx + cut, y - dy),
        (x + dx - cut, y - dy),
        (x + dx, y),
        (x + dx - cut, y + dy),
        (x - dx + cut, y + dy),
        (x - dx, y),
    ]
    ax.add_patch(
        Polygon(
            vertices,
            closed=True,
            facecolor=COLORS["physics_soft"],
            edgecolor=COLORS["physics"],
            linewidth=1.8,
            joinstyle="round",
            zorder=4,
        )
    )
    ax.text(
        x,
        y + 0.058,
        "Grammar Masker",
        ha="center",
        va="center",
        fontsize=10.5,
        weight="bold",
        zorder=6,
    )
    ax.text(
        x,
        y + 0.005,
        "curvature invariants",
        ha="center",
        va="center",
        fontsize=9.2,
        color=COLORS["muted"],
        zorder=6,
    )
    ax.text(
        x,
        y - 0.055,
        r"$\mathcal{O}_I\!:\ R,\ R^2,\ R_{\mu\nu}R^{\mu\nu},\ldots$",
        ha="center",
        va="center",
        fontsize=10.0,
        color=COLORS["physics"],
        zorder=6,
    )


def draw_ghost_filter(ax, center):
    """Shield-shaped EOM and ghost-cancellation stage."""
    x, y = center
    width, height = 0.20, 0.25
    dx, dy = width / 2, height / 2
    vertices = [
        (x - dx, y + dy),
        (x + dx, y + dy),
        (x + dx * 0.90, y - dy * 0.28),
        (x, y - dy),
        (x - dx * 0.90, y - dy * 0.28),
    ]
    ax.add_patch(
        Polygon(
            vertices,
            closed=True,
            facecolor="#F2F8F5",
            edgecolor=COLORS["physics"],
            linewidth=1.8,
            joinstyle="round",
            zorder=4,
        )
    )
    ax.text(
        x,
        y + 0.065,
        "EOM + ghost cancellation",
        ha="center",
        va="center",
        fontsize=10.0,
        weight="bold",
        zorder=6,
    )
    ax.text(
        x,
        y + 0.014,
        r"$E_A=\delta S/\delta y_A$",
        ha="center",
        va="center",
        fontsize=10.7,
        color=COLORS["physics"],
        zorder=6,
    )
    ax.text(
        x,
        y - 0.047,
        r"$\mathrm{Coeff}[E_A,y_B^{(r)}]=0,\ r\geq3$",
        ha="center",
        va="center",
        fontsize=9.2,
        color=COLORS["physics"],
        zorder=6,
    )


def draw_builder_solver(ax, center):
    x, y = center
    width, height = 0.19, 0.205
    ax.add_patch(
        FancyBboxPatch(
            (x - width / 2, y - height / 2),
            width,
            height,
            boxstyle="round,pad=0.012,rounding_size=0.052",
            facecolor=COLORS["physics_soft"],
            edgecolor=COLORS["physics"],
            linewidth=1.8,
            zorder=4,
        )
    )
    ax.add_patch(
        Ellipse(
            (x - width / 2 + 0.016, y),
            0.018,
            height * 0.70,
            facecolor=COLORS["white"],
            edgecolor=COLORS["physics_mid"],
            linewidth=1.0,
            zorder=5,
        )
    )
    ax.text(
        x + 0.007,
        y + 0.050,
        "Builder + Solver",
        ha="center",
        va="center",
        fontsize=10.6,
        weight="bold",
        zorder=6,
    )
    ax.text(
        x + 0.007,
        y - 0.006,
        r"$\mathcal{L}_{\rm GF}\ \longrightarrow\ H(z;\vartheta)$",
        ha="center",
        va="center",
        fontsize=10.7,
        color=COLORS["physics"],
        zorder=6,
    )
    ax.text(
        x + 0.007,
        y - 0.057,
        "numerical parameter scan",
        ha="center",
        va="center",
        fontsize=9.0,
        color=COLORS["muted"],
        zorder=6,
    )


def draw_data_score(ax, center):
    x, y = center
    ax.add_patch(
        Ellipse(
            (x, y),
            0.19,
            0.235,
            facecolor=COLORS["score_soft"],
            edgecolor=COLORS["score"],
            linewidth=2.0,
            zorder=4,
        )
    )
    ax.add_patch(
        Ellipse(
            (x, y),
            0.165,
            0.198,
            facecolor=COLORS["white"],
            edgecolor=COLORS["score_mid"],
            linewidth=1.0,
            zorder=5,
        )
    )
    ax.text(x, y + 0.063, "DES-SN + DESI DR2 BAO", ha="center", va="center", fontsize=9.7, weight="bold", zorder=6)
    ax.text(
        x,
        y + 0.002,
        r"$\chi^2_{\rm tot}$",
        ha="center",
        va="center",
        fontsize=15.0,
        color=COLORS["score"],
        weight="bold",
        zorder=6,
    )
    ax.text(
        x,
        y - 0.057,
        r"$=\chi^2_{\rm SN}+\chi^2_{\rm BAO}$",
        ha="center",
        va="center",
        fontsize=9.8,
        color=COLORS["score"],
        zorder=6,
    )


def draw_flowchart(output_dirs=OUTPUT_DIRS):
    plt.rcParams.update(
        {
            "font.family": "STIXGeneral",
            "mathtext.fontset": "stix",
            "font.size": 10,
            "axes.unicode_minus": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )

    fig, ax = plt.subplots(figsize=(15.6, 6.25))
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    layer_heading(ax, 0.945, "LANGGRAPH AGENT", COLORS["agent"])
    layer_heading(ax, 0.505, "DETERMINISTIC PHYSICS PIPELINE", COLORS["physics"])

    draw_document(ax, 0.075, 0.655, 0.21, 0.19)
    draw_langgraph(ax, (0.515, 0.748), 0.25, 0.20)
    draw_memory(ax, 0.755, 0.67, 0.175, 0.155)

    arrow(ax, (0.745, 0.748), (0.645, 0.748), color=COLORS["agent"], linewidth=2.0)
    arrow(ax, (0.385, 0.748), (0.295, 0.748), color=COLORS["agent"], linewidth=2.0)

    grammar_center = (0.145, 0.26)
    ghost_center = (0.385, 0.26)
    builder_center = (0.625, 0.26)
    data_center = (0.86, 0.26)

    # A subtle backbone unifies the deterministic stages without turning them
    # into identical process boxes.
    ax.plot(
        [0.105, 0.90],
        [0.26, 0.26],
        color=COLORS["physics_soft"],
        linewidth=10.0,
        solid_capstyle="round",
        zorder=1,
    )
    draw_grammar(ax, grammar_center)
    draw_ghost_filter(ax, ghost_center)
    draw_builder_solver(ax, builder_center)
    draw_data_score(ax, data_center)

    for start_x, end_x in ((0.245, 0.282), (0.485, 0.523), (0.72, 0.755)):
        arrow(
            ax,
            (start_x, 0.26),
            (end_x, 0.26),
            color=COLORS["physics_mid"],
            linewidth=2.1,
            mutation_scale=15,
            zorder=6,
        )

    arrow(
        ax,
        (0.18, 0.645),
        (0.15, 0.39),
        color=COLORS["agent"],
        linewidth=2.0,
        rad=0.08,
        zorder=2,
    )
    arrow(
        ax,
        (0.90, 0.37),
        (0.855, 0.66),
        color=COLORS["agent"],
        linewidth=2.0,
        rad=-0.13,
        zorder=2,
    )
    ax.text(
        0.84,
        0.545,
        "validation feedback",
        ha="center",
        va="bottom",
        fontsize=8.8,
        color=COLORS["agent"],
        zorder=7,
    )

    fig.subplots_adjust(left=0.012, right=0.992, top=0.99, bottom=0.02)

    for directory in output_dirs:
        directory.mkdir(parents=True, exist_ok=True)
        base = directory / "autonomous_discovery_pipeline"
        fig.savefig(base.with_suffix(".pdf"), bbox_inches="tight", facecolor="white")
        fig.savefig(base.with_suffix(".svg"), bbox_inches="tight", facecolor="white")
        fig.savefig(base.with_suffix(".png"), dpi=300, bbox_inches="tight", facecolor="white")

    plt.close(fig)


if __name__ == "__main__":
    draw_flowchart()
