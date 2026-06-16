# Screenshot Evidence Policy

Use screenshot evidence to preserve a visible before/after trail through the
visual overhaul. The baseline screenshots are comparison evidence, not just
Sprint 0 documentation.

## When Screenshots Are Required

Capture after screenshots for a story when it changes a user-visible screen,
custom dialog, reusable surface pattern in a pilot screen, or any light/dark
visual treatment that needs review.

Required examples:

- Home, test-taking, results, editor, history, analytics, review, and dialog
  layout stories.
- Stories that change card, list row, page header, status badge, feedback, or
  action hierarchy in an actual screen state.
- Sprint review, light/dark validation, minimum-size validation, and MVP
  regression pass.

Screenshots are optional for low-level foundation stories that only add shared
style constants, helper functions, or wiring with no stable finished screen
state. Those stories still need a startup or targeted visual smoke check.

## What To Capture

- Capture light and dark mode for each touched state where practical.
- Capture minimum supported window size when the story changes layout, wrapping,
  density, scroll behavior, or two-column structure.
- Prefer the exact states named in the story. If the story does not name states,
  use `06_handoffs/screenshot_checklist.md` and the relevant context summary.
- Store after screenshots outside the baseline folder, for example:
  `01_context/screenshots/after/STORY-008/`.

## How To Use The Harness

The scripted harness seeds temporary app data, drives supported states, captures
screenshots, and validates that the files are readable screenshots.

Examples from the repository root:

```bash
python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --group home --output visual_overhaul_project/01_context/screenshots/after/STORY-008
python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --states home_populated_grouped home_empty_state --output visual_overhaul_project/01_context/screenshots/after/STORY-008
python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --output visual_overhaul_project/01_context/screenshots/after/STORY-008
```

Supported groups are `home`, `dialogs`, `editor`, `test-taking`, `results`,
`data`, `empty`, and `all`.

If the harness does not cover the needed state, use a manual screenshot and name
the state, mode, and capture path in the handoff.

## Handoff Evidence

Each implementation handoff should list:

- Screens and states checked.
- Screenshot paths for required after captures.
- Baseline screenshot paths or summary used for comparison.
- States that could not be captured and the exact reason.
- Manual checks used when screenshot capture was blocked.
