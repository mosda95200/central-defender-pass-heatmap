from __future__ import annotations

import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from mplsoccer import Pitch


def plot_pass_density_heatmap(
    passes: pd.DataFrame,
    player_name: str,
    team_name: str | None = None,
    season_label: str | None = None,
    match_label: str | None = None,
    match_date: str | None = None,
    source: str = "StatsBomb Open Data",
    title: str | None = None,
    bw_adjust: float = 0.65,
    alpha: float = 0.78,
    thresh: float = 0.02,
):
    """
    Plot a pass density heatmap based on pass start locations.

    The pitch lines are kept above the heatmap so the pitch remains visible.
    """

    required_columns = ["x", "y"]

    missing_columns = [
        column for column in required_columns
        if column not in passes.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    plot_data = passes.dropna(subset=["x", "y"]).copy()

    if plot_data.empty:
        raise ValueError("No valid pass coordinates available for plotting.")

    heatmap_cmap = LinearSegmentedColormap.from_list(
        "pass_heatmap",
        [
            (0.00, "#cdeec0"),
            (0.25, "#fff176"),
            (0.50, "#ffca28"),
            (0.75, "#ff9800"),
            (1.00, "#f44336"),
        ],
    )

    pitch_color = "#99DC7F"
    line_color = "white"

    pitch = Pitch(
        pitch_type="statsbomb",
        pitch_color=pitch_color,
        line_color=line_color,
        linewidth=1.5,
        line_zorder=3,
    )

    fig, ax = pitch.draw(figsize=(10, 7.8))
    fig.patch.set_facecolor(pitch_color)
    ax.set_facecolor(pitch_color)

    fig.subplots_adjust(top=0.86, bottom=0.12)

    pitch.kdeplot(
        plot_data["x"],
        plot_data["y"],
        ax=ax,
        fill=True,
        levels=100,
        thresh=thresh,
        alpha=alpha,
        cmap=heatmap_cmap,
        bw_adjust=bw_adjust,
        zorder=1,
    )

    header_title = title or f"{player_name.upper()} — PASSING HEATMAP"

    subtitle_parts = []

    if team_name:
        subtitle_parts.append(team_name)

    if season_label:
        subtitle_parts.append(season_label)

    if match_label:
        subtitle_parts.append(match_label)

    if match_date:
        subtitle_parts.append(str(match_date))

    if source:
        subtitle_parts.append(source)

    header_subtitle = " | ".join(subtitle_parts)

    fig.text(
        0.5,
        0.955,
        header_title,
        ha="center",
        va="center",
        fontsize=18,
        fontweight="bold",
        color="white",
    )

    fig.text(
        0.5,
        0.925,
        header_subtitle,
        ha="center",
        va="center",
        fontsize=9,
        color="white",
    )

    ax.annotate(
        "",
        xy=(0.58, -0.06),
        xytext=(0.42, -0.06),
        xycoords="axes fraction",
        textcoords="axes fraction",
        arrowprops=dict(
            arrowstyle="simple",
            color="white",
            lw=0,
            mutation_scale=25,
        ),
        annotation_clip=False,
    )

    return fig, ax


def plot_pass_map(
    passes: pd.DataFrame,
    player_name: str,
    team_name: str | None = None,
    season_label: str | None = None,
    match_label: str | None = None,
    match_date: str | None = None,
    source: str = "StatsBomb Open Data",
    title: str | None = None,
    show_legend: bool = True,
    arrow_width: float = 1.3,
    arrow_alpha: float = 0.85,
):
    """
    Plot a pass map with arrows.

    Completed passes are shown in green.
    Incomplete passes are shown in red.
    """

    required_columns = ["x", "y", "end_x", "end_y", "is_completed"]

    missing_columns = [
        column for column in required_columns
        if column not in passes.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    plot_data = passes.dropna(
        subset=["x", "y", "end_x", "end_y"]
    ).copy()

    if plot_data.empty:
        raise ValueError("No valid pass coordinates available for plotting.")

    completed = plot_data[
        plot_data["is_completed"]
    ].copy()

    incomplete = plot_data[
        ~plot_data["is_completed"]
    ].copy()

    pitch_color = "#99DC7F"
    line_color = "white"

    pitch = Pitch(
        pitch_type="statsbomb",
        pitch_color=pitch_color,
        line_color=line_color,
        linewidth=1.5,
        line_zorder=4,
    )

    fig, ax = pitch.draw(figsize=(10, 8.4))
    fig.patch.set_facecolor(pitch_color)
    ax.set_facecolor(pitch_color)

    fig.subplots_adjust(top=0.42, bottom=0.24)

    if len(completed) > 0:
        pitch.arrows(
            completed["x"],
            completed["y"],
            completed["end_x"],
            completed["end_y"],
            ax=ax,
            color="#00a86b",
            width=arrow_width,
            headwidth=4,
            headlength=4,
            alpha=arrow_alpha,
            zorder=2,
            label="Completed passes",
        )

    if len(incomplete) > 0:
        pitch.arrows(
            incomplete["x"],
            incomplete["y"],
            incomplete["end_x"],
            incomplete["end_y"],
            ax=ax,
            color="#e74c3c",
            width=arrow_width,
            headwidth=4,
            headlength=4,
            alpha=arrow_alpha,
            zorder=2,
            label="Incomplete passes",
        )

    header_title = title or f"{player_name.upper()} — PASS MAP"

    subtitle_parts = []

    if team_name:
        subtitle_parts.append(team_name)

    if season_label:
        subtitle_parts.append(season_label)

    if match_label:
        subtitle_parts.append(match_label)

    if match_date:
        subtitle_parts.append(str(match_date))

    if source:
        subtitle_parts.append(source)

    header_subtitle = " | ".join(subtitle_parts)

    fig.text(
        0.5,
        0.955,
        header_title,
        ha="center",
        va="center",
        fontsize=18,
        fontweight="bold",
        color="white",
    )

    fig.text(
        0.5,
        0.925,
        header_subtitle,
        ha="center",
        va="center",
        fontsize=9,
        color="white",
    )

    ax.annotate(
        "",
        xy=(0.58, -0.00),
        xytext=(0.42, -0.00),
        xycoords="axes fraction",
        textcoords="axes fraction",
        arrowprops=dict(
            arrowstyle="simple",
            color="white",
            lw=0,
            mutation_scale=25,
        ),
        annotation_clip=False,
    )

    if show_legend:
        ax.legend(
            loc="upper center",
            bbox_to_anchor=(0.5, -0.03),
            ncol=2,
            frameon=False,
            fontsize=10,
            handlelength=1.8,
            handletextpad=0.6,
            columnspacing=1.8,
        )

    return fig, ax