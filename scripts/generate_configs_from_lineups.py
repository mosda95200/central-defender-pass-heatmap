from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
from statsbombpy import sb

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils import slugify_text, ensure_directory


def positions_to_list(positions) -> list[str]:
    """
    Extract all position names from the StatsBomb lineup positions field.
    """
    if not isinstance(positions, list):
        return []

    position_names = []

    for item in positions:
        if isinstance(item, dict) and item.get("position"):
            position_names.append(item["position"])

    return position_names


def extract_main_position(positions) -> str | None:
    """
    Extract the first listed position from the StatsBomb lineup positions field.
    """
    position_names = positions_to_list(positions)

    if len(position_names) == 0:
        return None

    return position_names[0]


def has_played(positions) -> bool:
    """
    A player is considered as having played if the positions list is not empty.
    """
    return isinstance(positions, list) and len(positions) > 0


def position_matches_filter(
    positions: list[str],
    position_filter: str | None
) -> bool:
    """
    Return True if one of the player's positions matches the requested filter.
    """
    if position_filter is None:
        return True

    position_filter = position_filter.lower()

    return any(
        position_filter in position.lower()
        for position in positions
    )


def build_players_dataframe(match_id: int) -> pd.DataFrame:
    """
    Load StatsBomb lineups and return a single DataFrame for both teams.
    """
    lineups = sb.lineups(match_id=match_id)

    players = []

    for team_name, lineup_df in lineups.items():
        temp = lineup_df.copy()
        temp["team"] = team_name
        players.append(temp)

    players_df = pd.concat(players, ignore_index=True)

    players_df["has_played"] = players_df["positions"].apply(has_played)
    players_df["all_positions"] = players_df["positions"].apply(positions_to_list)
    players_df["main_position"] = players_df["positions"].apply(extract_main_position)

    return players_df


def create_player_config(
    competition_id: int,
    season_id: int,
    match_id: int,
    player_name: str,
) -> dict:
    """
    Create the JSON configuration for one player.
    """
    return {
        "competition_id": competition_id,
        "season_id": season_id,
        "match_id": match_id,
        "player_name": player_name,
        "data_source": "StatsBomb Open Data",
        "event_type": "Pass",
        "analysis_type": "Pass density heatmap and pass map",
        "generate_heatmap": True,
        "generate_passmap": True,
    }


def save_config(
    config: dict,
    output_dir: Path,
    team_name: str,
    player_name: str,
) -> Path:
    """
    Save one player configuration as a JSON file.
    """
    team_slug = slugify_text(team_name)
    player_slug = slugify_text(player_name)

    output_path = output_dir / f"{team_slug}_{player_slug}.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=2, ensure_ascii=False)

    return output_path


def main(
    competition_id: int,
    season_id: int,
    match_id: int,
    output_dir: str,
    position_filter: str | None,
) -> None:
    output_dir = ensure_directory(output_dir)

    print("Loading lineups...")
    players_df = build_players_dataframe(match_id=match_id)

    players_played = players_df[
        players_df["has_played"]
    ].copy()

    if position_filter:
        players_filtered = players_played[
            players_played["all_positions"].apply(
                lambda positions: position_matches_filter(
                    positions,
                    position_filter
                )
            )
        ].copy()
    else:
        players_filtered = players_played.copy()

    players_filtered = players_filtered.sort_values(
        by=["team", "jersey_number"]
    )

    print("Players selected")
    print("----------------")
    print(
        players_filtered[
            [
                "team",
                "player_name",
                "jersey_number",
                "main_position",
                "all_positions",
            ]
        ].to_string(index=False)
    )

    print()
    print("Generating config files...")

    generated_files = []

    for _, row in players_filtered.iterrows():
        config = create_player_config(
            competition_id=competition_id,
            season_id=season_id,
            match_id=match_id,
            player_name=row["player_name"],
        )

        output_path = save_config(
            config=config,
            output_dir=output_dir,
            team_name=row["team"],
            player_name=row["player_name"],
        )

        generated_files.append(output_path)

        print(f"Created: {output_path}")

    print()
    print(f"Generated {len(generated_files)} config file(s).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate player config files from StatsBomb match lineups."
    )

    parser.add_argument(
        "--competition-id",
        type=int,
        required=True,
        help="StatsBomb competition ID.",
    )

    parser.add_argument(
        "--season-id",
        type=int,
        required=True,
        help="StatsBomb season ID.",
    )

    parser.add_argument(
        "--match-id",
        type=int,
        required=True,
        help="StatsBomb match ID.",
    )

    parser.add_argument(
        "--output-dir",
        default="configs/generated/euro_2024_final",
        help="Directory where JSON config files will be generated.",
    )

    parser.add_argument(
        "--position-filter",
        default="Center Back",
        help=(
            "Position filter. Example: 'Center Back'. "
            "Use an empty string to generate configs for all players."
        ),
    )

    args = parser.parse_args()

    position_filter = args.position_filter.strip()

    if position_filter == "":
        position_filter = None

    main(
        competition_id=args.competition_id,
        season_id=args.season_id,
        match_id=args.match_id,
        output_dir=args.output_dir,
        position_filter=position_filter,
    )