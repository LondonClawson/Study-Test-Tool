# STORY-022 Weighted Mix History Scalability Handoff

Story/Task: `STORY-022_weighted_mix_history_scalability.md`

Status: Done. Accepted by user authorization.

Summary: Replaced Mix history's full attempt-timestamp retrieval and Python
bisect with chunked, set-based SQLite retrieval. The public history-stats API,
weight formula, and MixService selection flow are unchanged. Equal completion
timestamps now resolve deterministically by latest attempt ID, then response
ID.

Files changed:

- `study_test_tool/database/db_manager.py`
- `study_test_tool/tests/test_db_manager.py`
- `01_context/summaries/performance_scalability_audit.md`
- `04_stories/STORY-022_weighted_mix_history_scalability.md`
- `00_project/status_board.md`
- This handoff

Definition of Ready checked: The implementation is one bounded database-layer
objective with explicit behavior and verification. It was directly assigned and
accepted by the user; `CTX-PERFORMANCE-SCALE` remains Submitted For Review as
a separate research artifact.

Context summaries read:

- `performance_scalability_audit.md`

Context summaries created/updated: Updated `performance_scalability_audit.md`
to record that Finding 5 is implemented and accepted.

Screens/states checked: No screen changes. Weighted Mix selection behavior is
covered by database and service tests.

Screenshot evidence: Not required; this change does not alter a screen, dialog,
or visual treatment.

Tests run:

- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests/test_db_manager.py study_test_tool/tests/test_mix_service.py`
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests`
- `git diff --check`

Tests not run and why: None.

Acceptance criteria notes: Candidate IDs are deduplicated and queried in chunks
of 900. The database counts attempts with a strictly later completion timestamp,
preserving recovery semantics without materializing global history in Python.

Risks: This is a static correctness and scalability refactor; representative
large-database timing and query-plan evidence are still needed before adding
indexes.

Follow-up backlog items:

- Benchmark Weighted Mix selection with representative question-bank and
  history sizes before considering new indexes.
- Continue the separate deferred Home card, lazy-frame, and History benchmark
  work from the performance audit.

Acceptance note: User accepted the implementation after focused and full-suite
verification.
