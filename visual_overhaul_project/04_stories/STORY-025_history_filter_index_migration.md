# STORY-025: History Filter-Index Migration

## Status

Done. Accepted by user authorization on 2026-08-03 after review of migration
coverage and the full regression suite.

## Goal

Reduce filtered History page and count query cost for large local databases by
adding the two indexes validated by R-010, without changing pagination,
filters, sort order, or public service/database interfaces.

## Required Context

- `CTX-PERFORMANCE-SCALE`
- `CTX-DATA-VIEWS`

## In Scope

- Add `(mode, completed_at DESC, id DESC)` and `(test_id, mode, completed_at
  DESC, id DESC)` indexes for fresh databases.
- Add an idempotent compatibility migration for existing databases.
- Test fresh-schema indexes and migration behavior, including preservation of
  existing attempt data.

## Out Of Scope

- Changes to `get_attempts_page()`, `count_attempts()`, `ScoringService`, or
  `HistoryViewFrame`.
- Keyset pagination, count-query removal, visual changes, screenshot capture,
  or any change to History filter/sort semantics.

## Acceptance Criteria

- New databases contain both History composite indexes after initialization.
- Existing databases receive both indexes through a numbered migration that is
  safe to run repeatedly and preserves attempts.
- Mode-only and test-plus-mode History page/count queries retain their current
  inputs, outputs, and ordering.

## Verification

- Run focused database and migration tests, then the full pytest suite.
- Inspect `PRAGMA index_list('test_attempts')` on fresh and migrated temporary
  databases.
- Screenshots are not required because this story changes no visible UI.
- Run `git diff --check`.

## Handoff Requirements

- Record the migration version, index names, focused and full test commands,
  no-screenshot rationale, and confirmation that pagination remains separate.
