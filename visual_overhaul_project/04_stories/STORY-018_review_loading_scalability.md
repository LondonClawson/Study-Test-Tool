# STORY-018: Review Loading Scalability

## Status

Done. Accepted by PM authorization.

## Goal

Keep the Missed Questions screen responsive for large question banks and long
attempt histories by retrieving and rendering bounded pages in the background.

## Required Context

- `CTX-DATA-VIEWS`
- `CTX-PERFORMANCE-SCALE`

## In Scope

- Paged missed-question and frequently-missed retrieval with totals.
- Background retrieval and stale-result protection in Review.
- Previous/Next controls, visible-page summary, and persistent explicit
  selections across pages.
- Focused service tests and Review screenshot validation.

## Out Of Scope

- Changing scoring, missed-question eligibility, review-session behavior, or
  mix-test selection.
- Per-test scope-count batching, broader review-session question loading, and
  database index/schema changes.

## Acceptance Criteria

- Review renders at most 50 question cards per page.
- Scope/filter/page changes do not block the Tk event loop while data is read.
- Out-of-date worker responses cannot overwrite the current scope, filter, or
  page.
- Explicit selections persist across pages; Select All affects the visible
  page; no explicit selection starts the visible page only.
- Existing empty states, archived-test exclusion, and frequent-miss thresholds
  remain intact.
