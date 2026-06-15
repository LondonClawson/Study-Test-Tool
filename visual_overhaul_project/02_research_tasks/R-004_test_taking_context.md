# R-004: Test-Taking Context

## Status

Done. Claimed and completed by Codex on 2026-06-03 after R-002 was marked
Done; accepted by reviewer on 2026-06-03.

## Role

Assign to Dev 1 Research Agent before test-taking implementation stories.

## Goal

Create focused context for test-taking visual work, especially the top bar,
question panel, selectable answer rows, progress indicators, bottom navigation,
timer, flag state, and practice feedback.

## Output

Write the summary to:

```text
visual_overhaul_project/01_context/summaries/test_taking_context.md
```

## Required Inputs

- `visual_overhaul_project/01_context/summaries/gui_architecture_summary.md`.
- `visual_overhaul_project/01_context/summaries/current_visual_state_seed.md`.
- `VISUAL_OVERHAUL_PLAN.md`.

## Source Files

- `study_test_tool/gui/test_taking.py`.
- `study_test_tool/gui/components/question_widget.py`.
- `study_test_tool/gui/components/progress_bar.py`.
- `study_test_tool/gui/components/timer_widget.py`.
- `study_test_tool/services/test_session.py`.
- `study_test_tool/tests/test_practice_mode.py`.
- `study_test_tool/tests/test_test_session.py`.

## Do Not Change

- Do not change application code.
- Do not redesign the test-taking screen.
- Do not change response saving, practice check locking, scoring, flagging,
  timing, review-session, or mix-test behavior.

## Research Steps

1. Map test-taking states: normal test, practice mode, review session, mix test,
   first question, middle question, last question, flagged, answered, unchecked,
   checked practice response, essay response.
2. Identify which UI elements are rebuilt per question.
3. Document current response saving and practice check locking behavior.
4. Inventory colors used for answered, unanswered, current, flagged, correct,
   incorrect, warning, and finish.
5. Identify layout constraints at minimum window size.
6. Note which changes could affect behavior and require tests.

## Summary Must Include

- Test-taking workflow and state map.
- Current widget structure.
- Behavior constraints.
- Visual issues and opportunities.
- Recommended split between screen work and shared component work.
- Verification requirements.
- Dev 2 Quick Start notes.

## Done Criteria

- `test_taking_context.md` exists.
- It gives enough detail for answer-row and practice-feedback stories.
- Context index status for CTX-TEST-TAKING is updated.
- `00_project/status_board.md` is updated.
- The handoff lists source files inspected and states not inspected.
- The summary passes `00_project/definition_of_ready.md`.
