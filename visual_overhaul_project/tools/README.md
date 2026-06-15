# Visual Overhaul Tools

Development-only helpers for visual-overhaul research and validation.

## Baseline Screenshot Capture

`capture_baseline_screenshots.py` creates an isolated temporary SQLite database,
seeds representative study data, drives the CustomTkinter app through its frame
controller, and writes screenshots under:

```text
visual_overhaul_project/01_context/screenshots/baseline/
```

It does not use or modify the normal app database at
`study_test_tool/data/database/study_tool.db`.

## Requirements

- macOS Screen Recording permission enabled for the terminal app running Codex
  or the command, usually iTerm2.
- Project dependencies installed from `study_test_tool/requirements.txt`.
- `pyobjc-framework-Quartz` installed for dev screenshot window-bound detection.
- Writable Matplotlib and XDG cache directories.

If Screen Recording is missing, captures can show only the desktop wallpaper or
menu bar even though the app window exists.

## Commands

Full light/dark baseline capture:

```bash
MPLCONFIGDIR=/private/tmp/study-test-tool-mpl \
XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg \
PYTHONPATH=study_test_tool \
python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both
```

Validate existing screenshots without launching the GUI:

```bash
PYTHONPATH=study_test_tool \
python3 visual_overhaul_project/tools/capture_baseline_screenshots.py \
  --mode both --validate-only
```

Capture one group:

```bash
MPLCONFIGDIR=/private/tmp/study-test-tool-mpl \
XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg \
PYTHONPATH=study_test_tool \
python3 visual_overhaul_project/tools/capture_baseline_screenshots.py \
  --mode dark --group test-taking
```

Capture named states:

```bash
MPLCONFIGDIR=/private/tmp/study-test-tool-mpl \
XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg \
PYTHONPATH=study_test_tool \
python3 visual_overhaul_project/tools/capture_baseline_screenshots.py \
  --mode light --states home_empty_state
```

Use `--no-validate` only while debugging a capture failure. Normal runs validate
all expected output files after capture.
