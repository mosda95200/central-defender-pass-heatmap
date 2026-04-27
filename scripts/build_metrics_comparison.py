from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def build_metrics_comparison(
    metrics_dir: str | Path,
    output_file: str | Path,
) -> None:
    metrics_dir = Path(metrics_dir)
    output_file = Path(output_file)

    if not metrics_dir.exists():
        raise FileNotFoundError(f"Metrics directory not found: {metrics_dir}")

    metric_files = sorted(metrics_dir.glob("*_metrics.csv"))

    if len(metric_files) == 0:
        print(f"No metrics files found in: {metrics_dir}")
        return

    dataframes = []

    for file in metric_files:
        df = pd.read_csv(file)
        df["source_file"] = file.name
        dataframes.append(df)

    comparison_df = pd.concat(dataframes, ignore_index=True)

    comparison_df = comparison_df.sort_values(
        by=["team", "player"]
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)

    comparison_df.to_csv(
        output_file,
        index=False,
        encoding="utf-8"
    )

    print(f"Loaded {len(metric_files)} metrics file(s).")
    print(f"Comparison file saved to: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build a comparison CSV from all player metrics files."
    )

    parser.add_argument(
        "--metrics-dir",
        default="outputs/metrics",
        help="Directory containing player metrics CSV files.",
    )

    parser.add_argument(
        "--output-file",
        default="outputs/metrics/euro_2024_final_centre_backs_comparison.csv",
        help="Output comparison CSV file.",
    )

    args = parser.parse_args()

    build_metrics_comparison(
        metrics_dir=args.metrics_dir,
        output_file=args.output_file,
    )