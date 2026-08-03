# STORY-020: Analytics Loading Scalability

## Status

Done. Accepted by PM authorization.

## Goal

Keep Analytics responsive for large attempt histories by loading tab data away
from the Tk event loop and bounding Score Trends data before chart rendering.

## Required Context

- `CTX-DATA-VIEWS`
- `CTX-PERFORMANCE-SCALE`

## In Scope

- Background retrieval for all Analytics tabs with stale-result protection.
- A visible loading state while Analytics data is being prepared.
- Bounded, deterministic Score Trends data suitable for a readable chart.
- Focused database/service and GUI-state tests.
- Light/dark Analytics screenshot validation for populated and no-data states.

## Out Of Scope

- Changing Analytics calculation semantics, mode filters, weak-topic grouping,
  score classifications, or the 30-day study-activity window.
- Schema or migration changes unless measurement during this story demonstrates
  that a specific index is necessary.
- Mix selection, History pagination, question/options bulk loading, and
  historical Results loading.

## Acceptance Criteria

- Tab and test/grouping-filter changes do not perform database retrieval on
  the Tk event loop; bounded Matplotlib drawing occurs only after the current
  worker response is applied on that event loop.
- A stale background response cannot replace the currently selected tab,
  test, or grouping.
- Score Trends renders no more than a documented bounded number of points,
  while retaining the chronological span and preserving an empty state when no
  test-mode attempts exist.
- Test Comparison, Study Activity, and Weak Topics preserve their current
  calculations, labels, grouping behavior, and no-data messages.
- Existing chart and weak-topic populated/no-data states work in light and
  dark mode, with screenshot evidence recorded in the handoff.

## Verification

- Run focused analytics service/database tests and the full pytest suite if
  shared data-access code changes.
- Capture light/dark `analytics_populated`, `analytics_test_comparison`,
  `analytics_study_activity`, `analytics_no_data`, and a score-trends state
  exceeding the new point cap when the harness supports it.
- Record any unavailable scale fixture or benchmark as a handoff limitation.
