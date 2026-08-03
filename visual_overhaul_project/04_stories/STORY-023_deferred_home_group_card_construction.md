# STORY-023: Deferred Home Group-Card Construction

## Status

Done. Accepted by user authorization after review of the implementation, full
regression, and required Home screenshot evidence.

## Goal

Keep Home responsive for libraries with many tests by creating test-card widgets
only when their active or archived group is expanded.

## Required Context

- `CTX-HOME`
- `CTX-PERFORMANCE-SCALE`

## In Scope

- Deferred active and archived Home card construction by group.
- One-time card rendering for each group expansion within a Home refresh cycle.
- Refresh, sorting, archive, unarchive, delete, import, and Collapse/Expand All
  lifecycle preservation.
- Light/dark Home screenshot validation.

## Out Of Scope

- Changes to test queries, question-count batching, services, persistence,
  scoring, card styles, card actions, or Home layout.
- Lazy construction of non-Home frames, History pagination/index changes, and
  Mix query benchmarking.

## Acceptance Criteria

- A collapsed Home group has no child test-card widgets until first expanded.
- Expanding a group renders its current cards once; repeated collapse/expand
  does not duplicate cards.
- Refresh restores expanded groups with cards and leaves collapsed groups
  unrendered, while preserving current grouping, sorting, counts, and actions.
- Collapse All and Expand All retain their current labels and behavior.
- Active, archived, and zero-question cards retain their current presentation
  and callbacks after deferred rendering.

## Verification

- Run the full pytest suite.
- Capture light/dark `home_populated_grouped`, `home_expanded_cards`,
  `home_expanded_archived_cards`, and `home_minimum_populated` evidence in
  `01_context/screenshots/after/STORY-023/`.
- Smoke-check first and repeated expansion, Collapse/Expand All, sorting, and
  refresh after archive/unarchive.
- Run `git diff --check`.
