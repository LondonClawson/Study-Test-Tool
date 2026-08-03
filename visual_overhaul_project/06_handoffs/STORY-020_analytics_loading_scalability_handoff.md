# STORY-020 Analytics Loading Scalability Handoff

Story/Task: `STORY-020_analytics_loading_scalability.md`

Status: Done. Accepted by PM authorization.

Summary: Moved Analytics tab retrieval onto daemon workers with Review-style
queue polling and generation-based stale-result protection. Score Trends now
uses a SQLite window query to return at most 200 evenly distributed attempts,
including the chronological endpoints. Tk and Matplotlib rendering remains on
the UI thread after a current response is received.

Files changed:

- `study_test_tool/database/db_manager.py`
- `study_test_tool/services/analytics_service.py`
- `study_test_tool/gui/analytics_loading.py`
- `study_test_tool/gui/analytics_view.py`
- `study_test_tool/tests/test_analytics_service.py`
- `study_test_tool/tests/test_analytics_loading.py`
- `04_stories/STORY-020_analytics_loading_scalability.md`
- `00_project/status_board.md`
- This handoff

Definition of Ready checked: `CTX-DATA-VIEWS` and `CTX-PERFORMANCE-SCALE` are
Ready. The story's scope remains limited to Analytics loading and bounded trend
data; persistence semantics, filters, grouping, and scoring are unchanged.

Context summaries read:

- `history_analytics_review_context.md`
- `performance_scalability_audit.md`

Context summaries created/updated: None.

Screens/states checked:

- Analytics Score Trends populated and no-data states.
- Analytics Test Comparison populated state.
- Analytics Study Activity populated state.
- Each checked in light and dark mode through the scripted harness.

Screenshot evidence:

- `01_context/screenshots/after/STORY-020/light/light_analytics_populated.png`
- `01_context/screenshots/after/STORY-020/light/light_analytics_test_comparison.png`
- `01_context/screenshots/after/STORY-020/light/light_analytics_study_activity.png`
- `01_context/screenshots/after/STORY-020/light/light_analytics_no_data.png`
- Matching `dark/` captures in the same folder; the harness validated all eight
  images as readable.

Tests run:

- `pytest --rootdir=. study_test_tool/tests/test_analytics_service.py study_test_tool/tests/test_analytics_loading.py` (28 passed)
- `pytest --rootdir=. study_test_tool/tests` (264 passed; 14 pre-existing
  pytest collection warnings)
- `python3 -m py_compile` for changed Analytics Python modules.
- `git diff --check`.

Tests not run and why: No representative production-scale database or timing
fixture is available in the repository, so no benchmark timings were recorded.

Acceptance criteria notes: Database work is asynchronous for every Analytics
tab. The UI applies only the latest request result. Score Trends renders at
most 200 chronological samples, preserving first and last attempts; other
Analytics calculations and no-data messages are unchanged.

Acceptance: Accepted by PM authorization after review of the implementation,
focused and full-suite test results, and light/dark Analytics evidence.

Risks: Weak Topics still creates one card per returned grouping bucket on the
Tk thread. A dataset with an unusually high category/test/group cardinality
may need a separate pagination or virtualization story.

Follow-up backlog items:

- Add a deterministic large-history fixture and record screen-ready timings.
- Evaluate Weak Topics pagination or virtualization if real data shows
  high-cardinality rendering delays.
