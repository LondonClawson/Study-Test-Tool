# STORY-019: Review State and Test-Count Refactor

## Status

Done. Accepted by PM authorization after review of implementation, test, and
screenshot evidence.

## Goal

Consolidate Review data-access behavior, make Review pagination state unit
testable without Tk, and remove per-test count queries from Home, Review scope,
and Mix Test setup.

## Required Context

- `CTX-DATA-VIEWS`
- `CTX-PERFORMANCE-SCALE`

## In Scope

- Shared missed-question query and row-mapping helpers for legacy, page, and
  count paths.
- A GUI-independent pagination/selection state helper with unit tests.
- One batched all-test question-count query used by Home, Review, and Mix Test.

## Out Of Scope

- Changes to Review eligibility, pagination size, selection semantics, scoring,
  schema, migrations, or lazy Home card creation.

## Acceptance Criteria

- Existing full-list and paged Review APIs return equivalent rows for the same
  filters and preserve archive/threshold behavior.
- Pagination and cross-page selection rules have pure unit tests.
- Home, Review scope, and Mix Test setup no longer call the single-test count
  API in loops.
- Full tests and light/dark Home and Review evidence pass.
