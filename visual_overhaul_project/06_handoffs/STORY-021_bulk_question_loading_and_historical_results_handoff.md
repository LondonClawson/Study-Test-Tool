# STORY-021 Bulk Question Loading and Historical Results Retrieval Handoff

Story/Task: `STORY-021_bulk_question_loading_and_historical_results.md`

Status: Done. Accepted by PM authorization.

Summary: Replaced the per-question option lookup with a single joined question
and option query. Historical Results now retrieves only questions referenced by
the selected attempt rather than eagerly loading its complete source test.

Files changed:

- `study_test_tool/database/db_manager.py`
- `study_test_tool/services/question_service.py`
- `study_test_tool/gui/results_view.py`
- `study_test_tool/tests/test_db_manager.py`
- `04_stories/STORY-021_bulk_question_loading_and_historical_results.md`
- `00_project/status_board.md`
- This handoff

Definition of Ready checked: `CTX-PERFORMANCE-SCALE` and `CTX-RESULTS` are
Ready. The story has one bounded data-access objective and preserves existing
Results behavior.

Context summaries read:

- `performance_scalability_audit.md`
- `results_context.md`

Context summaries created/updated: None.

Screens/states checked: Historical Results with populated question review in
light and dark mode.

Screenshot evidence:

- `01_context/screenshots/after/STORY-021/light/light_results_loaded_from_history.png`
- `01_context/screenshots/after/STORY-021/dark/dark_results_loaded_from_history.png`

Tests run:

- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests/test_db_manager.py`
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests`
- `git diff --check`

Tests not run and why: None.

Acceptance criteria notes: Full-test loading retains question and option order,
including essay questions with no options. Attempt retrieval returns only the
answered questions in saved response order; unknown and response-less attempts
return an empty list. The existing Results review-card content remains intact.

Risks: The joined query repeats question columns once per option, trading a
small amount of result-set duplication for the removal of N+1 SQLite calls.
Historical Results remains synchronous by scope; representative-device timing
benchmarks remain future work.

Follow-up backlog items:

- Benchmark full-test and historical-results loads using representative large
  local databases before considering background Results retrieval.
- Evaluate the remaining R-009 Mix-selection and History-pagination findings.

Acceptance note: PM accepted the completed bulk question/options loading and
attempt-specific Historical Results retrieval work.
