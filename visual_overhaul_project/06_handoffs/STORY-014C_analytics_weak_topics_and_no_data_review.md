# STORY-014C Analytics Weak Topics And No-Data States - PM Review

Status:
Accepted. `STORY-014C_analytics_weak_topics_and_no_data.md` is Done as of
2026-06-16.

Review scope:
- Inspected the submitted Analytics Weak Topics implementation in
  `study_test_tool/gui/analytics_view.py`.
- Inspected the new Weak Topics screenshot harness states in
  `visual_overhaul_project/tools/capture_baseline_screenshots.py`.
- Reviewed light and dark screenshot evidence for Weak Topics grouped by Test,
  Group, and Category, plus no-category, no-data, and minimum-window states.
- Checked the work against the accepted `STORY-014B` chart-shell boundary so it
  stayed focused on Weak Topics and non-chart empty states.

Verification run by PM:
- `python3 -m compileall -q study_test_tool/gui/analytics_view.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/analytics_view.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests/test_analytics_service.py`
- `PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --mode both --states analytics_weak_topics_test analytics_weak_topics_group analytics_weak_topics_category analytics_weak_topics_minimum analytics_weak_topics_no_category analytics_weak_topics_no_data --output visual_overhaul_project/01_context/screenshots/after/STORY-014C`

Acceptance notes:
- Weak, moderate, and strong topic cards are visually distinct in light and dark
  mode through semantic status color, status pills, rails, and progress bars.
- Grouping controls remain mapped to the existing `test`, `group`, and
  `category` service values.
- No analytics service APIs, queries, weak-topic thresholds, category fallback
  behavior, or chart-shell behavior changed.
- No-data and no-category states are distinct and use actionable copy.
- The no-category screenshot fixture clears categories only in a temporary
  screenshot database.

Residual risks:
- Long topic names, dense Weak Topics lists, and deeper scrolling still belong
  in `STORY-016_light_dark_and_min_size_validation.md`.
- Analytics and Review now repeat local segmented-control and empty-state helper
  patterns. Defer extraction until validation shows the pattern is stable
  enough to share without broad refactor risk.
