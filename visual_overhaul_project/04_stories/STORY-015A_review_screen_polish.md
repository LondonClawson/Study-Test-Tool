# STORY-015A: Review Screen Polish

## Status

Blocked.

## Readiness

- Blocked by: `STORY-005_button_hierarchy.md`,
  `STORY-006_card_and_list_patterns.md`, and
  `STORY-007_page_header_pattern.md`.
- Unblocked by: completion of the button, card/list, and header pilots.

## Sprint

Target sprint: Sprint 3.

## User Story

As a learner, I want the missed-question review screen to clearly communicate
scope, selected questions, and the start action so I can confidently launch a
focused practice session.

## Required Context

- `visual_overhaul_project/01_context/summaries/history_analytics_review_context.md`.
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.
- Completed handoffs for `STORY-005`, `STORY-006`, and `STORY-007`.

## Scope

In:

- Review scope selector hierarchy.
- Selected-count and action bar hierarchy.
- Missed-question card/list polish.
- Review empty states for no active tests, no tests selected, and no missed
  questions.

Out:

- Review service behavior.
- Selection semantics.
- Practice-mode launch behavior.
- Test-taking screen polish.

## Likely Files

- `study_test_tool/gui/review_view.py`.

## Implementation Steps

1. Read CTX-DATA-VIEWS, CTX-FOUNDATION, and the completed foundation handoffs.
2. Polish only the review screen scope selector, action bar, question cards, and
   empty states.
3. Preserve all checkbox state, selected-count behavior, and Start Review
   fallback behavior.
4. Verify review with active tests, no active tests, no missed questions,
   grouped tests, selected tests, no selected questions, light mode, and dark
   mode.

## Acceptance Criteria

- Scope, selection count, and Start Review hierarchy are clear.
- Missed-question cards are easier to scan without changing data or selection.
- Empty states clearly distinguish no active tests, no selected tests, and no
  missed questions.
- Existing review launch behavior is unchanged.

## Verification

- Smoke check review session start paths.
- Run review service tests if behavior-bearing code changes.
- Visual check light and dark mode.

## Handoff Requirements

- List review states checked.
- List changed visual roles.
- Confirm selection and launch behavior stayed unchanged.
