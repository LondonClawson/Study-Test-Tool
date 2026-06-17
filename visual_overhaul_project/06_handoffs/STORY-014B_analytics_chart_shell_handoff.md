Story/Task:
`STORY-014B_analytics_chart_shell.md`

Status:
Submitted For Review. PM/reviewer acceptance is still required.

Summary:
Polished the Analytics chart-tab shell without changing analytics calculations.
The page now uses the shared page header, semantic controls, a chart card/surface,
and chart-tab no-data surfaces. `GraphWidget` now derives matplotlib figure,
axes, text, grid, and series colors from shared chart roles so light and dark
charts align with CTX-FOUNDATION.

Files changed:
- `study_test_tool/gui/analytics_view.py`
- `study_test_tool/gui/components/graph_widget.py`
- `study_test_tool/gui/styles.py`
- `visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `visual_overhaul_project/04_stories/STORY-014B_analytics_chart_shell.md`
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/06_handoffs/STORY-014B_analytics_chart_shell_handoff.md`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014B/`

Definition of Ready checked:
`CTX-DATA-VIEWS`, `CTX-FOUNDATION`, and accepted foundation handoffs for
`STORY-005`, `STORY-006`, and `STORY-007` were available and sufficient.

Context summaries read:
- `visual_overhaul_project/01_context/summaries/history_analytics_review_context.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`

Context summaries created/updated:
None.

Screens/states checked:
- Analytics Score Trends populated state.
- Analytics Test Comparison populated state.
- Analytics Study Activity populated state.
- Analytics chart no-data state.
- Analytics minimum-window Score Trends state.
- Weak Topics tab access and group-by controls were smoke checked to avoid
  regressing the out-of-scope tab.

Screenshot evidence:
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

Tests run:
- `python3 -m compileall -q study_test_tool/gui/analytics_view.py study_test_tool/gui/components/graph_widget.py study_test_tool/gui/styles.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/analytics_view.py study_test_tool/gui/components/graph_widget.py study_test_tool/gui/styles.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests/test_analytics_service.py`
- `PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --mode both --states analytics_populated analytics_test_comparison analytics_study_activity analytics_minimum_score_trends analytics_no_data --output visual_overhaul_project/01_context/screenshots/after/STORY-014B`
- GUI smoke: opened Analytics with seeded data, switched Score Trends, Test
  Comparison, Study Activity, and Weak Topics, then checked an empty database
  renders the chart no-data surface.
- Screenshot capture: `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --states analytics_populated analytics_test_comparison analytics_study_activity analytics_minimum_score_trends analytics_no_data --output visual_overhaul_project/01_context/screenshots/after/STORY-014B`

Tests not run and why:
Full pytest was not run. The story touched Analytics GUI styling, shared chart
roles, `GraphWidget`, and screenshot harness states, so the focused analytics
service tests plus GUI/screenshot validation cover the changed behavior surface.

Acceptance criteria notes:
- Chart tabs and filters now sit in a shared controls surface with clearer
  hierarchy.
- Chart figure and axes backgrounds use shared chart roles for light and dark
  mode.
- Chart text, grid, and primary series colors come from CTX-FOUNDATION chart
  roles.
- Chart-tab no-data states use a designed surface instead of a plain gray label.
- Existing service calls, chart series, axis labels, titles, test filter values,
  and Weak Topics grouping semantics were preserved.

Risks:
- Dense or unusually long test names may still need validation in
  `STORY-016_light_dark_and_min_size_validation.md`.
- Weak Topics visual polish remains intentionally deferred to `STORY-014C`.

Follow-up backlog items:
- Use `STORY-014C_analytics_weak_topics_and_no_data.md` for Weak Topics cards,
  grouping states, and non-chart no-data polish.
- Keep the single-day Study Activity bar in `STORY-016_light_dark_and_min_size_validation.md`
  or a later chart-readability follow-up. It is service-consistent, but the
  current evidence only proves one populated day and renders as a very wide bar.
- After another screen repeats the same local option-menu, segmented-control,
  page-header, or empty-state builders, consider extracting small shared GUI
  helpers. Do not start a broad design-system refactor from this story alone.

PM review decision:
Accepted on 2026-06-16. The review checked current Analytics and GraphWidget
code, the submitted light/dark Score Trends, Test Comparison, Study Activity,
chart no-data, and minimum-window screenshots, and focused analytics service
tests. The implementation keeps Analytics calculations, filter values, chart
titles, axis meanings, and Weak Topics grouping semantics unchanged while moving
matplotlib theme roles into `GraphWidget`.
