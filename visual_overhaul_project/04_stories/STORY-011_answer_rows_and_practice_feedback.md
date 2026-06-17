# STORY-011: Answer Rows And Practice Feedback

## Status

Done.

## Readiness

- Blocked by: None.
- Unblocked by: CTX-TEST-TAKING, CTX-FOUNDATION, and accepted completion of
  `STORY-010_test_taking_shell.md`.

CTX-TEST-TAKING and CTX-FOUNDATION are Ready. `STORY-010` is accepted, and this
story was accepted by PM/reviewer on 2026-06-16 after implementation handoff,
focused tests, and screenshot evidence review.

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

- Screenshot evidence is required under
  `visual_overhaul_project/01_context/screenshots/after/STORY-011/`.
- Capture or document a blocker for light and dark states covering
  multiple-choice unselected, selected, checked-correct, checked-incorrect,
  checked-disabled after navigating away/back, essay input, essay expected
  answer feedback, unanswered, and flagged-with-answer states where practical.
- Smoke check multiple-choice selection by radio, label, and any new row click
  target; essay input; Check Answer; disabled checked state; and navigating
  away/back.
- Run `pytest --rootdir=. study_test_tool/tests/test_practice_mode.py`.
- Run `pytest --rootdir=. study_test_tool/tests/test_test_session.py` if
  response saving, navigation, progress-click, flag, or session state paths are
  touched.

## Dev 2 Assignment Notes

- Do not change scoring, response persistence, or checked-response locking.
- Do not change shell layout beyond feedback placement required by this story.
- If CTX-TEST-TAKING does not cover the needed answer states, stop and update
  R-004 output first.

## Handoff Requirements

- List answer states checked.
- List screenshot evidence paths or exact capture blockers.
- List any behavior tests run.
- Confirm first-check locking and final scoring preference for checked
  responses stayed unchanged.
- Call out any remaining CustomTkinter limitations.
