Story/Task:
`STORY-015A_review_screen_polish.md`

Status:
Done. Accepted by PM/reviewer on June 16, 2026.

Summary:
Polished the Review screen shell, scope selector, action bar, missed-question
cards, and Review empty states using the accepted visual foundation. The screen
now uses shared page header, card, text, button, spacing, and color roles while
preserving the existing review service calls, scope checkbox behavior, selected
question tracking, and Start Review fallback path.

Files changed:
- `study_test_tool/gui/review_view.py`
- `study_test_tool/gui/styles.py`
- `visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `visual_overhaul_project/04_stories/STORY-015A_review_screen_polish.md`
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/06_handoffs/STORY-015A_review_screen_polish_handoff.md`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015A/`

Definition of Ready checked:
`CTX-DATA-VIEWS`, `CTX-FOUNDATION`, and accepted foundation handoffs for
`STORY-005`, `STORY-006`, and `STORY-007` were available and sufficient.

Context summaries read:
- `visual_overhaul_project/01_context/summaries/history_analytics_review_context.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`

Context summaries created/updated:
None.

Screens/states checked:
- Review with active tests and missed questions.
- Review scoped to one selected test.
- Review with one selected missed question.
- Review with no selected tests.
- Review scoped to an active test with no missed questions.
- Review with no active tests.
- Review missed questions at the minimum supported window size.
- Light and dark modes.

Screenshot evidence:
- `visual_overhaul_project/01_context/screenshots/after/STORY-015A/light/light_review_missed_questions.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015A/light/light_review_selected_scope.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015A/light/light_review_selected_questions.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015A/light/light_review_no_selected_tests.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015A/light/light_review_minimum_missed_questions.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015A/light/light_review_no_missed_questions.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015A/light/light_review_empty_state.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015A/dark/dark_review_missed_questions.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015A/dark/dark_review_selected_scope.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015A/dark/dark_review_selected_questions.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015A/dark/dark_review_no_selected_tests.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015A/dark/dark_review_minimum_missed_questions.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015A/dark/dark_review_no_missed_questions.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015A/dark/dark_review_empty_state.png`

Tests run:
- `python3 -m compileall -q study_test_tool/gui/review_view.py study_test_tool/gui/styles.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/review_view.py study_test_tool/gui/styles.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests/test_review_service.py`
- `PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --mode both --states review_missed_questions review_selected_scope review_selected_questions review_no_selected_tests review_minimum_missed_questions review_no_missed_questions review_empty_state --output visual_overhaul_project/01_context/screenshots/after/STORY-015A`
- GUI smoke: opened Review with seeded data, selected one missed question,
  verified selected-count text, verified Start Review routes to
  `SCREEN_TEST_TAKING`, checked no-selected-tests and no-missed-question empty
  states, and checked the empty database no-active-tests state.
- Screenshot capture: `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --states review_missed_questions review_selected_scope review_selected_questions review_no_selected_tests review_minimum_missed_questions review_no_missed_questions review_empty_state --output visual_overhaul_project/01_context/screenshots/after/STORY-015A`
- `git diff --check`

Tests not run and why:
Full pytest was not run. This story changed Review GUI styling, a narrow shared
text role, and screenshot harness states. Focused Review service tests, GUI
smoke, compile/format checks, and screenshot validation cover the changed
surface.

Acceptance criteria notes:
- Scope summary, scope selector, selected count, and Start Review now have
  clearer hierarchy.
- Start Review uses the primary action role rather than success styling.
- Missed-question cards use the shared card surface and semantic text roles.
- Empty states distinguish no active tests, no selected tests, no missed
  questions, and no frequently missed questions.
- Existing checkbox variables, scope selection methods, selected-count behavior,
  review service calls, and Start Review fallback behavior were preserved.
- Added a narrow `body_bold` text role in `gui.styles` for Review scope group
  labels.
- Added Review-specific screenshot harness states and a no-missed Review
  fixture for repeatable evidence.

Risks:
- Long test names and unusually long missed-question text should still be
  covered in `STORY-016_light_dark_and_min_size_validation.md`.
- Review and Analytics now repeat similar local segmented-control and checkbox
  styling helpers. Defer extraction until another screen proves the pattern is
  stable.

Follow-up backlog items:
- Use `STORY-016_light_dark_and_min_size_validation.md` to validate Review with
  longer names/questions and deeper missed-question lists.

PM/reviewer acceptance:
- Accepted on June 16, 2026 after inspection of the submitted Review screen
  implementation, light/dark screenshot evidence, and focused verification.
- The implementation stays within the GUI polish scope and preserves Review
  service calls, scope selection semantics, selected-count behavior, and the
  Start Review fallback path.
- No required changes were found. Remaining long-content coverage belongs in
  `STORY-016_light_dark_and_min_size_validation.md`.
