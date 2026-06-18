"""Local user preference persistence."""

import json
import os
from pathlib import Path
from typing import Dict, Optional

from config.settings import PREFERENCES_PATH

TEXT_SIZE_NORMAL = "Normal"
TEXT_SIZE_LARGE = "Large"
TEXT_SIZE_EXTRA_LARGE = "Extra Large"

TEXT_SIZE_SCALES: Dict[str, float] = {
    TEXT_SIZE_NORMAL: 1.0,
    TEXT_SIZE_LARGE: 1.15,
    TEXT_SIZE_EXTRA_LARGE: 1.3,
}
TEXT_SIZE_OPTIONS = list(TEXT_SIZE_SCALES.keys())

DEFAULT_PREFERENCES = {
    "text_size": TEXT_SIZE_NORMAL,
}


def get_text_size_scale(text_size: str) -> float:
    """Return the widget scale for a saved text-size label."""
    return TEXT_SIZE_SCALES.get(text_size, TEXT_SIZE_SCALES[TEXT_SIZE_NORMAL])


def validate_text_size(text_size: str) -> str:
    """Return a supported text-size label, falling back to the default."""
    if text_size in TEXT_SIZE_SCALES:
        return text_size
    return DEFAULT_PREFERENCES["text_size"]


def load_preferences(path: Optional[Path] = None) -> dict:
    """Load preferences from disk, tolerating missing or invalid files."""
    preferences_path = path or PREFERENCES_PATH
    try:
        with preferences_path.open("r", encoding="utf-8") as file:
            loaded = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return DEFAULT_PREFERENCES.copy()

    if not isinstance(loaded, dict):
        return DEFAULT_PREFERENCES.copy()

    preferences = DEFAULT_PREFERENCES.copy()
    preferences["text_size"] = validate_text_size(
        str(loaded.get("text_size", preferences["text_size"]))
    )
    return preferences


def save_preferences(preferences: dict, path: Optional[Path] = None) -> None:
    """Persist preferences to disk using an atomic replacement."""
    preferences_path = path or PREFERENCES_PATH
    normalized = DEFAULT_PREFERENCES.copy()
    normalized["text_size"] = validate_text_size(
        str(preferences.get("text_size", normalized["text_size"]))
    )

    preferences_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = preferences_path.with_suffix(preferences_path.suffix + ".tmp")
    with temp_path.open("w", encoding="utf-8") as file:
        json.dump(normalized, file, indent=2)
        file.write("\n")
    os.replace(temp_path, preferences_path)
