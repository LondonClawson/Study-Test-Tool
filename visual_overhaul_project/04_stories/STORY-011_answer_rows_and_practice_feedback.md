# STORY-011: Answer Rows And Practice Feedback

## Status

Blocked.

## Readiness

- Blocked by: CTX-TEST-TAKING, CTX-FOUNDATION.
- Unblocked by: `R-004_test_taking_context.md` and
  `STORY-003_visual_foundation_spec.md`.

## Sprint

Target sprint: Sprint 2.

## User Story

As a test taker, I want answer choices and practice feedback to be easy to read
and clearly interactive so that I can focus on answering and learning.

## Goal

Upgrade multiple-choice answer presentation and practice feedback while
preserving response capture and first-check locking behavior.

## Required Context

- `visual_overhaul_project/01_context/summaries/test_taking_context.md`.
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.
- `study_test_tool/tests/test_practice_mode.py`.

## Scope

In:

- Multiple-choice selectable answer rows.
- Essay answer panel styling if needed for consistency.
- Practice feedback card/panel.
- Correct/incorrect/expected-answer status treatment.
- Disabled checked state after practice feedback.

Out:

- Scoring behavior.
- Practice mode locking semantics.
- Question randomization.

## Likely Files

- `study_test_tool/gui/components/question_widget.py`.
- `study_test_tool/gui/test_taking.py`.

## Implementation Steps

1. Read CTX-TEST-TAKING, CTX-FOUNDATION, and practice-mode constraints.
2. Inspect only answer row, essay answer, selection, and practice feedback
   regions named by CTX-TEST-TAKING.
3. Apply selected, unselected, checked, correct, incorrect, warning, and essay
   visual states.
4. Preserve first-check locking and final scoring behavior.
5. Verify multiple-choice, essay, unanswered, checked-correct, checked-incorrect,
   disabled, and flagged states.
6. Run practice/session tests if any behavior-bearing path is touched.

## Acceptance Criteria

- Multiple-choice answers feel like full selectable rows, not loose radio labels.
- Label click behavior remains intact or is replaced by equivalent row click
  behavior.
- Practice feedback is clear, calm, and visually distinct from the question.
- First checked response remains locked and final scoring still prefers checked
  responses.
- Essay responses remain scorable as `None` where applicable.

## Verification

- Run `pytest --rootdir=. study_test_tool/tests/test_practice_mode.py`.
- Smoke check multiple-choice selection, essay input, check answer, disabled
  state, and navigating away/back.
- Visual check in light and dark mode.

## Dev 2 Assignment Notes

- Do not change scoring, response persistence, or checked-response locking.
- Do not change shell layout beyond feedback placement required by this story.
- If CTX-TEST-TAKING does not cover the needed answer states, stop and update
  R-004 output first.

## Handoff Requirements

- List answer states checked.
- List any behavior tests run.
- Call out any remaining CustomTkinter limitations.
