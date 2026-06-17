# STORY-014C: Analytics Weak Topics And No-Data States

## Status

Done.

## Readiness

- Blocked by: None.
- Unblocked by: CTX-DATA-VIEWS, CTX-FOUNDATION, and accepted foundation
  handoffs.

## Sprint

Target sprint: Sprint 3.

## User Story

As a learner, I want weak-topic analytics to clearly distinguish weak,
moderate, strong, and missing-data states so that I know what to study next.

## Goal

Polish the Analytics Weak Topics tab, grouping controls, status cards, and
weak-topic empty/no-category states without changing topic classification.

## Required Context

- `visual_overhaul_project/01_context/summaries/history_analytics_review_context.md`.
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.
- Completed handoffs for `STORY-005`, `STORY-006`, and `STORY-007`.

## Scope

In:

- Weak Topics tab layout and grouping-control hierarchy.
- Weak-topic card styling, status color treatment, progress bars, metadata, and
  scroll spacing.
- No weak topics, no analytics data, and no category-tag states for Weak Topics.

Out:

- Weak-topic classification thresholds.
- Analytics service queries and grouping semantics.
- Chart shell/theme polish for Score Trends, Test Comparison, or Study Activity
  except preserving navigation between tabs.
- History and review screen polish.

## Likely Files

- `study_test_tool/gui/analytics_view.py`.
- `study_test_tool/gui/styles.py` only if existing shared helpers need a
  narrow reuse.

## Implementation Steps

1. Read CTX-DATA-VIEWS, CTX-FOUNDATION, and the completed foundation handoffs.
2. Inspect only Analytics Weak Topics regions named by CTX-DATA-VIEWS unless
   live code contradicts the summary.
3. Apply shared card/list, status, progress, and empty-state guidance to Weak
   Topics only.
4. Preserve group-by values, service calls, weak/moderate/strong thresholds,
   category fallback behavior, and no-category semantics.
5. Verify Weak Topics grouped by Test, Group, and Category; weak, moderate, and
   strong cards; no-data/no-category states; light mode; dark mode; and
   minimum-window behavior where layout changed.
6. Update the story handoff with changed files, states checked, screenshot
   evidence or capture blockers, tests run, risks, and follow-ups.

## Acceptance Criteria

- Weak, moderate, and strong cards are visually distinct and readable in light
  and dark mode.
- Grouping controls are easy to find without overpowering the topic cards.
- Weak-topic metadata and progress bars are aligned and scannable.
- No-data and no-category states tell the user what is missing without changing
  service behavior.
- Existing weak-topic grouping and classification behavior is unchanged.

## Verification

- Screenshot evidence is required under
  `visual_overhaul_project/01_context/screenshots/after/STORY-014C/`.
- Capture or document a blocker for light and dark Weak Topics populated,
  grouped by Test, Group, and Category.
- Capture or document weak, moderate, strong, no-data, and no-category states.
- Run `pytest --rootdir=. study_test_tool/tests/test_analytics_service.py` if
  grouping, thresholds, service calls, or tab behavior changes.
- If only visual GUI code changes, document why analytics service tests were
  skipped and smoke check Weak Topics in the app.

## Dev 2 Assignment Notes

- Do not repeat broad GUI exploration unless required context is missing, stale,
  or contradicted by live code.
- Do not change weak-topic thresholds, grouping semantics, category fallback
  behavior, analytics service APIs, or database queries.
- If seeded data cannot produce all three topic statuses, document the missing
  state and exact capture blocker in the handoff.

## Handoff Requirements

- Changed files.
- Weak Topics states checked.
- Screenshot paths or capture blocker.
- Confirmation that grouping and classification behavior stayed unchanged.
- Tests run or reason skipped.
- Follow-up backlog items.
