# STORY-014A History List And Filters Review

Story/Task:
`STORY-014A_history_list_and_filters.md`

Review status:
Accepted. Marked `Done` on 2026-06-16.

Review scope:
- Checked `study_test_tool/gui/history_view.py` against the story's visual-only
  scope.
- Confirmed the story did not intentionally change persistence, query
  semantics, filter values, result navigation, service behavior, scoring,
  import/export, analytics, review, or session logic.
- Kept unrelated `STORY-014B` in-progress work isolated.

Evidence reviewed:
- `visual_overhaul_project/01_context/screenshots/after/STORY-014A/light/light_history_populated.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014A/light/light_history_filtered.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014A/light/light_history_loading_state.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014A/light/light_history_minimum_populated.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014A/light/light_history_empty_state.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014A/dark/dark_history_populated.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014A/dark/dark_history_filtered.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014A/dark/dark_history_loading_state.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014A/dark/dark_history_minimum_populated.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014A/dark/dark_history_empty_state.png`

Verification performed:
- `python3 -m compileall -q study_test_tool/gui/history_view.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/history_view.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --mode both --states history_populated history_filtered history_loading_state history_minimum_populated history_empty_state --output visual_overhaul_project/01_context/screenshots/after/STORY-014A`
- Direct row-click smoke confirming `_on_row_click()` still calls
  `SCREEN_RESULTS` with `attempt_id`.

Acceptance notes:
- Filters remain the same `All Tests` and `All Modes`/`Test`/`Practice` values
  and still use the existing client-side filter path.
- Header labels and rows use shared column sizing and were visually acceptable
  in normal and minimum-window screenshots.
- Attempt rows are visibly clickable through surface, border, spacing, cursor,
  and hover treatment without adding new behavior.
- Loading and empty states use foundation surfaces instead of plain gray text.
- Row-to-results navigation contract is unchanged.

Residual risks:
- Very long History test names were not covered by this story's seeded
  screenshots and should stay in `STORY-016_light_dark_and_min_size_validation.md`.
- The pre-existing `_load_data()` exception callback still closes over the
  exception variable before the scheduled callback runs. This was not introduced
  by `STORY-014A`; track it as a future non-visual bugfix if error-path
  robustness becomes part of a validation pass.

Tests not run:
Full pytest was not run. The accepted change is visual-only History GUI work,
and the focused checks covered the story's behavior-preservation risks.
