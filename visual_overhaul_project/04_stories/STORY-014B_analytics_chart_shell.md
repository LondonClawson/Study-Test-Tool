# STORY-014B: Analytics Chart Shell

## Status

Ready.

## Readiness

- Blocked by: None.
- Unblocked by: CTX-DATA-VIEWS, CTX-FOUNDATION, and accepted foundation
  handoffs.

## Sprint

Target sprint: Sprint 3.

## User Story

As a learner, I want analytics charts and filters to feel integrated with the
app so that score trends and study activity are easier to interpret.

## Goal

Polish the Analytics screen chart shell, tab/filter hierarchy, chart surface,
and matplotlib theme alignment for the chart tabs without changing analytics
calculations.

## Required Context

- `visual_overhaul_project/01_context/summaries/history_analytics_review_context.md`.
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.
- Completed handoffs for `STORY-005`, `STORY-006`, and `STORY-007`.

## Scope

In:

- Analytics page header and top spacing only where needed for chart shell
  consistency.
- Analytics tab strip and test filter hierarchy.
- Chart card/surface layout for Score Trends, Test Comparison, and Study
  Activity.
- `GraphWidget` light/dark theme alignment with CTX-FOUNDATION chart roles.
- Chart-tab no-data surface.

Out:

- Analytics calculations.
- New chart types.
- Weak Topics card/list polish, except preserving its existing tab access.
- History and review screen polish.
- Analytics service APIs or database queries.

## Likely Files

- `study_test_tool/gui/analytics_view.py`.
- `study_test_tool/gui/components/graph_widget.py`.
- `study_test_tool/gui/styles.py` only if existing shared helpers need a
  narrow reuse.

## Implementation Steps

1. Read CTX-DATA-VIEWS, CTX-FOUNDATION, and the completed foundation handoffs.
2. Inspect only Analytics chart-tab and `GraphWidget` regions named by
   CTX-DATA-VIEWS unless live code contradicts the summary.
3. Apply the shared page header, surface, control, and chart-theme guidance to
   chart tabs only.
4. Preserve tab names, test filter values, service calls, chart data series,
   axis labels, and no-data semantics.
5. Verify Score Trends, Test Comparison, Study Activity, chart no-data, light
   mode, dark mode, and minimum-window behavior where layout changed.
6. Update the story handoff with changed files, states checked, screenshot
   evidence or capture blockers, tests run, risks, and follow-ups.

## Acceptance Criteria

- Chart tabs and filters have a clear hierarchy and do not compete with chart
  content.
- Chart figure and axes backgrounds match the active app theme in light and
  dark mode.
- Chart text, grid, and primary series colors follow CTX-FOUNDATION chart roles
  with sufficient contrast.
- Chart no-data state uses the visual foundation instead of a plain gray label.
- Existing analytics service calls and displayed chart data are unchanged.

## Verification

- Screenshot evidence is required under
  `visual_overhaul_project/01_context/screenshots/after/STORY-014B/`.
- Capture or document a blocker for light and dark `analytics_populated` and
  `analytics_no_data`.
- Manually capture or document Score Trends, Test Comparison, and Study
  Activity if the harness only lands on one tab.
- Run `pytest --rootdir=. study_test_tool/tests/test_analytics_service.py` if
  chart data flow, filters, or tab behavior changes.
- If only visual GUI code changes, document why analytics service tests were
  skipped and smoke check the chart tabs in the app.

## Dev 2 Assignment Notes

- Do not repeat broad GUI exploration unless required context is missing, stale,
  or contradicted by live code.
- Do not change analytics calculations, query defaults, grouping semantics, data
  lookback, axis meaning, or chart titles unless separately approved.
- Keep Weak Topics polish for `STORY-014C`; only avoid regressing access to that
  tab here.

## Handoff Requirements

- Changed files.
- Analytics chart states checked.
- Screenshot paths or capture blocker.
- Confirmation that chart data flow and filters stayed unchanged.
- Tests run or reason skipped.
- Follow-up backlog items.
