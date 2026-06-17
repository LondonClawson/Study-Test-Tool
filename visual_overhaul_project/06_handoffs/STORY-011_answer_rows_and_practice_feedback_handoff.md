Story/Task:
`STORY-011_answer_rows_and_practice_feedback.md`

Status:
Submitted For Review. PM/reviewer acceptance is still required; this is not
marked Done.

Summary:
Updated the test-taking answer and practice feedback presentation while
preserving response capture, first-check locking, final scoring preference for
checked responses, and essay `None` scoring semantics. Multiple-choice answers
are now full-width selectable rows with row, label, and radio-button selection
paths. Checked practice answers show locked correct/incorrect row treatment,
practice feedback uses semantic status surfaces, essay input uses shared surface
tokens, and Check Answer uses a muted disabled treatment after a practice answer
is locked.

Files changed:
- `study_test_tool/gui/components/question_widget.py`
- `study_test_tool/gui/test_taking.py`
- `visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/04_stories/STORY-011_answer_rows_and_practice_feedback.md`
- `visual_overhaul_project/06_handoffs/STORY-011_answer_rows_and_practice_feedback_handoff.md`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/`

Definition of Ready checked:
Yes. `STORY-011` was Ready and unblocked, CTX-TEST-TAKING and CTX-FOUNDATION
were Ready, and `STORY-010_test_taking_shell.md` was accepted before this work
was claimed.

Context summaries read:
- `visual_overhaul_project/01_context/summaries/test_taking_context.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/06_handoffs/STORY-010_test_taking_shell_handoff.md`
- `visual_overhaul_project/06_handoffs/STORY-010_test_taking_shell_review.md`
- `visual_overhaul_project/06_handoffs/STORY-011_answer_rows_and_practice_feedback_readiness_review.md`

Context summaries created/updated:
None.

Screens/states checked:
- Multiple-choice unanswered rows.
- Multiple-choice selected row.
- Practice checked-correct feedback.
- Practice checked-incorrect feedback.
- Checked disabled state after navigating away and back.
- Essay input.
- Essay expected-answer feedback.
- Flagged-with-answer state.
- Light and dark mode for every captured state.

Screenshot evidence:
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/light/light_test_taking_unanswered.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/light/light_test_taking_selected_answer.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/light/light_test_taking_practice_correct_feedback.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/light/light_test_taking_practice_incorrect_feedback.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/light/light_test_taking_practice_checked_return.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/light/light_test_taking_essay_input.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/light/light_test_taking_essay_feedback.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/light/light_test_taking_answered_flagged.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/dark/dark_test_taking_unanswered.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/dark/dark_test_taking_selected_answer.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/dark/dark_test_taking_practice_correct_feedback.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/dark/dark_test_taking_practice_incorrect_feedback.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/dark/dark_test_taking_practice_checked_return.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/dark/dark_test_taking_essay_input.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/dark/dark_test_taking_essay_feedback.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/dark/dark_test_taking_answered_flagged.png`

Tests run:
- `python3 -m compileall -q study_test_tool/gui/components/question_widget.py study_test_tool/gui/test_taking.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/components/question_widget.py study_test_tool/gui/test_taking.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- Focused GUI smoke with seeded temporary data for row click, label click,
  radio click, Check Answer, locked answer immutability, navigating away/back,
  and essay feedback.
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests/test_practice_mode.py`
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests/test_test_session.py`
- `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --states test_taking_unanswered test_taking_selected_answer test_taking_practice_correct_feedback test_taking_practice_incorrect_feedback test_taking_practice_checked_return test_taking_essay_input test_taking_essay_feedback test_taking_answered_flagged --output visual_overhaul_project/01_context/screenshots/after/STORY-011`

Tests not run and why:
Full pytest was not run because this story changed GUI answer/feedback
presentation and the screenshot harness. Focused practice/session tests plus a
targeted GUI smoke covered the behavior-sensitive areas.

Acceptance criteria notes:
- Multiple-choice answers are selectable full-width rows and keep equivalent
  row, label, and radio-button answer selection.
- Checked practice answers use row-level correct/incorrect treatment and lock
  input controls after the first Check Answer action.
- Practice feedback is visually distinct from the question and uses semantic
  correct, incorrect, and neutral essay treatments.
- Feedback is scrolled into view after Check Answer so result details are
  visible without manual scrolling.
- Essay input keeps `QuestionWidget.get_answer()`, `set_answer(...)`, and
  `disable()` behavior and still scores as `None`.
- Check Answer gets a muted disabled treatment after the checked response is
  locked.

Risks:
- The row click binding uses CustomTkinter internal canvas/label children in
  addition to the public widget binding so the drawn full-row surface is
  clickable. This is common for CustomTkinter composites but should be sampled
  during PM review.
- The feedback auto-scroll is a small UX behavior change made inside the story
  scope so practice feedback is immediately visible after checking an answer.
- Very long answer options should be rechecked during the later minimum-size
  validation pass.

Follow-up backlog items:
- None required for this story. Later validation stories should include long
  answer text and very large question counts.
