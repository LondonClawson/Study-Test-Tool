# STORY-014: History And Analytics Polish

## Status

Done.

## Readiness

- Blocked by: None.
- Superseded by: child stories below.

PM split completed on 2026-06-16. Do not assign this parent story for
implementation. Use the child stories instead:

- `STORY-014A_history_list_and_filters.md`.
- `STORY-014B_analytics_chart_shell.md`.
- `STORY-014C_analytics_weak_topics_and_no_data.md`.

## Sprint

Target sprint: Sprint 3.

## User Story

As a learner, I want history and analytics to feel like polished data views so
that I can quickly understand past attempts and weak topics.

## Goal

Polish history rows, filters, loading/empty states, analytics charts, tab/filter
layout, and weak-topic cards.

## PM Refinement Note

Do not assign this as a single junior implementation story. This parent is now
a completed PM refinement placeholder. Use the child story files for actual
implementation assignment.

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

1. Do not start as a junior implementation assignment; this parent has been
   split.
2. Read CTX-DATA-VIEWS, CTX-FOUNDATION, and the research-recommended split.
3. Assign one narrow child story for history rows/filters, analytics charts, or
   weak-topic/no-data states.
4. Implement only the selected child story scope.
5. Verify the exact populated, empty/no-data, loading, light, dark, and
   navigation states named by the child story.
6. Document remaining child stories or post-MVP follow-ups.

## Acceptance Criteria

- The parent story has been split before junior implementation assignment.
- Each child story has narrow scope, named context, behavior constraints,
  verification expectations, and screenshot evidence requirements.

## Verification

- PM split handoff documents the child stories and readiness notes.
- Child stories carry their own runtime screenshot and smoke-test requirements.

## Dev 2 Assignment Notes

- Treat this file as a PM refinement placeholder until split stories exist.
- Do not change analytics calculations, history persistence, chart data flow, or
  result loading behavior.
- If CTX-DATA-VIEWS becomes stale or contradicted by live code, stop and assign
  a context refresh before implementation.

## Handoff Requirements

- Child story handoffs must list the history or analytics states checked.
- Child story handoffs must list screenshot evidence or capture blockers.
