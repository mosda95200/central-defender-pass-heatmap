from __future__ import annotations

import json
import unicodedata
from pathlib import Path


def load_config(config_path: str | Path) -> dict:
    """
    Load a JSON configuration file.
    """
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def slugify_text(text: str) -> str:
    """
    Convert text into a clean filename-friendly slug.
    """
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = text.replace(" ", "_")
    text = text.replace("-", "_")

    text = "".join(
        character for character in text
        if character.isalnum() or character == "_"
    )

    while "__" in text:
        text = text.replace("__", "_")

    return text.strip("_")


def ensure_directory(path: str | Path) -> Path:
    """
    Create a directory if it does not already exist.
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path