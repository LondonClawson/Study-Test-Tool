#!/usr/bin/env python3
"""Apply a PNG asset as the icon for a macOS .app bundle."""

import os
import plistlib
import sys
from pathlib import Path

from PIL import Image


ICON_FILE_NAME = "AppIcon.icns"
ICON_PLIST_VALUE = "AppIcon"
ICON_SIZES = [
    (16, 16),
    (32, 32),
    (64, 64),
    (128, 128),
    (256, 256),
    (512, 512),
    (1024, 1024),
]


def _plist_icon_value(plist_path: Path) -> str:
    """Return the configured bundle icon name, if any."""
    if not plist_path.exists():
        return ""

    with plist_path.open("rb") as plist_file:
        data = plistlib.load(plist_file)
    return str(data.get("CFBundleIconFile", ""))


def _icon_is_current(source_path: Path, icon_path: Path, plist_path: Path) -> bool:
    """Return whether the app bundle already has the current generated icon."""
    if not icon_path.exists():
        return False
    if icon_path.stat().st_mtime < source_path.stat().st_mtime:
        return False
    return _plist_icon_value(plist_path) == ICON_PLIST_VALUE


def _write_icns(source_path: Path, icon_path: Path) -> None:
    """Create an ICNS file from a square PNG source image."""
    image = Image.open(source_path).convert("RGBA")
    if image.width != image.height:
        raise ValueError(f"Icon source must be square: {source_path}")

    icon_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(icon_path, format="ICNS", sizes=ICON_SIZES)


def _write_plist_icon(plist_path: Path) -> None:
    """Set CFBundleIconFile in the app bundle Info.plist."""
    with plist_path.open("rb") as plist_file:
        data = plistlib.load(plist_file)

    data["CFBundleIconFile"] = ICON_PLIST_VALUE

    with plist_path.open("wb") as plist_file:
        plistlib.dump(data, plist_file)


def apply_app_icon(source_path: Path, app_bundle_path: Path) -> bool:
    """Apply source_path as app_bundle_path's icon.

    Returns:
        True when the app bundle was changed, False when it was already current.
    """
    if not source_path.is_file():
        raise FileNotFoundError(source_path)
    if not app_bundle_path.is_dir():
        raise FileNotFoundError(app_bundle_path)

    contents_path = app_bundle_path / "Contents"
    plist_path = contents_path / "Info.plist"
    resources_path = contents_path / "Resources"
    icon_path = resources_path / ICON_FILE_NAME

    if not plist_path.is_file():
        raise FileNotFoundError(plist_path)
    if _icon_is_current(source_path, icon_path, plist_path):
        return False

    _write_icns(source_path, icon_path)
    _write_plist_icon(plist_path)
    os.utime(app_bundle_path, None)
    return True


def main() -> int:
    """Run the app icon updater from the command line."""
    if len(sys.argv) != 3:
        print("Usage: app_icon.py <source-png> <app-bundle>", file=sys.stderr)
        return 2

    source_path = Path(sys.argv[1]).expanduser()
    app_bundle_path = Path(sys.argv[2]).expanduser()
    apply_app_icon(source_path, app_bundle_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
