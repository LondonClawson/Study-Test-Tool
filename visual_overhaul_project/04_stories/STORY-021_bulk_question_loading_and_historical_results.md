# STORY-021: Bulk Question Loading and Historical Results Retrieval

## Status

Done. Accepted by PM authorization.

## Goal

Remove the per-question option-query path for full test loads and avoid
loading an entire source test when Historical Results only needs the questions
answered in one attempt.

## Required Context

- `CTX-PERFORMANCE-SCALE`
- `CTX-RESULTS`

## In Scope

- One joined query that hydrates a test's questions and options in order.
- Attempt-specific question retrieval with options, ordered by the attempt's
  saved responses.
- Historical Results wiring to use the attempt-specific loader.
- Focused database/service tests and light/dark Historical Results validation.

## Out Of Scope

- Background Results loading, loading-state changes, schema or migration work.
- Changes to scoring, review rendering, question order, answer content, flags,
  Mix selection, or export behavior.

## Acceptance Criteria

- Loading a test with N questions no longer issues an options query for each
  question.
- Full-test callers receive the same question fields, question ordering, and
  option ordering as before, including essay questions with no options.
- Historical Results loads only the questions referenced by the selected
  attempt and retains its current review-card content and response order.
- Unknown or response-less attempts return no questions without an error.

## Verification

- Run focused database and question-service tests, then the full pytest suite.
- Capture light/dark `results_loaded_from_history` evidence in
  `01_context/screenshots/after/STORY-021/`.
- Run `git diff --check`.
