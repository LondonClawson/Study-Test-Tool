Story/Task:
STORY-017: MVP Visual Regression Pass

Status:
Submitted For Review. PM acceptance is still required; this is not marked Done.

Summary:
Completed the final MVP visual closeout package. Reviewed the acceptance matrix,
baseline audit, foundation decisions, `STORY-016` validation package, and PM
review notes from `STORY-008` through `STORY-015E`. No new app runtime code was
changed. The closeout found no MVP visual blocker in accepted evidence or in the
full test run.

Files changed:
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/03_backlog/acceptance_matrix.md`
- `visual_overhaul_project/04_stories/STORY-017_mvp_visual_regression_pass.md`
- `visual_overhaul_project/06_handoffs/STORY-017_mvp_visual_regression_pass_handoff.md`

Definition of Ready checked:
- `STORY-016_light_dark_and_min_size_validation.md` is Done and accepted by PM.
- `baseline_visual_audit.md` is Ready.
- `visual_foundation_decisions.md` is Ready.
- `STORY-008` through `STORY-015E` are Done.
- PM assigned `STORY-017` to Dev 2 on 2026-06-17.

Context summaries read:
- `visual_overhaul_project/03_backlog/acceptance_matrix.md`
- `visual_overhaul_project/01_context/summaries/baseline_visual_audit.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/06_handoffs/STORY-016_light_dark_and_min_size_validation_handoff.md`
- `visual_overhaul_project/06_handoffs/STORY-016_light_dark_and_min_size_validation_review.md`
- PM review and handoff notes for `STORY-008` through `STORY-015E`

Context summaries created/updated:
None.

Screens/states checked:
- Baseline before evidence: Home populated/empty; Mode and Mix dialogs; Editor
  new/existing; Test Taking unanswered, answered/flagged, practice feedback,
  essay, mix full/partial/multi-group; Results partial and history-loaded;
  History populated/empty; Analytics populated/no-data; Review populated/empty.
- Accepted after evidence: the full `STORY-016` screen-family validation matrix,
  including Home, Test Taking, Results, Editor, History, Analytics, Review, Mode
  dialog, Mix dialog, Import Preview dialog, and documented native-dialog
  exceptions.

Screenshot evidence:
- Baseline comparison evidence:
  `visual_overhaul_project/01_context/screenshots/baseline/`
- Accepted final validation evidence:
  `visual_overhaul_project/01_context/screenshots/after/STORY-016/`
- Validation results:
  - Baseline validation passed for 42 screenshots.
  - `STORY-016` validation passed for 138 screenshots.

Tests run:
- `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --mode both --states home_populated_grouped home_empty_state mode_selection_dialog mix_test_dialog editor_new_test editor_existing_test_with_questions test_taking_unanswered test_taking_answered_flagged test_taking_practice_incorrect_feedback test_taking_essay_question test_taking_mix_test test_taking_mix_partial_group test_taking_mix_multi_group results_partial_score_essay_flagged results_loaded_from_history history_populated analytics_populated review_missed_questions history_empty_state analytics_no_data review_empty_state --output visual_overhaul_project/01_context/screenshots/baseline`
- `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --mode both --group all --output visual_overhaul_project/01_context/screenshots/after/STORY-016`
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests`

Test results:
- Baseline screenshot validation: 42 passed.
- `STORY-016` screenshot validation: 138 passed.
- Full pytest: 231 passed, 13 existing collection warnings.

Tests not run and why:
- No additional GUI capture was run because `STORY-017` is closeout review work
  and the accepted `STORY-016` evidence set already provides the final after
  screenshots. No app runtime code changed.

Acceptance criteria notes:
- Every acceptance matrix row now has evidence, a documented exception, or a
  closeout classification in `acceptance_matrix.md`.
- Before/after comparison shows improvement from the default CustomTkinter
  baseline toward the accepted foundation across app-wide hierarchy, surfaces,
  buttons, cards/lists, empty states, charts, and custom dialogs.
- No known core behavior regression remains open. Earlier Results retake-state
  and Editor minimum-evidence issues were accepted after resubmission.
- Remaining issues are classified below.

MVP blockers:
- None found in accepted screenshot evidence, PM reviews, or the full test run.

Post-MVP follow-up backlog items:
- Add long-content stress screenshot fixtures for long Home names,
  descriptions, and groups; long Test Taking question/answer text; long Results
  answer and essay comparisons; long Editor prompts, options, and group names;
  long History test names; dense Analytics Weak Topics with long names; long
  Review question text; larger Mix dialog source lists; and long Import Preview
  row names.
- Add a chart-readability follow-up for Analytics Study Activity when only one
  populated day renders as a very wide bar.
- Consider a post-MVP custom report/confirmation pattern for native import
  reports, export warnings, or missing-answer confirmations after MVP
  acceptance.

Accepted MVP limitations:
- Native messageboxes and file dialogs remain native by PM decision in
  `STORY-015E`.
- Custom dialogs are fixed-size modal windows and were validated in light/dark
  mode, not through separate minimum-host screenshot states.
- The screenshot harness uses representative seeded data. It is sufficient for
  MVP evidence but not exhaustive for arbitrary user-authored long text.

Risks:
- The only residual visual risk is coverage depth for extreme user-authored
  content, which is documented as post-MVP fixture work rather than an MVP
  blocker.
