Story/Task:
`STORY-014A_history_list_and_filters.md`

Status:
Submitted For Review. PM/reviewer acceptance is still required; this is not
marked Done.

Summary:
Polished the History screen page header, filter surface, table header, attempt
rows, hover/click affordance, loading state, empty state, and minimum-window
layout. History persistence, query semantics, filter values, background loading
flow, and row-to-results navigation were preserved.

Files changed:
- `study_test_tool/gui/history_view.py`
- `visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/04_stories/STORY-014A_history_list_and_filters.md`
- `visual_overhaul_project/06_handoffs/STORY-014A_history_list_and_filters_handoff.md`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014A/`

Definition of Ready checked:
Yes. `STORY-014A` was Ready and unblocked before claiming. CTX-DATA-VIEWS,
CTX-FOUNDATION, and the accepted `STORY-005`, `STORY-006`, and `STORY-007`
handoffs were read.

Context summaries read:
- `visual_overhaul_project/01_context/summaries/history_analytics_review_context.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/06_handoffs/STORY-005_button_hierarchy_handoff.md`
- `visual_overhaul_project/06_handoffs/STORY-006_card_and_list_patterns_handoff.md`
- `visual_overhaul_project/06_handoffs/STORY-007_page_header_pattern_handoff.md`

Context summaries created/updated:
None.

Screens/states checked:
- Populated History in light and dark mode.
- Filtered History in light and dark mode.
- Loading History in light and dark mode.
- Empty History in light and dark mode.
- Minimum-window populated History in light and dark mode.
- Focused GUI smoke for synchronous data load, filtering to one attempt,
  filtered-empty state, and row click routing to Results with the same attempt
  id.

Screenshot evidence:
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

Tests run:
- `python3 -m compileall -q study_test_tool/gui/history_view.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/history_view.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- Focused History GUI smoke with seeded temporary data for loading state,
  populated attempts, filtered attempts, filtered-empty state, and row-to-results
  routing.
- `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --states history_populated history_filtered history_loading_state history_minimum_populated history_empty_state --output visual_overhaul_project/01_context/screenshots/after/STORY-014A`
- `PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --mode both --states history_populated history_filtered history_loading_state history_minimum_populated history_empty_state --output visual_overhaul_project/01_context/screenshots/after/STORY-014A`
- `git diff --check`

Tests not run and why:
Full pytest was not run. The application change is visual-only History GUI work,
and the focused GUI smoke covered the behavior-preservation risks named by the
story. No service, database, persistence, scoring, analytics, or review logic
changed.

Acceptance criteria notes:
- History filters remain in the same values and still update the existing
  client-side filtering path.
- Header labels and attempt rows now share column sizing and stay aligned in
  normal and minimum-window captures.
- Attempt rows use semantic surfaces, borders, spacing, and hover treatment so
  they read as clickable without adding new behavior.
- Loading and empty states now use designed surfaces instead of plain gray
  labels.
- Row-to-results navigation still calls `SCREEN_RESULTS` with the selected
  attempt id.

Risks:
- The History table still uses fixed minimum column widths. Very long test names
  should be included in `STORY-016_light_dark_and_min_size_validation.md`.
- The loading-state screenshot is harness-driven so the transient state can be
  captured deterministically; runtime loading still uses the existing background
  thread path.

Follow-up backlog items:
- Include long History test names and unusually small window validation in
  `STORY-016_light_dark_and_min_size_validation.md`.
- Consider a future non-visual bugfix for the pre-existing History load-error
  callback, which still closes over the exception variable before the scheduled
  main-thread callback runs. This was outside `STORY-014A` because the submitted
  work did not change the exception-capture contract.

PM review decision:
Accepted on 2026-06-16. The review checked current History code, the submitted
light/dark populated, filtered, loading, empty, and minimum-window screenshots,
and direct row-to-results routing. Compile, Black, screenshot validation, and a
focused row-click smoke all passed. Full pytest remains skipped because no
service, database, scoring, import/export, analytics, review, or session logic
changed.
