Story/Task:
`STORY-010_test_taking_shell.md`

Status:
Done. Accepted by PM/reviewer on 2026-06-16 after the implementation handoff was
added.

Summary:
Polished the test-taking shell without changing session, scoring, timer,
response, review, or mix-test behavior. The screen now uses semantic app
background, header, question-area, and footer surfaces; timer/progress/flag are
grouped as a quieter status cluster; question content sits inside the focused
question panel; navigation buttons use approved roles; and Finish is no longer
danger-styled. Progress indicators remain clickable buttons.

Files changed:
- `study_test_tool/gui/test_taking.py`
- `study_test_tool/gui/components/progress_bar.py`
- `study_test_tool/gui/components/timer_widget.py`
- `study_test_tool/gui/styles.py`
- `visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/04_stories/STORY-010_test_taking_shell.md`
- `visual_overhaul_project/06_handoffs/STORY-010_test_taking_shell_handoff.md`
- `visual_overhaul_project/01_context/screenshots/after/STORY-010/`

Definition of Ready checked:
Yes. `STORY-010` was Ready and unblocked, CTX-TEST-TAKING and CTX-FOUNDATION
were Ready, and the PM readiness pass named it as the parallel-safe next core
screen story.

Context summaries read:
- `visual_overhaul_project/01_context/summaries/test_taking_context.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- Accepted handoffs for `STORY-005` and `STORY-007`
- `visual_overhaul_project/06_handoffs/PM_readiness_pass_2026-06-16.md`

Context summaries created/updated:
None.

Screens/states checked:
- Normal test first question in light and dark mode.
- Normal test middle question in light and dark mode.
- Normal test last question in light and dark mode.
- Answered and flagged question in light and dark mode.
- Practice mode with checked incorrect feedback in light and dark mode.
- Review-session entry path in light and dark mode.
- Mix-test entry path in light and dark mode.
- Essay question shell in light and dark mode.
- Normal test minimum-window shell in light and dark mode.
- Focused GUI smoke for Previous, Next, progress-click navigation, flag toggle,
  finish confirmation cancellation, practice Check Answer lock, review entry,
  and mix entry.

Screenshot evidence:
- `visual_overhaul_project/01_context/screenshots/after/STORY-010/light/light_test_taking_unanswered.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-010/light/light_test_taking_middle_question.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-010/light/light_test_taking_last_question.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-010/light/light_test_taking_answered_flagged.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-010/light/light_test_taking_practice_incorrect_feedback.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-010/light/light_test_taking_review_session.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-010/light/light_test_taking_mix_test.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-010/light/light_test_taking_essay_question.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-010/light/light_test_taking_minimum_unanswered.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-010/dark/dark_test_taking_unanswered.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-010/dark/dark_test_taking_middle_question.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-010/dark/dark_test_taking_last_question.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-010/dark/dark_test_taking_answered_flagged.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-010/dark/dark_test_taking_practice_incorrect_feedback.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-010/dark/dark_test_taking_review_session.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-010/dark/dark_test_taking_mix_test.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-010/dark/dark_test_taking_essay_question.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-010/dark/dark_test_taking_minimum_unanswered.png`

Tests run:
- `python3 -m compileall -q study_test_tool/gui/test_taking.py study_test_tool/gui/components/progress_bar.py study_test_tool/gui/components/timer_widget.py study_test_tool/gui/styles.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/test_taking.py study_test_tool/gui/components/progress_bar.py study_test_tool/gui/components/timer_widget.py study_test_tool/gui/styles.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --states test_taking_unanswered test_taking_middle_question test_taking_last_question test_taking_answered_flagged test_taking_practice_incorrect_feedback test_taking_review_session test_taking_mix_test test_taking_essay_question test_taking_minimum_unanswered --output visual_overhaul_project/01_context/screenshots/after/STORY-010`
- Focused GUI smoke with seeded temporary data for shell interactions and entry
  paths.
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests/test_test_session.py`
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests/test_practice_mode.py`

Tests not run and why:
Full pytest was not run because this story changed GUI shell layout/styling and
the development screenshot harness. Focused session and practice tests covered
the behavior-sensitive areas.

Acceptance criteria notes:
- Question content remains the dominant screen content inside a semantic
  question surface.
- Timer, progress label, and flag state are visible in a compact header cluster.
- Finish uses the primary role instead of danger styling.
- Previous and Next use secondary role styling; Check Answer uses the primary
  role when shown in practice mode.
- Normal, practice, review, and mix-test entry paths were smoke checked.
- Progress indicators remain clickable `CTkButton` widgets and preserve current
  status precedence.

Scope-adjacent notes for PM review:
- `capture_baseline_screenshots.py` now has additional test-taking states for
  middle question, last question, review session, and minimum-window normal
  shell evidence.
- `get_button_style()` filled roles now explicitly set `border_width=0` so
  buttons can safely switch between tertiary and filled roles, such as Flag and
  Unflag, without retaining the tertiary border.

Risks:
- Practice feedback is still the pre-existing gray feedback surface because
  `STORY-011` owns practice feedback redesign.
- Answer rows remain the pre-existing radio-button/label pattern because
  `STORY-011` owns answer row redesign.
- The header title wrap length is tuned for current seeded titles. Very long
  real test names should be rechecked during later validation.

Follow-up backlog items:
- `STORY-011_answer_rows_and_practice_feedback.md`: redesign answer rows and
  practice feedback on top of the accepted shell.
