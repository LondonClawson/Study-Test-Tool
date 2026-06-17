# STORY-010: Test-Taking Shell

## Status

Done.

## Readiness

- Blocked by: None.
- Unblocked by: accepted completion of the button hierarchy pilot.

CTX-TEST-TAKING, CTX-FOUNDATION, and `STORY-004_shared_style_entrypoints.md` are
Ready or Done. `STORY-005` has accepted visual evidence for the button role
model in a full screen. This story is Ready for Dev 2 assignment.

## Sprint

Target sprint: Sprint 2.

## User Story

As a test taker, I want the test-taking screen to feel focused and readable so
that progress, timing, flagging, and navigation support the question instead of
competing with it.

## Goal

Polish the test-taking screen shell: top bar, question panel container, bottom
navigation, progress indicator placement, timer display, and flag state.

## Required Context

- `visual_overhaul_project/01_context/summaries/test_taking_context.md`.
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.
- Research task if context is missing:
  `visual_overhaul_project/02_research_tasks/R-004_test_taking_context.md`.

## Scope

In:

- Test title, progress label, timer, and flag layout.
- Question area framing and scroll behavior.
- Previous, next, check answer, and finish button hierarchy.
- Progress bar visual placement and role colors.

Out:

- Answer row redesign.
- Practice feedback redesign.
- Test session behavior changes.

## Likely Files

- `study_test_tool/gui/test_taking.py`.
- `study_test_tool/gui/components/progress_bar.py`.
- `study_test_tool/gui/components/timer_widget.py`.

## Implementation Steps

1. Read CTX-TEST-TAKING, CTX-FOUNDATION, and the Dev 2 Quick Start notes.
2. Inspect only the shell, top bar, progress, timer, flag, and navigation areas
   named by CTX-TEST-TAKING.
3. Polish the shell without changing answer row or practice feedback internals.
4. Preserve previous, next, check answer, flag, finish, timer, and progress
   behavior.
5. Verify normal, practice, review, mix-test, flagged, first, middle, and last
   question states where practical.
6. Run session tests if response flow or session state is touched.

## Acceptance Criteria

- Question content remains the dominant visual focus.
- Timer, progress, and flag state are visible without distracting from the
  question.
- Finish is styled as an end-of-flow primary/confirming action unless foundation
  decisions explicitly classify it otherwise.
- Previous/Next/Check Answer hierarchy matches the approved button roles.
- Normal, practice, review, and mix-test entry paths still work.

## Verification

- Screenshot evidence is required under
  `visual_overhaul_project/01_context/screenshots/after/STORY-010/`.
- Capture or document a blocker for light and dark states covering normal,
  practice, review, mix-test, flagged, first-question, middle-question, and
  last-question shell states where practical.
- Visual check in normal and practice mode.
- Smoke check previous/next/progress/flag/finish interactions.
- Run `pytest --rootdir=. study_test_tool/tests/test_test_session.py` if session
  behavior or response flow is touched.

## Dev 2 Assignment Notes

- Do not change `TestSession` behavior, scoring, timing, flagging, or navigation
  semantics.
- Do not redesign answer rows or practice feedback in this story.
- If CTX-TEST-TAKING is missing or stale, stop and assign R-004.

## Handoff Requirements

- List test-taking states checked.
- List any follow-up work reserved for answer rows or practice feedback.
