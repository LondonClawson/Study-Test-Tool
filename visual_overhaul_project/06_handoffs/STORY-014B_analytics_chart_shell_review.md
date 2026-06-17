# STORY-014B Analytics Chart Shell Review

Story/Task:
`STORY-014B_analytics_chart_shell.md`

Review status:
Accepted. Marked `Done` on 2026-06-16.

Review scope:
- Checked `study_test_tool/gui/analytics_view.py`,
  `study_test_tool/gui/components/graph_widget.py`, and
  `study_test_tool/gui/styles.py` against the story's chart-shell scope.
- Confirmed the story did not intentionally change analytics calculations,
  service APIs, database queries, chart titles, axis meanings, test filter
  values, or Weak Topics grouping semantics.
- Kept unrelated `STORY-015A` in-progress Review screen work isolated.

Evidence reviewed:
- `visual_overhaul_project/01_context/screenshots/after/STORY-014B/light/light_analytics_populated.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014B/light/light_analytics_test_comparison.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014B/light/light_analytics_study_activity.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014B/light/light_analytics_minimum_score_trends.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014B/light/light_analytics_no_data.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014B/dark/dark_analytics_populated.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014B/dark/dark_analytics_test_comparison.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014B/dark/dark_analytics_study_activity.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014B/dark/dark_analytics_minimum_score_trends.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014B/dark/dark_analytics_no_data.png`

Verification performed:
- `python3 -m compileall -q study_test_tool/gui/analytics_view.py study_test_tool/gui/components/graph_widget.py study_test_tool/gui/styles.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/analytics_view.py study_test_tool/gui/components/graph_widget.py study_test_tool/gui/styles.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests/test_analytics_service.py`
- `PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --mode both --states analytics_populated analytics_test_comparison analytics_study_activity analytics_minimum_score_trends analytics_no_data --output visual_overhaul_project/01_context/screenshots/after/STORY-014B`

Acceptance notes:
- Chart tabs and the test filter now sit in a shared controls surface with a
  clearer hierarchy.
- `GraphWidget` centralizes matplotlib chart role resolution, which is the right
  maintenance direction for future chart styling.
- Figure, plot, text, grid, and primary series colors follow shared chart roles
  in light and dark mode.
- Chart no-data states use a designed surface instead of a plain gray label.
- Existing service calls remain the same for Score Trends, Test Comparison,
  Study Activity, and Weak Topics.

Residual risks:
- The Study Activity screenshot only proves a one-day populated data state; the
  single bar renders very wide. This is not a blocker for chart-shell acceptance,
  but it should be covered by `STORY-016_light_dark_and_min_size_validation.md`
  or a later chart-readability follow-up.
- Analytics and Review now repeat some local control-style helper patterns. Do
  not refactor broadly yet, but after the next matching screen lands, extract
  small shared helpers for page headers, control surfaces, and empty states if
  the repetition remains stable.

Tests not run:
Full pytest was not run. The focused analytics service tests and visual
validation cover the changed behavior surface for this chart-shell story.
