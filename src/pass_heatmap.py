"""
Utilities for building pass heatmaps from StatsBomb event data.

This module contains reusable functions used in the notebook and future scripts.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
from statsbombpy import sb


def load_competitions() -> pd.DataFrame:
    """
    Load available StatsBomb Open Data competitions.

    Returns
    -------
    pd.DataFrame
        DataFrame containing available competitions and seasons.
    """
    return sb.competitions()


def load_matches(competition_id: int, season_id: int) -> pd.DataFrame:
    """
    Load matches for a given competition and season.

    Parameters
    ----------
    competition_id : int
        StatsBomb competition ID.
    season_id : int
        StatsBomb season ID.

    Returns
    -------
    pd.DataFrame
        DataFrame containing matches.
    """
    return sb.matches(
        competition_id=competition_id,
        season_id=season_id
    )


def load_events(match_id: int) -> pd.DataFrame:
    """
    Load event data for a given match.

    Parameters
    ----------
    match_id : int
        StatsBomb match ID.

    Returns
    -------
    pd.DataFrame
        DataFrame containing all match events.
    """
    return sb.events(match_id=match_id)


def filter_passes(events: pd.DataFrame) -> pd.DataFrame:
    """
    Filter event data to keep only pass events.

    Parameters
    ----------
    events : pd.DataFrame
        StatsBomb events DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame containing only pass events.
    """
    if "type" not in events.columns:
        raise ValueError("Column 'type' is missing from events DataFrame.")

    return events[events["type"] == "Pass"].copy()


def filter_player_passes(
    passes: pd.DataFrame,
    player_name: str
) -> pd.DataFrame:
    """
    Filter passes for a specific player.

    Parameters
    ----------
    passes : pd.DataFrame
        Pass events DataFrame.
    player_name : str
        Player name to filter.

    Returns
    -------
    pd.DataFrame
        DataFrame containing passes from the selected player.
    """
    if "player" not in passes.columns:
        raise ValueError("Column 'player' is missing from passes DataFrame.")

    return passes[passes["player"] == player_name].copy()


def extract_coordinate(
    value: object,
    index: int
) -> float:
    """
    Extract a coordinate from a StatsBomb location list.

    Parameters
    ----------
    value : object
        Location value, usually a list like [x, y].
    index : int
        Coordinate index to extract.

    Returns
    -------
    float
        Extracted coordinate or NaN.
    """
    if isinstance(value, list) and len(value) > index:
        return value[index]

    return np.nan


def prepare_pass_coordinates(passes: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare pass start and end coordinates.

    Parameters
    ----------
    passes : pd.DataFrame
        Pass events DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with x, y, end_x, end_y and is_completed columns.
    """
    required_columns = ["location", "pass_end_location", "pass_outcome"]

    missing_columns = [
        column for column in required_columns
        if column not in passes.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    passes = passes.copy()

    passes["x"] = passes["location"].apply(
        lambda value: extract_coordinate(value, 0)
    )
    passes["y"] = passes["location"].apply(
        lambda value: extract_coordinate(value, 1)
    )

    passes["end_x"] = passes["pass_end_location"].apply(
        lambda value: extract_coordinate(value, 0)
    )
    passes["end_y"] = passes["pass_end_location"].apply(
        lambda value: extract_coordinate(value, 1)
    )

    passes["is_completed"] = passes["pass_outcome"].isna()

    return passes


def add_pass_features(passes: pd.DataFrame) -> pd.DataFrame:
    """
    Add useful pass features for analysis.

    Features added:
    - is_forward_pass
    - is_long_pass
    - x_progression
    - y_progression

    Parameters
    ----------
    passes : pd.DataFrame
        Prepared passes DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with additional pass features.
    """
    required_columns = ["x", "y", "end_x", "end_y"]

    missing_columns = [
        column for column in required_columns
        if column not in passes.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    passes = passes.copy()

    passes["x_progression"] = passes["end_x"] - passes["x"]
    passes["y_progression"] = passes["end_y"] - passes["y"]
    passes["is_forward_pass"] = passes["x_progression"] > 0

    if "pass_length" in passes.columns:
        passes["is_long_pass"] = passes["pass_length"] >= 30
    else:
        passes["pass_length"] = np.sqrt(
            passes["x_progression"] ** 2 + passes["y_progression"] ** 2
        )
        passes["is_long_pass"] = passes["pass_length"] >= 30

    return passes


def calculate_pass_metrics(passes: pd.DataFrame) -> dict:
    """
    Calculate basic pass metrics.

    Parameters
    ----------
    passes : pd.DataFrame
        Prepared passes DataFrame.

    Returns
    -------
    dict
        Dictionary containing pass metrics.
    """
    if len(passes) == 0:
        return {
            "total_passes": 0,
            "completed_passes": 0,
            "completion_rate": 0,
            "forward_passes": 0,
            "forward_pass_share": 0,
            "long_passes": 0,
            "long_pass_share": 0,
            "average_pass_length": 0,
        }

    passes = add_pass_features(passes)

    total_passes = len(passes)
    completed_passes = int(passes["is_completed"].sum())
    completion_rate = completed_passes / total_passes

    forward_passes = int(passes["is_forward_pass"].sum())
    forward_pass_share = forward_passes / total_passes

    long_passes = int(passes["is_long_pass"].sum())
    long_pass_share = long_passes / total_passes

    average_pass_length = float(passes["pass_length"].mean())

    return {
        "total_passes": total_passes,
        "completed_passes": completed_passes,
        "completion_rate": completion_rate,
        "forward_passes": forward_passes,
        "forward_pass_share": forward_pass_share,
        "long_passes": long_passes,
        "long_pass_share": long_pass_share,
        "average_pass_length": average_pass_length,
    }


def create_metrics_summary(
    metrics: dict,
    player_name: str,
    team_name: str,
    match_label: str,
    match_date: str
) -> pd.DataFrame:
    """
    Create a readable metrics summary table.

    Parameters
    ----------
    metrics : dict
        Pass metrics dictionary.
    player_name : str
        Selected player name.
    team_name : str
        Selected team name.
    match_label : str
        Match label.
    match_date : str
        Match date.

    Returns
    -------
    pd.DataFrame
        Metrics summary table.
    """
    return pd.DataFrame(
        {
            "metric": [
                "Player",
                "Team",
                "Match",
                "Match date",
                "Total passes",
                "Completed passes",
                "Completion rate",
                "Forward passes",
                "Forward pass share",
                "Long passes",
                "Long pass share",
                "Average pass length",
            ],
            "value": [
                player_name,
                team_name,
                match_label,
                match_date,
                metrics["total_passes"],
                metrics["completed_passes"],
                f"{metrics['completion_rate']:.1%}",
                metrics["forward_passes"],
                f"{metrics['forward_pass_share']:.1%}",
                metrics["long_passes"],
                f"{metrics['long_pass_share']:.1%}",
                round(metrics["average_pass_length"], 1),
            ],
        }
    )


def plot_pass_heatmap(
    passes: pd.DataFrame,
    player_name: str,
    match_label: Optional[str] = None,
    match_date: Optional[str] = None,
    source: str = "StatsBomb Open Data",
    title: Optional[str] = None,
):
    """
    Plot a pass heatmap using pass start locations.

    Parameters
    ----------
    passes : pd.DataFrame
        Prepared passes DataFrame with x and y columns.
    player_name : str
        Selected player name.
    match_label : str, optional
        Match label to display in subtitle.
    match_date : str, optional
        Match date to display in subtitle.
    source : str
        Data source name.
    title : str, optional
        Custom chart title.

    Returns
    -------
    tuple
        Matplotlib figure and axis.
    """
    required_columns = ["x", "y"]

    missing_columns = [
        column for column in required_columns
        if column not in passes.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    plot_data = passes.dropna(subset=["x", "y"]).copy()

    pitch = Pitch(
        pitch_type="statsbomb",
        pitch_color="white",
        line_color="black"
    )

    fig, ax = pitch.draw(figsize=(12, 8))

    pitch.kdeplot(
        plot_data["x"],
        plot_data["y"],
        ax=ax,
        fill=True,
        levels=100,
        thresh=0.05,
        alpha=0.65
    )

    chart_title = title or f"Pass Heatmap — {player_name}"

    ax.set_title(
        chart_title,
        fontsize=18,
        pad=20
    )

    subtitle_parts = []

    if match_label:
        subtitle_parts.append(match_label)

    if match_date:
        subtitle_parts.append(str(match_date))

    if source:
        subtitle_parts.append(source)

    if subtitle_parts:
        fig.text(
            0.5,
            0.92,
            " | ".join(subtitle_parts),
            ha="center",
            fontsize=11
        )

    fig.text(
        0.5,
        0.08,
        "Heatmap based on pass start locations",
        ha="center",
        fontsize=10
    )

    return fig, ax


def save_figure(
    fig,
    output_path: str | Path,
    dpi: int = 300
) -> None:
    """
    Save a Matplotlib figure.

    Parameters
    ----------
    fig
        Matplotlib figure.
    output_path : str | Path
        Output file path.
    dpi : int
        Export resolution.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig.savefig(
        output_path,
        dpi=dpi,
        bbox_inches="tight"
    )


def build_player_pass_dataset(
    match_id: int,
    player_name: str
) -> pd.DataFrame:
    """
    Build a clean pass dataset for one player and one match.

    Parameters
    ----------
    match_id : int
        StatsBomb match ID.
    player_name : str
        Selected player name.

    Returns
    -------
    pd.DataFrame
        Prepared player pass dataset.
    """
    events = load_events(match_id)
    passes = filter_passes(events)
    player_passes = filter_player_passes(passes, player_name)
    player_passes = prepare_pass_coordinates(player_passes)
    player_passes = add_pass_features(player_passes)

    return player_passes

def plot_pass_map(
    passes: pd.DataFrame,
    player_name: str,
    team_name: Optional[str] = None,
    match_label: Optional[str] = None,
    match_date: Optional[str] = None,
    source: str = "StatsBomb Open Data",
    title: Optional[str] = None,
):
    """
    Plot a pass map with successful passes in green
    and unsuccessful passes in red.

    Parameters
    ----------
    passes : pd.DataFrame
        Prepared passes DataFrame with x, y, end_x, end_y and is_completed.
    player_name : str
        Selected player name.
    team_name : str, optional
        Team name for subtitle.
    match_label : str, optional
        Match label.
    match_date : str, optional
        Match date.
    source : str
        Data source.
    title : str, optional
        Custom title.

    Returns
    -------
    tuple
        Matplotlib figure and axis.
    """
    required_columns = ["x", "y", "end_x", "end_y", "is_completed"]

    missing_columns = [
        column for column in required_columns
        if column not in passes.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    plot_data = passes.dropna(subset=["x", "y", "end_x", "end_y"]).copy()

    completed = plot_data[plot_data["is_completed"]].copy()
    incomplete = plot_data[~plot_data["is_completed"]].copy()

    pitch = Pitch(
        pitch_type="statsbomb",
        pitch_color="#c7dfb4",
        line_color="#8aa57a",
        linewidth=1.2
    )

    fig, ax = pitch.draw(figsize=(12, 8))
    fig.patch.set_facecolor("#c7dfb4")

    # Successful passes
    if len(completed) > 0:
        pitch.arrows(
            completed["x"],
            completed["y"],
            completed["end_x"],
            completed["end_y"],
            ax=ax,
            color="#13b26b",
            width=1.5,
            headwidth=4,
            headlength=4,
            alpha=0.9,
            label="Successful passes"
        )

    # Unsuccessful passes
    if len(incomplete) > 0:
        pitch.arrows(
            incomplete["x"],
            incomplete["y"],
            incomplete["end_x"],
            incomplete["end_y"],
            ax=ax,
            color="#d84b4b",
            width=1.5,
            headwidth=4,
            headlength=4,
            alpha=0.9,
            label="Unsuccessful passes"
        )

    chart_title = title or f"Pass Map — {player_name}"

    ax.set_title(
        chart_title,
        fontsize=18,
        pad=18
    )

    subtitle_parts = []

    if team_name:
        subtitle_parts.append(team_name)

    if match_label:
        subtitle_parts.append(match_label)

    if match_date:
        subtitle_parts.append(str(match_date))

    if source:
        subtitle_parts.append(source)

    if subtitle_parts:
        fig.text(
            0.5,
            0.92,
            " | ".join(subtitle_parts),
            ha="center",
            fontsize=10
        )

    legend = ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.02),
        ncol=2,
        frameon=False,
        fontsize=10
    )

    return fig, ax