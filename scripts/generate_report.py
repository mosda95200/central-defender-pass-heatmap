from __future__ import annotations

import argparse
import os
from pathlib import Path

import pandas as pd


def make_relative_link(target: Path, base_dir: Path) -> str:
    """
    Create a Markdown-compatible relative path from base_dir to target.
    """
    return Path(os.path.relpath(target, start=base_dir)).as_posix()


def format_value(value) -> str:
    """
    Format values for Markdown tables.
    """
    if pd.isna(value):
        return ""

    if isinstance(value, float):
        return f"{value:.1f}"

    return str(value)


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    """
    Convert a DataFrame to a Markdown table without requiring tabulate.
    """
    if df.empty:
        return "_No data available._"

    columns = list(df.columns)

    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"

    rows = []

    for _, row in df.iterrows():
        values = [
            format_value(row[column]).replace("|", "\\|")
            for column in columns
        ]
        rows.append("| " + " | ".join(values) + " |")

    return "\n".join([header, separator] + rows)


def load_comparison_table(comparison_file: Path) -> pd.DataFrame:
    """
    Load and format the centre-back comparison table.
    """
    df = pd.read_csv(comparison_file)

    columns_to_keep = [
        "player",
        "team",
        "position",
        "total_passes",
        "completed_passes",
        "incomplete_passes",
        "completion_rate_pct",
        "forward_passes",
        "forward_pass_share_pct",
        "long_passes",
        "long_pass_share_pct",
        "average_pass_length",
    ]

    existing_columns = [
        column for column in columns_to_keep
        if column in df.columns
    ]

    df = df[existing_columns].copy()

    rename_map = {
        "player": "Player",
        "team": "Team",
        "position": "Position",
        "total_passes": "Total passes",
        "completed_passes": "Completed passes",
        "incomplete_passes": "Incomplete passes",
        "completion_rate_pct": "Completion rate (%)",
        "forward_passes": "Forward passes",
        "forward_pass_share_pct": "Forward pass share (%)",
        "long_passes": "Long passes",
        "long_pass_share_pct": "Long pass share (%)",
        "average_pass_length": "Average pass length",
    }

    df = df.rename(columns=rename_map)

    numeric_columns = [
        "Completion rate (%)",
        "Forward pass share (%)",
        "Long pass share (%)",
        "Average pass length",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = df[column].round(1)

    if "Total passes" in df.columns:
        df = df.sort_values("Total passes", ascending=False)

    return df


def build_profile_summary(profile_file: Path) -> str:
    """
    Build a readable profile summary section.
    """
    if not profile_file.exists():
        return "_Profile summary file not found._"

    profile_df = pd.read_csv(profile_file)

    if profile_df.empty:
        return "_No profile summary available._"

    lines = []

    for _, row in profile_df.iterrows():
        insight = row.get("insight", "")
        player = row.get("player", "")
        team = row.get("team", "")
        value = row.get("value", "")
        metric = row.get("metric", "")

        lines.append(
            f"- **{insight}**: {player} ({team}) — {value} `{metric}`"
        )

    return "\n".join(lines)


def build_chart_section(charts_dir: Path, report_dir: Path) -> str:
    """
    Build Markdown image links for comparison charts.
    """
    chart_files = [
        ("Total passes", "total_passes_comparison.png"),
        ("Completion rate", "completion_rate_comparison.png"),
        ("Forward pass share", "forward_pass_share_comparison.png"),
        ("Long pass share", "long_pass_share_comparison.png"),
        ("Average pass length", "average_pass_length_comparison.png"),
    ]

    sections = []

    for title, filename in chart_files:
        chart_path = charts_dir / filename

        if chart_path.exists():
            relative_path = make_relative_link(chart_path, report_dir)
            sections.append(f"### {title}\n\n![{title}]({relative_path})")
        else:
            sections.append(f"### {title}\n\n_File not found: `{chart_path}`_")

    return "\n\n".join(sections)


def build_player_visuals_section(
    heatmaps_dir: Path,
    passmaps_dir: Path,
    report_dir: Path,
) -> str:
    """
    Build Markdown sections for each player's heatmap and pass map.
    """
    heatmap_files = sorted(heatmaps_dir.glob("*_pass_density_heatmap.png"))

    if len(heatmap_files) == 0:
        return "_No heatmaps found._"

    sections = []

    for heatmap_path in heatmap_files:
        player_slug = heatmap_path.name.replace("_pass_density_heatmap.png", "")
        passmap_path = passmaps_dir / f"{player_slug}_pass_map.png"

        player_title = player_slug.replace("_", " ").title()

        heatmap_relative = make_relative_link(heatmap_path, report_dir)

        section = [
            f"### {player_title}",
            "",
            "**Pass density heatmap**",
            "",
            f"![{player_title} pass density heatmap]({heatmap_relative})",
        ]

        if passmap_path.exists():
            passmap_relative = make_relative_link(passmap_path, report_dir)
            section.extend(
                [
                    "",
                    "**Pass map**",
                    "",
                    f"![{player_title} pass map]({passmap_relative})",
                ]
            )
        else:
            section.extend(
                [
                    "",
                    f"_Pass map not found: `{passmap_path}`_",
                ]
            )

        sections.append("\n".join(section))

    return "\n\n---\n\n".join(sections)


def build_report(
    comparison_file: Path,
    profile_file: Path,
    heatmaps_dir: Path,
    passmaps_dir: Path,
    charts_dir: Path,
    output_file: Path,
) -> None:
    """
    Build the final Markdown report.
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)

    report_dir = output_file.parent

    comparison_df = load_comparison_table(comparison_file)
    comparison_markdown = dataframe_to_markdown(comparison_df)

    profile_summary = build_profile_summary(profile_file)
    chart_section = build_chart_section(charts_dir, report_dir)
    player_visuals_section = build_player_visuals_section(
        heatmaps_dir=heatmaps_dir,
        passmaps_dir=passmaps_dir,
        report_dir=report_dir,
    )

    report = f"""# Euro 2024 Final — Centre-Back Passing Analysis

## Project context

This report analyses the centre-backs who participated in the Euro 2024 final between Spain and England.

The analysis is based on StatsBomb Open Data and focuses on passing behaviour:

- pass volume;
- pass completion;
- forward passing;
- long passing;
- average pass length;
- pass density heatmaps;
- pass maps.

## Match context

| Field | Value |
|---|---|
| Competition | UEFA Euro |
| Season | 2024 |
| Match | Spain 2 - 1 England |
| Date | 2024-07-14 |
| Data source | StatsBomb Open Data |
| Event type | Pass |
| Population | Centre-backs |

## Comparison table

The table below excludes players with very low passing volume in order to avoid misleading interpretation from very small samples.

{comparison_markdown}

## Automatic profile summary

{profile_summary}

## Comparison charts

{chart_section}

## Player visualisations

{player_visuals_section}

## Methodological notes

- A completed pass is identified when `pass_outcome` is missing in StatsBomb event data.
- A forward pass is approximated with `end_x > x`.
- A long pass is defined with `pass_length >= 30`.
- The comparison is based on a single match and should not be interpreted as a full player profile across a season.
"""

    output_file.write_text(report, encoding="utf-8")

    print(f"Report saved to: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a Markdown report for centre-back passing analysis."
    )

    parser.add_argument(
        "--comparison-file",
        default="outputs/metrics/euro_2024_final_centre_backs_comparison_filtered.csv",
        help="Path to the filtered comparison CSV file.",
    )

    parser.add_argument(
        "--profile-file",
        default="outputs/metrics/euro_2024_final_centre_backs_profile_summary.csv",
        help="Path to the profile summary CSV file.",
    )

    parser.add_argument(
        "--heatmaps-dir",
        default="outputs/heatmaps",
        help="Directory containing pass density heatmaps.",
    )

    parser.add_argument(
        "--passmaps-dir",
        default="outputs/passmaps",
        help="Directory containing pass maps.",
    )

    parser.add_argument(
        "--charts-dir",
        default="outputs/comparison_charts",
        help="Directory containing comparison charts.",
    )

    parser.add_argument(
        "--output-file",
        default="outputs/reports/euro_2024_final_centre_backs_report.md",
        help="Output Markdown report file.",
    )

    args = parser.parse_args()

    build_report(
        comparison_file=Path(args.comparison_file),
        profile_file=Path(args.profile_file),
        heatmaps_dir=Path(args.heatmaps_dir),
        passmaps_dir=Path(args.passmaps_dir),
        charts_dir=Path(args.charts_dir),
        output_file=Path(args.output_file),
    )