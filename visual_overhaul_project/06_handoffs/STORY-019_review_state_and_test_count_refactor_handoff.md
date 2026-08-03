# STORY-019 Review State and Test-Count Refactor Handoff

Story/Task: `STORY-019_review_state_and_test_count_refactor.md`

Status: Done. Accepted by PM authorization after review of implementation,
test, and screenshot evidence.

Summary: Consolidated missed-question aggregation into shared database helpers,
extracted GUI-independent Review pagination/selection state, and replaced
per-test question-count calls in Home, Review scope, and Mix Test setup with
one grouped count query.

Files changed:

- `study_test_tool/database/db_manager.py`
- `study_test_tool/services/test_service.py`
- `study_test_tool/gui/review_pagination.py`
- `study_test_tool/gui/review_view.py`
- `study_test_tool/gui/test_selector.py`
- `study_test_tool/tests/test_db_manager.py`
- `study_test_tool/tests/test_review_service.py`
- `study_test_tool/tests/test_review_pagination.py`
- `04_stories/STORY-019_review_state_and_test_count_refactor.md`
- `00_project/status_board.md`
- This handoff

Definition of Ready checked: `CTX-DATA-VIEWS` and `CTX-PERFORMANCE-SCALE` are
Ready. The story is a bounded behavior-preserving cleanup of the accepted
Review scalability work.

Context summaries read:

- `history_analytics_review_context.md`
- `performance_scalability_audit.md`

Context summaries created/updated: None.

Screens/states checked:

- Home populated and grouped.
- Review missed questions.
- Light and dark mode for both states.

Screenshot evidence:

- `01_context/screenshots/after/STORY-019/light/`
- `01_context/screenshots/after/STORY-019/dark/`

Tests run:

- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests/test_db_manager.py study_test_tool/tests/test_review_service.py study_test_tool/tests/test_review_pagination.py`
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests`
- `git diff --check`

Tests not run and why: No additional GUI unit-test harness exists; the light
and dark captures cover the changed Home and Review presentation paths.

Acceptance criteria notes: Full-list and paged Review calls share query,
ordering, row mapping, archive filtering, and threshold behavior. The pure
state tests cover next/previous offsets, cross-page explicit selections,
visible-page select-all, fallback selection, and reset. The affected GUI paths
no longer call the single-test count API in a loop.

Risks: The grouped count query eliminates N+1 count calls but still calculates
all counts when a large Home or Mix dialog is opened. Missed-question
aggregates remain query-time calculations; the audit's index/caching follow-up
should be evaluated with production-scale local data before further changes.

Follow-up backlog items:

- Implement Analytics retrieval/plotting scalability from R-009.
- Implement bulk question/options retrieval and historical-result loading from
  R-009.
- Evaluate Review aggregate-query performance against production-scale local
  databases before adding indexes or cached statistics.
