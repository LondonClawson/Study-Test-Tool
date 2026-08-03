# R-010: History Benchmark And Query-Plan Research

## Status

Done. Accepted by user authorization on 2026-08-03. The recommended History
filter-index migration is unblocked as a separate implementation story.

## Role

Assign to Dev 1 Research Agent. This is not an implementation task.

## Goal

Measure the History attempt-list and count queries at representative local
SQLite scale, inspect their query plans, and recommend whether an index or a
pagination strategy story is justified. This resolves Finding 8 of
`CTX-PERFORMANCE-SCALE` without changing History behavior prematurely.

## Output

Update:

`visual_overhaul_project/01_context/summaries/performance_scalability_audit.md`

with reproducible fixture dimensions, timing observations, query-plan results,
and a bounded recommendation for any follow-up implementation story.

## Required Inputs

- `00_project/status_board.md`
- `01_context/summaries/performance_scalability_audit.md`
- `01_context/summaries/history_analytics_review_context.md`
- Current database schema, History data path, and database tests

## Source Files

Inspect:

- `study_test_tool/database/db_manager.py`
- `study_test_tool/database/schema.sql`
- `study_test_tool/database/migrations.py`
- `study_test_tool/gui/history_view.py`
- `study_test_tool/services/scoring_service.py`
- `study_test_tool/tests/test_db_manager.py`

## Screens Or States To Inspect

- History initial load with no filters.
- History with a mode filter.
- History with a test and mode filter.
- A deep Load More request using the current offset behavior.

## Do Not Change

- Do not change application code, tests, database schema, or migrations.
- Do not redesign History or change its filters, sort order, loading states, or
  pagination behavior.
- Do not add an index until a separately reviewed implementation story is
  assigned.

## Research Steps

1. Read the required context and identify the exact count and page queries.
2. Build a disposable deterministic SQLite fixture at representative history
   sizes without committing generated data.
3. Capture `EXPLAIN QUERY PLAN` and representative timings for unfiltered,
   mode-filtered, test-and-mode-filtered, and deep-offset queries.
4. Compare the observed plans against the existing indexes and candidate
   composite indexes named by the performance audit.
5. Record reproducible commands, findings, constraints, and a specific
   implementation recommendation only if supported by the measurements.
6. Update the audit, backlog/dependency metadata if needed, and write a
   handoff for reviewer acceptance.

## Done Criteria

- The audit records fixture dimensions, query-plan evidence, and timings or an
  explicit environment limitation.
- The recommendation distinguishes evidence from a proposed index or pagination
  change.
- No application code, schema, or migration changes are included.
- The context index, status board, and handoff reflect the proposed status.

## Completed Evidence

On 2026-08-03, a disposable SQLite 3.49.1 fixture containing 10 tests and
100,000 evenly distributed Test/Practice attempts was measured with 50-row
pages. Each query was warmed once and measured five times. The complete timing,
query-plan, and write-cost results are recorded in
`performance_scalability_audit.md`.

The evidence supports a separate index-only story adding `(mode, completed_at
DESC, id DESC)` and `(test_id, mode, completed_at DESC, id DESC)` to the fresh
schema and compatibility migrations. It does not support coupling that work to
a pagination redesign: the existing completed-at index already serves
unfiltered ordering, but deep `OFFSET` costs remain linear.
