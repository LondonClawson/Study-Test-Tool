Story/Task:
`STORY-012_results_summary_and_review_cards.md`

Status:
Done. Accepted by PM/reviewer on 2026-06-17 after retake-state resubmission.

Summary:
Polished the Results screen score summary, result metadata, status badges,
question review cards, answer comparison panels, essay treatment, and mix-test
source breakdown styling. Scoring values, attempt persistence, history-loaded
results, retake routing, and source-breakdown calculations were preserved.

Resubmission addendum:
After PM/reviewer Changes Requested feedback, retained retake routing state is
now reset before every new Results payload. `_show_from_session(...)` and
`_show_from_db(...)` repopulate only the state for the current payload, and
history-loaded attempts now restore their stored mode before Retake Test.

Files changed:
- `study_test_tool/gui/results_view.py`
- `visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/04_stories/STORY-012_results_summary_and_review_cards.md`
- `visual_overhaul_project/06_handoffs/STORY-012_results_summary_and_review_cards_handoff.md`
- `visual_overhaul_project/01_context/screenshots/after/STORY-012/`

Definition of Ready checked:
Yes. `STORY-012` was Ready and unblocked. CTX-RESULTS and CTX-FOUNDATION were
Ready, and the story listed no blocking dependency.

Context summaries read:
- `visual_overhaul_project/01_context/summaries/results_context.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`

Context summaries created/updated:
None.

Screens/states checked:
- All-correct live results in light and dark mode.
- Partial score with flagged incorrect MC and essay content in light and dark
  mode.
- Essay review card scrolled into view in light and dark mode.
- Missing-answer MC review in light and dark mode.
- Mixed-test results with source breakdown in light and dark mode.
- History-loaded results in light and dark mode.
- Focused GUI smoke for new-session results, history-loaded results, regular
  retake routing, and mix retake routing.

Screenshot evidence:
- `visual_overhaul_project/01_context/screenshots/after/STORY-012/light/light_results_all_correct.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-012/light/light_results_partial_score_essay_flagged.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-012/light/light_results_essay_review.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-012/light/light_results_missing_answer.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-012/light/light_results_mix_breakdown.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-012/light/light_results_loaded_from_history.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-012/dark/dark_results_all_correct.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-012/dark/dark_results_partial_score_essay_flagged.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-012/dark/dark_results_essay_review.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-012/dark/dark_results_missing_answer.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-012/dark/dark_results_mix_breakdown.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-012/dark/dark_results_loaded_from_history.png`

Tests run:
- `python3 -m compileall -q study_test_tool/gui/results_view.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/results_view.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests/test_scoring_service.py`
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests/test_mix_service.py`
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests/test_scoring_service.py study_test_tool/tests/test_mix_service.py`
- Focused Results GUI smoke with seeded temporary data for live all-correct
  results, live mixed results, history-loaded results, regular retake routing,
  and mix retake routing.
- Focused PM-requested retake-state regression with seeded temporary data:
  loaded a mixed practice result, then loaded a history regular attempt, then
  confirmed Retake Test routed to `SCREEN_TEST_TAKING` with the history
  attempt's `test_id` and `mode: test`.
- `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --states results_all_correct results_partial_score_essay_flagged results_essay_review results_missing_answer results_mix_breakdown results_loaded_from_history --output visual_overhaul_project/01_context/screenshots/after/STORY-012`
- `PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --mode both --states results_all_correct results_partial_score_essay_flagged results_essay_review results_missing_answer results_mix_breakdown results_loaded_from_history --output visual_overhaul_project/01_context/screenshots/after/STORY-012`
- `git diff --check`

Tests not run and why:
Full pytest was not run. Focused scoring and mix tests covered the protected
data behavior named by the story, and screenshot/GUI smoke checks covered the
visual and navigation states changed here.

Acceptance criteria notes:
- Score and percentage now occupy the primary summary hierarchy, with time,
  scored count, and essay self-evaluation metadata as compact chips.
- Correct, incorrect, essay, and flagged statuses use distinct badges and remain
  readable in light and dark mode.
- Multiple-choice answers now consistently show separate user-answer and
  correct-answer panels, including all-correct and missing-answer cases.
- Essay answers and expected answers are separated from scored MC content with a
  neutral essay badge.
- Mix-test source rows remain grouped by original `question.test_id`, preserve
  the existing MC-only source calculation, and present per-source results as
  scannable rows.
- Results review scroll now resets to the top when fresh Results content loads.
  This prevents stale scroll position from hiding the first review card after
  moving between result states.
- Retake routing state now resets before fresh Results content loads. This
  prevents stale mixed-test questions, mix names, subtitles, or practice mode
  from leaking into a later history-loaded regular result.

Risks:
- The answer panel wrap lengths are fixed to the current Results content width.
  Future minimum-size validation should include unusually long answer text.
- `CTkScrollableFrame` scroll reset uses the existing CustomTkinter parent
  canvas because the widget does not expose a public scroll-reset helper.

Follow-up backlog items:
- Add a future validation case with very long MC answers and essay responses for
  Results, preferably during `STORY-016_light_dark_and_min_size_validation.md`.
