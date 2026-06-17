# STORY-011 Answer Rows And Practice Feedback Review

Story/Task:
`STORY-011_answer_rows_and_practice_feedback.md`

Status:
Done. Accepted by PM/reviewer on 2026-06-16.

Summary:
Accepted the submitted implementation. Full-row answer selection, checked
correct/incorrect treatment, practice feedback, essay feedback, and disabled
Check Answer behavior match the story scope. I found no required scoring,
session, or screenshot-evidence blocker.

Files reviewed:
- `study_test_tool/gui/components/question_widget.py`
- `study_test_tool/gui/test_taking.py`
- `visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `visual_overhaul_project/04_stories/STORY-011_answer_rows_and_practice_feedback.md`
- `visual_overhaul_project/06_handoffs/STORY-011_answer_rows_and_practice_feedback_handoff.md`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/`

Context checked:
- `visual_overhaul_project/01_context/summaries/test_taking_context.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/00_project/screenshot_evidence_policy.md`
- `visual_overhaul_project/00_project/status_transition_rules.md`

Acceptance notes:
- Multiple-choice answers are full-width selectable rows while preserving radio,
  label, and row-click selection paths.
- Checked practice responses still use the first checked answer for scoring and
  lock the answer widget after Check Answer.
- Correct, incorrect, neutral essay, disabled, selected, and muted row states
  are distinct in the sampled light and dark screenshots.
- Feedback auto-scroll is accepted as in scope because it makes the checked
  feedback visible immediately, and the checked-return evidence still shows the
  locked row treatment.
- Essay feedback remains a neutral comparison path and does not change essay
  scoring semantics.

Screenshot evidence reviewed:
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/light/light_test_taking_selected_answer.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/dark/dark_test_taking_selected_answer.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/light/light_test_taking_practice_incorrect_feedback.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/light/light_test_taking_practice_checked_return.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/dark/dark_test_taking_practice_checked_return.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/light/light_test_taking_essay_feedback.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-011/dark/dark_test_taking_essay_feedback.png`

Verification:
- `python3 -m compileall -q study_test_tool/gui/components/question_widget.py study_test_tool/gui/test_taking.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/components/question_widget.py study_test_tool/gui/test_taking.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests/test_practice_mode.py study_test_tool/tests/test_test_session.py study_test_tool/tests/test_scoring_service.py`
- `PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --mode both --states test_taking_unanswered test_taking_selected_answer test_taking_practice_correct_feedback test_taking_practice_incorrect_feedback test_taking_practice_checked_return test_taking_essay_input test_taking_essay_feedback test_taking_answered_flagged --output visual_overhaul_project/01_context/screenshots/after/STORY-011`
- `git diff --check`

Results:
- Syntax check passed.
- Black check passed.
- Focused pytest passed: 41 passed, 5 collection warnings.
- Screenshot validation passed: 16 screenshots.
- `git diff --check` passed.

Risks and follow-up:
- The implementation uses CustomTkinter internal child bindings to make the
  full drawn row clickable. This is acceptable for the MVP, but should be
  sampled again if CustomTkinter is upgraded.
- Later minimum-size validation should include long answer text and large
  question counts.
