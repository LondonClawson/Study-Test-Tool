Story/Task:
`STORY-014C_analytics_weak_topics_and_no_data.md`

Status:
Submitted For Review. PM/reviewer acceptance is still required.

Summary:
Polished the Analytics Weak Topics tab without changing analytics service
behavior. Weak, moderate, and strong topics now render as semantic cards with a
status rail, compact status pill, progress bar, and aligned metadata. Weak
Topics no-data and no-category states now use designed empty-state surfaces.
The screenshot harness now supports repeatable Weak Topics captures for Test,
Group, Category, minimum-window, no-category, and no-data states.

Files changed:
- `study_test_tool/gui/analytics_view.py`
- `visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/04_stories/STORY-014C_analytics_weak_topics_and_no_data.md`
- `visual_overhaul_project/06_handoffs/STORY-014C_analytics_weak_topics_and_no_data_handoff.md`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014C/`

Definition of Ready checked:
`CTX-DATA-VIEWS`, `CTX-FOUNDATION`, and accepted foundation handoffs for
`STORY-005`, `STORY-006`, and `STORY-007` were available and sufficient.
`STORY-014B` chart-shell review was also checked so this work stayed scoped to
Weak Topics and non-chart empty states.

Context summaries read:
- `visual_overhaul_project/01_context/summaries/history_analytics_review_context.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/06_handoffs/STORY-005_button_hierarchy_handoff.md`
- `visual_overhaul_project/06_handoffs/STORY-006_card_and_list_patterns_handoff.md`
- `visual_overhaul_project/06_handoffs/STORY-007_page_header_pattern_handoff.md`
- `visual_overhaul_project/06_handoffs/STORY-014B_analytics_chart_shell_handoff.md`
- `visual_overhaul_project/06_handoffs/STORY-014B_analytics_chart_shell_review.md`

Context summaries created/updated:
None.

Screens/states checked:
- Analytics Weak Topics grouped by Test.
- Analytics Weak Topics grouped by Group.
- Analytics Weak Topics grouped by Category.
- Analytics Weak Topics minimum-window Test grouping.
- Analytics Weak Topics Category grouping with no category tags.
- Analytics Weak Topics no-data state.
- Light and dark mode for every captured state.

Screenshot evidence:
- `visual_overhaul_project/01_context/screenshots/after/STORY-014C/light/light_analytics_weak_topics_test.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014C/light/light_analytics_weak_topics_group.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014C/light/light_analytics_weak_topics_category.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014C/light/light_analytics_weak_topics_minimum.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014C/light/light_analytics_weak_topics_no_category.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014C/light/light_analytics_weak_topics_no_data.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014C/dark/dark_analytics_weak_topics_test.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014C/dark/dark_analytics_weak_topics_group.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014C/dark/dark_analytics_weak_topics_category.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014C/dark/dark_analytics_weak_topics_minimum.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014C/dark/dark_analytics_weak_topics_no_category.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-014C/dark/dark_analytics_weak_topics_no_data.png`

Tests run:
- `python3 -m compileall -q study_test_tool/gui/analytics_view.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/analytics_view.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests/test_analytics_service.py`
- `PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --mode both --states analytics_weak_topics_test analytics_weak_topics_group analytics_weak_topics_category analytics_weak_topics_minimum analytics_weak_topics_no_category analytics_weak_topics_no_data --output visual_overhaul_project/01_context/screenshots/after/STORY-014C`
- GUI smoke: opened Analytics with seeded data, switched Weak Topics through
  Test, Group, and Category; confirmed category no-tag and empty-database
  states render the designed Weak Topics empty surface.
- Screenshot capture: `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --states analytics_weak_topics_test analytics_weak_topics_group analytics_weak_topics_category analytics_weak_topics_minimum analytics_weak_topics_no_category analytics_weak_topics_no_data --output visual_overhaul_project/01_context/screenshots/after/STORY-014C`
- `git diff --check`

Tests not run and why:
Full pytest was not run. The story touched Analytics GUI styling and screenshot
harness states, while the focused analytics service tests plus GUI smoke and
screenshot validation cover the changed behavior surface.

Acceptance criteria notes:
- Weak, moderate, and strong topic statuses use semantic status colors and are
  visually distinct in light and dark mode.
- Grouping controls and service calls are preserved. The UI still maps
  `Test`, `Group`, and `Category` to the existing `test`, `group`, and
  `category` service grouping values.
- Weak-topic metadata and progress values remain based on the existing service
  response; no thresholds, database queries, or classification behavior were
  changed.
- No-data and no-category states are now designed Weak Topics empty surfaces
  with distinct copy.
- The harness adds a `no_category` seeded source by clearing categories in a
  temporary screenshot database only. App runtime behavior is unchanged.

Risks:
- Long topic names and deeper Weak Topics lists still need validation in
  `STORY-016_light_dark_and_min_size_validation.md`.
- Analytics and Review now both have local segmented-control and empty-state
  helper patterns. Do not extract yet; revisit after validation or another
  screen repeats the pattern.

Follow-up backlog items:
- Use `STORY-016_light_dark_and_min_size_validation.md` to validate long topic
  names, dense Weak Topics lists, and minimum-size wrapping across data views.
