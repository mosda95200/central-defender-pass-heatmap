"""
Functions for building pass heatmaps from football event data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import Pitch


def filter_passes(events: pd.DataFrame) -> pd.DataFrame:
    """
    Filter event data to keep only passes.
    """
    return events[events["type"] == "Pass"].copy()


def filter_player_passes(passes: pd.DataFrame, player_name: str) -> pd.DataFrame:
    """
    Filter passes for a specific player.
    """
    return passes[passes["player"] == player_name].copy()


def prepare_pass_coordinates(passes: pd.DataFrame) -> pd.DataFrame:
    """
    Extract start and end coordinates from StatsBomb pass data.
    """
    passes = passes.copy()

    passes["x"] = passes["location"].apply(lambda loc: loc[0] if isinstance(loc, list) else np.nan)
    passes["y"] = passes["location"].apply(lambda loc: loc[1] if isinstance(loc, list) else np.nan)

    passes["end_x"] = passes["pass_end_location"].apply(
        lambda loc: loc[0] if isinstance(loc, list) else np.nan
    )
    passes["end_y"] = passes["pass_end_location"].apply(
        lambda loc: loc[1] if isinstance(loc, list) else np.nan
    )

    passes["is_completed"] = passes["pass_outcome"].isna()

    return passes


def calculate_pass_metrics(passes: pd.DataFrame) -> dict:
    """
    Calculate basic pass metrics.
    """
    total_passes = len(passes)
    completed_passes = passes["is_completed"].sum()

    completion_rate = completed_passes / total_passes if total_passes > 0 else 0

    return {
        "total_passes": total_passes,
        "completed_passes": int(completed_passes),
        "completion_rate": completion_rate,
    }


def plot_pass_heatmap(passes: pd.DataFrame, player_name: str, title: str = None):
    """
    Plot a basic pass heatmap using pass start locations.
    """
    pitch = Pitch(
        pitch_type="statsbomb",
        pitch_color="white",
        line_color="black"
    )

    fig, ax = pitch.draw(figsize=(12, 8))

    pitch.kdeplot(
        passes["x"],
        passes["y"],
        ax=ax,
        fill=True,
        levels=100,
        thresh=0.05,
        alpha=0.6
    )

    ax.set_title(
        title or f"Pass Heatmap — {player_name}",
        fontsize=16
    )

    return fig, ax