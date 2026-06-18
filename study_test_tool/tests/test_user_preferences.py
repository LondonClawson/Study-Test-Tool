"""Tests for local user preference persistence."""

from config.user_preferences import (
    TEXT_SIZE_EXTRA_LARGE,
    TEXT_SIZE_LARGE,
    TEXT_SIZE_NORMAL,
    load_preferences,
    save_preferences,
)


def test_missing_preferences_file_uses_default(tmp_path):
    """Missing preference files fall back to the normal text size."""
    path = tmp_path / "preferences.json"

    preferences = load_preferences(path)

    assert preferences["text_size"] == TEXT_SIZE_NORMAL


def test_preferences_round_trip(tmp_path):
    """Saved text-size preferences can be loaded again."""
    path = tmp_path / "preferences.json"

    save_preferences({"text_size": TEXT_SIZE_LARGE}, path)
    preferences = load_preferences(path)

    assert preferences["text_size"] == TEXT_SIZE_LARGE


def test_unknown_text_size_uses_default(tmp_path):
    """Unsupported text-size labels are ignored."""
    path = tmp_path / "preferences.json"

    save_preferences({"text_size": "Huge"}, path)
    preferences = load_preferences(path)

    assert preferences["text_size"] == TEXT_SIZE_NORMAL


def test_malformed_preferences_file_uses_default(tmp_path):
    """Malformed JSON does not prevent startup."""
    path = tmp_path / "preferences.json"
    path.write_text("{not-json", encoding="utf-8")

    preferences = load_preferences(path)

    assert preferences["text_size"] == TEXT_SIZE_NORMAL


def test_invalid_saved_payload_uses_default(tmp_path):
    """Non-object preference payloads are ignored."""
    path = tmp_path / "preferences.json"
    path.write_text('["not", "an", "object"]', encoding="utf-8")

    preferences = load_preferences(path)

    assert preferences["text_size"] == TEXT_SIZE_NORMAL


def test_extra_large_preference_is_supported(tmp_path):
    """The accessibility-oriented largest option is valid."""
    path = tmp_path / "preferences.json"

    save_preferences({"text_size": TEXT_SIZE_EXTRA_LARGE}, path)
    preferences = load_preferences(path)

    assert preferences["text_size"] == TEXT_SIZE_EXTRA_LARGE
