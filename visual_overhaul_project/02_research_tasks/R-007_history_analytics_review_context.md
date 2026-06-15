# R-007: History, Analytics, And Review Context

## Status

Done. Completed after the R-002 assignment gate was satisfied.

## Role

Assign to Dev 1 Research Agent before history, analytics, or review
implementation stories.

## Goal

Create focused context for secondary data-view screens: history, analytics, and
review. These screens should share polished data-list, chart, card, empty-state,
and action-hierarchy patterns without losing scanability.

## Output

Write the summary to:

```text
visual_overhaul_project/01_context/summaries/history_analytics_review_context.md
```

## Required Inputs

- `visual_overhaul_project/01_context/summaries/gui_architecture_summary.md`.
- `visual_overhaul_project/01_context/summaries/current_visual_state_seed.md`.
- `VISUAL_OVERHAUL_PLAN.md`.

## Source Files

- `study_test_tool/gui/history_view.py`.
- `study_test_tool/gui/analytics_view.py`.
- `study_test_tool/gui/review_view.py`.
- `study_test_tool/gui/components/graph_widget.py`.
- Related service tests only as needed: analytics, review, scoring.

## Do Not Change

- Do not change application code.
- Do not redesign history, analytics, or review screens.
- Do not change analytics calculations, history persistence, review question
  selection, scoring, or chart data flow.

## Research Steps

1. Map each screen structure, filters, list/card rows, actions, empty states, and
   loading states.
2. Document chart types and current theme colors.
3. Identify common data-view patterns that could be shared visually.
4. Identify screen-specific behavior constraints.
5. Note where each screen needs screenshots or seeded data to verify polish.

## Summary Must Include

- Per-screen workflow and state map.
- Common data-view visual patterns.
- Chart theme findings.
- Empty/loading/no-data findings.
- Behavior constraints.
- Recommended story split.
- Dev 2 Quick Start notes.

## Done Criteria

- `history_analytics_review_context.md` exists.
- It gives enough detail for history, analytics, and review stories.
- Context index status for CTX-DATA-VIEWS is updated.
- `00_project/status_board.md` is updated.
- The handoff lists source files inspected and states not inspected.
- The summary passes `00_project/definition_of_ready.md`.
