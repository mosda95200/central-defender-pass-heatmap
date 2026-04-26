from __future__ import annotations

import numpy as np
import pandas as pd
from statsbombpy import sb


def extract_coordinate(value, index: int):
    """
    Extract a coordinate from a StatsBomb location list.
    """
    if isinstance(value, list) and len(value) > index:
        return value[index]

    return np.nan


def load_analysis_context(
    competition_id: int,
    season_id: int,
    match_id: int
) -> dict:
    """
    Load competition and match context from StatsBomb.
    """
    competitions = sb.competitions()

    selected_competition = competitions[
        (competitions["competition_id"] == competition_id)
        & (competitions["season_id"] == season_id)
    ].iloc[0]

    matches = sb.matches(
        competition_id=competition_id,
        season_id=season_id
    )

    selected_match = matches[
        matches["match_id"] == match_id
    ].iloc[0]

    match_label = (
        f"{selected_match['home_team']} {selected_match['home_score']} - "
        f"{selected_match['away_score']} {selected_match['away_team']}"
    )

    return {
        "competition_name": selected_competition["competition_name"],
        "season_name": selected_competition["season_name"],
        "country_name": selected_competition["country_name"],
        "match_date": selected_match["match_date"],
        "home_team": selected_match["home_team"],
        "away_team": selected_match["away_team"],
        "home_score": selected_match["home_score"],
        "away_score": selected_match["away_score"],
        "competition_stage": selected_match["competition_stage"],
        "match_label": match_label,
    }


def prepare_player_passes(
    match_id: int,
    player_name: str
) -> pd.DataFrame:
    """
    Load StatsBomb events, filter selected player's passes,
    and prepare pass coordinates/features.
    """
    events = sb.events(match_id=match_id)

    passes = events[
        events["type"] == "Pass"
    ].copy()

    player_passes = passes[
        passes["player"] == player_name
    ].copy()

    if player_passes.empty:
        available_players = (
            events[["player"]]
            .dropna()
            .drop_duplicates()
            .sort_values("player")
        )

        raise ValueError(
            f"No passes found for player: {player_name}. "
            f"Check the exact StatsBomb player name. "
            f"Available players include: {available_players['player'].head(20).tolist()}"
        )

    player_passes["x"] = player_passes["location"].apply(
        lambda value: extract_coordinate(value, 0)
    )

    player_passes["y"] = player_passes["location"].apply(
        lambda value: extract_coordinate(value, 1)
    )

    player_passes["end_x"] = player_passes["pass_end_location"].apply(
        lambda value: extract_coordinate(value, 0)
    )

    player_passes["end_y"] = player_passes["pass_end_location"].apply(
        lambda value: extract_coordinate(value, 1)
    )

    player_passes["is_completed"] = player_passes["pass_outcome"].isna()

    player_passes["x_progression"] = player_passes["end_x"] - player_passes["x"]
    player_passes["y_progression"] = player_passes["end_y"] - player_passes["y"]

    player_passes["is_forward_pass"] = player_passes["x_progression"] > 0
    player_passes["is_long_pass"] = player_passes["pass_length"] >= 30

    required_columns = ["x", "y", "end_x", "end_y"]

    missing_values = player_passes[required_columns].isna().sum()

    if missing_values.sum() > 0:
        raise ValueError(
            f"Missing coordinates found: {missing_values.to_dict()}"
        )

    return player_passes


def create_clean_pass_dataset(player_passes: pd.DataFrame) -> pd.DataFrame:
    """
    Create a clean DataFrame with only the useful pass columns.
    """
    columns = [
        "match_id",
        "team",
        "player",
        "position",
        "minute",
        "second",
        "x",
        "y",
        "end_x",
        "end_y",
        "pass_length",
        "pass_angle",
        "pass_height",
        "pass_outcome",
        "pass_recipient",
        "is_completed",
        "x_progression",
        "y_progression",
        "is_forward_pass",
        "is_long_pass",
    ]

    existing_columns = [
        column for column in columns
        if column in player_passes.columns
    ]

    return player_passes[existing_columns].copy()


def calculate_pass_metrics(player_passes: pd.DataFrame) -> dict:
    """
    Calculate pass metrics for a player.
    """
    total_passes = len(player_passes)
    completed_passes = int(player_passes["is_completed"].sum())
    incomplete_passes = total_passes - completed_passes

    completion_rate = completed_passes / total_passes if total_passes > 0 else 0

    forward_passes = int(player_passes["is_forward_pass"].sum())
    forward_pass_share = forward_passes / total_passes if total_passes > 0 else 0

    long_passes = int(player_passes["is_long_pass"].sum())
    long_pass_share = long_passes / total_passes if total_passes > 0 else 0

    average_pass_length = player_passes["pass_length"].mean()

    return {
        "total_passes": total_passes,
        "completed_passes": completed_passes,
        "incomplete_passes": incomplete_passes,
        "completion_rate": completion_rate,
        "forward_passes": forward_passes,
        "forward_pass_share": forward_pass_share,
        "long_passes": long_passes,
        "long_pass_share": long_pass_share,
        "average_pass_length": average_pass_length,
    }