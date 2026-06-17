# STORY-014A: History List And Filters

## Status

Done.

## Readiness

- Blocked by: None.
- Unblocked by: CTX-DATA-VIEWS, CTX-FOUNDATION, and accepted foundation
  handoffs.

## Sprint

Target sprint: Sprint 3.

## User Story

As a learner, I want history rows and filters to be easy to scan so that I can
quickly find a past attempt and reopen its results.

## Goal

Polish the History screen filter row, table header, attempt rows, clickable
affordance, loading state, and empty state without changing persistence or
result navigation behavior.

## Required Context

- `visual_overhaul_project/01_context/summaries/history_analytics_review_context.md`.
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.
- Completed handoffs for `STORY-005`, `STORY-006`, and `STORY-007`.

## Scope

In:

- History filter row layout and spacing.
- History table/header visual hierarchy.
- Attempt row styling, metadata alignment, hover/click affordance, and
  readability.
- History loading and empty states.

Out:

- History persistence.
- Attempt query semantics.
- Result-loading behavior.
- Analytics and review screen polish.
- New filters or new history data fields.

## Likely Files

- `study_test_tool/gui/history_view.py`.
- `study_test_tool/gui/styles.py` only if existing shared helpers need a
  narrow reuse.

## Implementation Steps

1. Read CTX-DATA-VIEWS, CTX-FOUNDATION, and the completed foundation handoffs.
2. Inspect only the History screen regions named by CTX-DATA-VIEWS unless live
   code contradicts the summary.
3. Apply the shared page header, row/card, button, and empty/loading guidance to
   the History screen only.
4. Preserve all filter values, background loading flow, row click callbacks, and
   result navigation behavior.
5. Verify populated history, empty history, filtered history, loading state if
   practical, light mode, dark mode, and minimum-window behavior where layout
   changed.
6. Update the story handoff with changed files, states checked, screenshot
   evidence or capture blockers, tests run, risks, and follow-ups.

## Acceptance Criteria

- History filters remain easy to find and use.
- Table/header labels align with row content at normal and minimum window
  widths.
- Attempt rows are visibly clickable without adding new behavior.
- Loading and empty states use the visual foundation instead of a plain gray
  label.
- Clicking a populated history row still opens the same result detail flow.

## Verification

- Screenshot evidence is required under
  `visual_overhaul_project/01_context/screenshots/after/STORY-014A/`.
- Capture or document a blocker for light and dark
  `history_populated` and `history_empty_state`.
- Capture or manually document filtered history, loading state, and minimum
  window behavior if changed.
- Smoke check that a populated history row opens results.
- Run focused tests only if behavior-bearing code changes; otherwise document
  that pytest was skipped because the change is visual-only GUI work.

## Dev 2 Assignment Notes

- Do not repeat broad GUI exploration unless required context is missing, stale,
  or contradicted by live code.
- Do not change history persistence, filters, database calls, date formatting
  semantics, or result navigation.
- If the harness cannot capture a required history state, document the manual
  check or exact blocker in the handoff.

## Handoff Requirements

- Changed files.
- History states checked.
- Screenshot paths or capture blocker.
- Confirmation that row-to-results navigation stayed unchanged.
- Tests run or reason skipped.
- Follow-up backlog items.
