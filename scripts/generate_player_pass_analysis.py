from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt

from src.utils import load_config, slugify_text, ensure_directory
from src.data_preparation import (
    load_analysis_context,
    prepare_player_passes,
    create_clean_pass_dataset,
    calculate_pass_metrics,
    create_metrics_dataframe,
)
from src.visualizations import (
    plot_pass_density_heatmap,
    plot_pass_map,
)


def main(config_path: str) -> None:
    config = load_config(config_path)

    competition_id = config["competition_id"]
    season_id = config["season_id"]
    match_id = config["match_id"]
    player_name = config["player_name"]
    data_source = config.get("data_source", "StatsBomb Open Data")

    generate_heatmap = config.get("generate_heatmap", True)
    generate_passmap = config.get("generate_passmap", True)

    print("Loading analysis context...")
    context = load_analysis_context(
        competition_id=competition_id,
        season_id=season_id,
        match_id=match_id,
    )

    print("Preparing player passes...")
    player_passes = prepare_player_passes(
        match_id=match_id,
        player_name=player_name,
    )

    player_passes_clean = create_clean_pass_dataset(player_passes)

    team_name = player_passes_clean["team"].mode()[0]
    position_name = player_passes_clean["position"].mode()[0]

    metrics = calculate_pass_metrics(player_passes_clean)

    player_slug = slugify_text(player_name)

    heatmap_dir = ensure_directory("outputs/heatmaps")
    passmap_dir = ensure_directory("outputs/passmaps")
    metrics_dir = ensure_directory("outputs/metrics")

    metrics_df = create_metrics_dataframe(
        metrics=metrics,
        player_name=player_name,
        team_name=team_name,
        position_name=position_name,
        context=context,
    )

    metrics_output = metrics_dir / f"{player_slug}_metrics.csv"

    metrics_df.to_csv(
        metrics_output,
        index=False,
        encoding="utf-8",
    )

    print(f"Metrics saved to: {metrics_output}")

    print("Analysis summary")
    print("----------------")
    print(f"Player: {player_name}")
    print(f"Team: {team_name}")
    print(f"Position: {position_name}")
    print(f"Competition: {context['competition_name']}")
    print(f"Season: {context['season_name']}")
    print(f"Match: {context['match_label']}")
    print(f"Date: {context['match_date']}")
    print(f"Total passes: {metrics['total_passes']}")
    print(f"Completed passes: {metrics['completed_passes']}")
    print(f"Completion rate: {metrics['completion_rate']:.1%}")

    if generate_heatmap:
        print("Generating pass density heatmap...")

        fig, ax = plot_pass_density_heatmap(
            passes=player_passes_clean,
            player_name=player_name,
            team_name=team_name,
            season_label=context["season_name"],
            match_label=context["match_label"],
            match_date=context["match_date"],
            source=data_source,
        )

        heatmap_output = heatmap_dir / f"{player_slug}_pass_density_heatmap.png"

        fig.savefig(
            heatmap_output,
            dpi=300,
            bbox_inches="tight",
            facecolor=fig.get_facecolor(),
        )

        plt.close(fig)

        print(f"Heatmap saved to: {heatmap_output}")

    if generate_passmap:
        print("Generating pass map...")

        fig, ax = plot_pass_map(
            passes=player_passes_clean,
            player_name=player_name,
            team_name=team_name,
            season_label=context["season_name"],
            match_label=context["match_label"],
            match_date=context["match_date"],
            source=data_source,
        )

        passmap_output = passmap_dir / f"{player_slug}_pass_map.png"

        fig.savefig(
            passmap_output,
            dpi=300,
            bbox_inches="tight",
            facecolor=fig.get_facecolor(),
        )

        plt.close(fig)

        print(f"Pass map saved to: {passmap_output}")

    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate pass heatmap and pass map for one player."
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to JSON config file.",
    )

    args = parser.parse_args()

    main(config_path=args.config)