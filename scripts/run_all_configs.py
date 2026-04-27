from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.generate_player_pass_analysis import main


def find_config_files(config_dir: str | Path, recursive: bool = True) -> list[Path]:
    """
    Find JSON config files in a directory.
    """
    config_dir = Path(config_dir)

    if not config_dir.is_absolute():
        config_dir = PROJECT_ROOT / config_dir

    print(f"Project root: {PROJECT_ROOT}")
    print(f"Config directory: {config_dir}")
    print(f"Recursive search: {recursive}")

    if not config_dir.exists():
        raise FileNotFoundError(f"Config directory not found: {config_dir}")

    pattern = "**/*.json" if recursive else "*.json"

    config_files = sorted(config_dir.glob(pattern))

    return config_files


def run_all_configs(config_dir: str | Path, recursive: bool = True) -> None:
    """
    Run the pass analysis pipeline for all JSON config files.
    """
    print("Searching config files...")

    config_files = find_config_files(
        config_dir=config_dir,
        recursive=recursive
    )

    print(f"Found {len(config_files)} config file(s).")

    if len(config_files) == 0:
        print("No config files found. Nothing to run.")
        return

    for config_file in config_files:
        print()
        print("=" * 80)
        print(f"Running config: {config_file}")
        print("=" * 80)

        try:
            main(config_path=str(config_file))
        except Exception as error:
            print()
            print(f"Error while running config: {config_file}")
            print(f"Error: {error}")
            print("Continuing with next config...")

    print()
    print("=" * 80)
    print("All configs processed.")
    print("=" * 80)


if __name__ == "__main__":
    print("Starting run_all_configs.py...")

    parser = argparse.ArgumentParser(
        description="Run pass analysis for all JSON config files."
    )

    parser.add_argument(
        "--config-dir",
        default="configs/generated/euro_2024_final",
        help="Directory containing JSON config files.",
    )

    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Only read JSON files directly inside config-dir, not subdirectories.",
    )

    args = parser.parse_args()

    run_all_configs(
        config_dir=args.config_dir,
        recursive=not args.no_recursive
    )