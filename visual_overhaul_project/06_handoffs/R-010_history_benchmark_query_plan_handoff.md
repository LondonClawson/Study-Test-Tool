# R-010 History Benchmark And Query-Plan Handoff

Story/Task: `R-010_history_benchmark_query_plan.md`

Status: Done. Accepted by user authorization on 2026-08-03.

Summary: Completed a reproducible local SQLite benchmark for Finding 8. The
evidence supports two complementary filtered-History indexes and keeps
deep-offset pagination as a separate follow-up.

Files changed:

- `01_context/summaries/performance_scalability_audit.md`
- `02_research_tasks/R-010_history_benchmark_query_plan.md`
- `00_project/status_board.md`
- `01_context/context_index.md`
- `03_backlog/research_backlog.md`
- `03_backlog/dependency_map.md`
- `06_handoffs/R-010_history_benchmark_query_plan_handoff.md`

Definition of Ready checked: R-010 had named inputs, bounded research steps,
explicit no-code constraints, and a reviewer-ready output.

Context summaries read: `CTX-PERFORMANCE-SCALE` and `CTX-DATA-VIEWS`.

Context summaries created/updated: Refreshed `CTX-PERFORMANCE-SCALE` with
SQLite 3.49.1 query-plan, timing, storage, and write-cost evidence; it is now
Ready after user acceptance.

Screens/states checked: History unfiltered first/deep page, mode-filtered
first/deep page, and test-plus-mode first/deep page at the database-query
layer. No live GUI state was required.

Screenshot evidence: Not required. This research task changed no visible UI or
application behavior.

Tests run: No pytest tests run.

Tests not run and why: No application code, schema, migration, or tests changed.
The task used disposable benchmark databases only.

Acceptance criteria notes: The audit records deterministic fixture dimensions,
five-run warmed timing means, `EXPLAIN QUERY PLAN` effects, and a 10,000-row
write-cost comparison. It recommends a separate index-only story for
`(mode, completed_at DESC, id DESC)` and `(test_id, mode, completed_at DESC,
id DESC)`.

Risks: The benchmark is representative synthetic local data, not a production
database. Both indexes add measurable write time and storage. Deep unfiltered
offsets remain slow enough that pagination redesign should be evaluated later,
independently.

Follow-up backlog items: Create and assign a History filter-index migration
story. Do not combine it with keyset pagination or change
`get_attempts_page()`/`count_attempts()` behavior.
