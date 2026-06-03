# STORY-014: History And Analytics Polish

## Status

Blocked.

## Readiness

- Blocked by: CTX-DATA-VIEWS, CTX-FOUNDATION.
- Unblocked by: `R-007_history_analytics_review_context.md` and
  `STORY-003_visual_foundation_spec.md`.

## Sprint

Target sprint: Sprint 3.

## User Story

As a learner, I want history and analytics to feel like polished data views so
that I can quickly understand past attempts and weak topics.

## Goal

Polish history rows, filters, loading/empty states, analytics charts, tab/filter
layout, and weak-topic cards.

## PM Refinement Note

Do not assign this as a single junior implementation story. After
`R-007_history_analytics_review_context.md` is complete, split this into narrow
stories based on the research summary. Expected splits are history list/filter
polish, analytics chart/theme polish, and analytics weak-topic/no-data states.

## Required Context

- `visual_overhaul_project/01_context/summaries/history_analytics_review_context.md`.
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.
- Research task if context is missing:
  `visual_overhaul_project/02_research_tasks/R-007_history_analytics_review_context.md`.

## Scope

In:

- History table/list row styling.
- History filter presentation.
- Loading and empty states.
- Analytics chart theme alignment.
- Analytics tab/filter layout.
- Weak-topic card styling.

Out:

- Analytics calculations.
- History persistence.
- New chart types unless approved.

## Likely Files

- `study_test_tool/gui/history_view.py`.
- `study_test_tool/gui/analytics_view.py`.
- `study_test_tool/gui/components/graph_widget.py`.

## Implementation Steps

1. Do not start as a junior implementation assignment until this story is split.
2. Read CTX-DATA-VIEWS, CTX-FOUNDATION, and the research-recommended split.
3. Create or assign one narrow child story for history rows/filters, analytics
   charts, or weak-topic/no-data states.
4. Implement only the selected child story scope.
5. Verify the exact populated, empty/no-data, loading, light, dark, and
   navigation states named by the child story.
6. Document remaining child stories or post-MVP follow-ups.

## Acceptance Criteria

- History rows are aligned, readable, and visibly clickable.
- Filters remain easy to find and use.
- Charts match the visual foundation in light and dark mode.
- Weak-topic cards are easy to scan.
- Empty/no-data/loading states are intentional.
- The story has been split before junior implementation assignment, or the PM
  handoff explains why one senior-owned story is being used instead.

## Verification

- Run analytics tests if chart data flow is touched:
  `pytest --rootdir=. study_test_tool/tests/test_analytics_service.py`.
- Smoke check history row opens results.
- Visual check populated and no-data states if possible.

## Dev 2 Assignment Notes

- Treat this file as a PM refinement placeholder until split stories exist.
- Do not change analytics calculations, history persistence, chart data flow, or
  result loading behavior.
- If CTX-DATA-VIEWS is missing or does not recommend splits, stop and assign or
  revise R-007.

## Handoff Requirements

- List history and analytics states checked.
- List chart theme decisions added or updated.
