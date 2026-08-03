# STORY-022: Weighted Mix History Scalability

## Status

Done. Accepted by user authorization. `CTX-PERFORMANCE-SCALE` remains
Submitted For Review as a separate research artifact.

## Goal

Keep Weighted Mix selection responsive for large question banks and long
attempt histories without changing its weighting semantics.

## Required Context

- `CTX-PERFORMANCE-SCALE` (Submitted For Review; reviewer/PM acceptance is
  still required before this context can be reused for future work.)

## In Scope

- Chunk candidate question IDs below SQLite host-parameter limits.
- Use set-based database retrieval for each question's latest response and its
  count of strictly later attempts.
- Define deterministic ordering for responses with identical completion times.
- Focused database and Mix weighting tests.

## Out Of Scope

- New indexes, schema migrations, question loading, UI changes, Mix dialog
  changes, or changes to the weighting formula and randomization behavior.

## Acceptance Criteria

- Mix history lookup does not load every attempt timestamp into Python.
- Candidate lists larger than 999 IDs complete without a binding error.
- Unanswered, incorrect, and essay responses retain full weight; correctly
  answered questions retain their existing recovery behavior.
- Equal completion timestamps select the latest attempt, then latest response,
  while counting only strictly later timestamps as recovery attempts.

## Verification

- Run focused database and Mix service tests, then the full pytest suite.
- Run `git diff --check`.
- Screenshot evidence is not required: no user-visible UI changes are in scope.
