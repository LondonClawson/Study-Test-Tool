# STORY-025 History Filter-Index Migration Handoff

Story/Task: `STORY-025_history_filter_index_migration.md`

Status: Done. Accepted by user authorization on 2026-08-03.

Summary: Added the two R-010-validated History filter/order indexes to the
fresh schema and compatibility migration 5. No History query, service, GUI, or
pagination behavior changed.

Files changed:

- `study_test_tool/database/schema.sql`
- `study_test_tool/database/migrations.py`
- `study_test_tool/tests/test_migrations.py`
- `visual_overhaul_project/04_stories/STORY-025_history_filter_index_migration.md`
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/03_backlog/dependency_map.md`
- `visual_overhaul_project/06_handoffs/STORY-025_history_filter_index_migration_handoff.md`

Definition of Ready checked: `CTX-PERFORMANCE-SCALE` and `CTX-DATA-VIEWS` are
Ready. STORY-025 has a single migration scope, named files, observable
acceptance criteria, and a no-screenshot rationale.

Context summaries read: `CTX-PERFORMANCE-SCALE`, including R-010 benchmark
evidence, and `CTX-DATA-VIEWS`.

Context summaries created/updated: None.

Screens/states checked: Database-level History unfiltered, mode-filtered, and
test-plus-mode query support only. The existing History UI and paging behavior
were intentionally not changed.

Screenshot evidence: Not required. This is a schema/migration-only change with
no visible UI, layout, or interaction change.

Tests run:

- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests/test_migrations.py study_test_tool/tests/test_db_manager.py` (38 passed)
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests` (272 passed)
- Disposable fresh and simulated version-4 databases verified both index names
  through `PRAGMA index_list('test_attempts')`.

Tests not run and why: No screenshot harness run; the screenshot policy does
not require it for a non-visual schema-only change.

Acceptance criteria notes: Fresh installs create
`idx_test_attempts_mode_completed_id` and
`idx_test_attempts_test_mode_completed_id`. Migration 5 recreates both indexes
for existing databases and preserves existing attempt data. Migration tests
also retain idempotency coverage.

Risks: The indexes add the R-010-measured storage and write cost. Deep offset
pagination remains linear and must be considered independently.

Follow-up backlog items: Do not combine any later keyset-pagination work with
this migration.
