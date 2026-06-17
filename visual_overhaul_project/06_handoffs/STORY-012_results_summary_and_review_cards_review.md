# STORY-012 Results Summary And Review Cards Review

Story/Task:
`STORY-012_results_summary_and_review_cards.md`

Status:
Changes Requested by PM/reviewer on 2026-06-16.

Summary:
The visual results work is mostly on track and the submitted focused checks
pass, but the implementation cannot be accepted yet because Results retains
stale retake state across `on_show(...)` calls. This can route Retake Test from
a history-loaded result into a previous mixed/practice result.

Required Fix:
- Reset all retained retake state before rendering each new Results payload:
  `_test_id`, `_mode`, `_mix_questions`, `_mix_name`, and `_mix_subtitle`.
- Then let `_show_from_session(...)` and `_show_from_db(...)` repopulate only
  the state that belongs to the current result.
- Add or run a focused smoke/test proving this sequence: show a mixed or
  practice result, then show a history-loaded regular attempt, then Retake Test
  routes to `SCREEN_TEST_TAKING` with the history attempt's `test_id`, not the
  stale mix questions or stale mode.

Finding:
- `study_test_tool/gui/results_view.py:155` clears only review widgets before
  selecting the new data path. It does not reset the retained retake fields.
  `_show_from_db(...)` sets `_test_id` at
  `study_test_tool/gui/results_view.py:280`, but it leaves prior
  `_mix_questions`, `_mix_name`, `_mix_subtitle`, and `_mode` intact.
  `_on_retake(...)` at `study_test_tool/gui/results_view.py:586` checks
  `_mix_questions` first, so stale mix state wins over the current history
  attempt. A stale practice `_mode` can also leak into a later history retake.

Evidence:
```text
[(('test_taking',), {'mode': 'practice', 'questions': ['stale-mix-question'], 'mix_test_name': 'Stale Mix', 'mix_test_subtitle': 'Stale subtitle'})]
```

That output came from a direct `_on_retake(...)` check with both stale
`_mix_questions` and a current `_test_id` present. The method routed to the mix
path, proving the stale-state precedence problem.

Files reviewed:
- `study_test_tool/gui/results_view.py`
- `visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `visual_overhaul_project/04_stories/STORY-012_results_summary_and_review_cards.md`
- `visual_overhaul_project/06_handoffs/STORY-012_results_summary_and_review_cards_handoff.md`
- `visual_overhaul_project/01_context/screenshots/after/STORY-012/`

Context checked:
- `visual_overhaul_project/01_context/summaries/results_context.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/00_project/screenshot_evidence_policy.md`
- `visual_overhaul_project/00_project/status_transition_rules.md`

Screenshot evidence reviewed:
- `visual_overhaul_project/01_context/screenshots/after/STORY-012/light/light_results_partial_score_essay_flagged.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-012/dark/dark_results_mix_breakdown.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-012/light/light_results_loaded_from_history.png`

Verification run during review:
- `python3 -m compileall -q study_test_tool/gui/results_view.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/results_view.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests/test_scoring_service.py study_test_tool/tests/test_mix_service.py`
- `PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --mode both --states results_all_correct results_partial_score_essay_flagged results_essay_review results_missing_answer results_mix_breakdown results_loaded_from_history --output visual_overhaul_project/01_context/screenshots/after/STORY-012`
- `git diff --check`

Verification results:
- Syntax check passed.
- Black check passed.
- Focused pytest passed: 31 passed, 4 collection warnings.
- Screenshot validation passed: 12 screenshots.
- `git diff --check` passed before tracker status edits.

Notes:
- I did not find a required scoring, persistence, or mix-source calculation
  failure in the focused checks.
- The dark mix-breakdown screenshot is scrolled down to show the breakdown and
  clips the top of the first visible card. I am not making that a blocker for
  this review, but the resubmission should avoid introducing new screenshot
  evidence gaps.
