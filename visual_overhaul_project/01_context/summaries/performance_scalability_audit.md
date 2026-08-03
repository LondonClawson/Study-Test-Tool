# Performance Scalability Audit

## Metadata

- Summary ID: `CTX-PERFORMANCE-SCALE`.
- Produced by: `R-009_performance_scalability_audit.md`; refreshed by
  `R-010_history_benchmark_query_plan.md`.
- Status: Ready. R-010's benchmark evidence and Finding 8 recommendation were
  accepted by user authorization on 2026-08-03.
- Scope: static audit of application startup, Home, History, Analytics, Review,
  Results, test loading, and weighted Mix Test selection.
- Audience: post-MVP engineering planning.

## Purpose

Identify data-loading and rendering paths likely to produce long waits for
users with hundreds or more questions and a large test-attempt history.

## Observed Findings

### 1. Review performs unbounded history aggregation and unbounded card rendering

`DatabaseManager.get_missed_questions()` joins questions, responses, and tests,
groups all matching question responses, and returns every missed question.
`ReviewViewFrame._load_questions()` calls it on the Tk UI thread, and
`_display_questions()` immediately creates a card for every returned item.
Each card contains a `FormattedText` widget.

- Sources: `database/db_manager.py:682-736`, `gui/review_view.py:402-439`, and
  `gui/components/formatted_text.py:37-55,133-145`.
- Scaling: database work grows with the relevant `question_responses` history;
  UI work grows with the number of missed questions and question-text length.
- User effect: opening Review or changing scope/filter can freeze before the
  user can interact with the screen.

### 2. Analytics reads and draws unbounded history synchronously

Score Trends returns every matching test-mode attempt and then plots every
point with Matplotlib on the Tk UI thread. Weak Topics also aggregates all
scored responses before creating one card per grouping bucket.

- Sources: `database/db_manager.py:926-984,1002-1090` and
  `gui/analytics_view.py:229-388`.
- Scaling: Score Trends grows with total matching attempts; weak-topic queries
  grow with historical responses, with additional widget work for high-cardinality
  categories or tests.
- User effect: Analytics can block navigation, redraw slowly when switching
  filters/tabs, and produce dense, hard-to-read charts.

### 3. Loading a test uses one option query per question

`_load_questions()` fetches the questions for one test, then queries options in
a loop. This is an N+1 query pattern: a 500-question test produces 501 SQL
queries. It is used by test-taking, editing, mix selection, and historical
result loading.

- Source: `database/db_manager.py:315-352`.
- Scaling: query count grows linearly with the questions in a source test.
- User effect: selecting or editing a large test has unnecessary SQLite and
  object-construction overhead even before UI rendering begins.

### 4. Historical Results load a whole source test for a single attempt

When viewing a saved attempt, Results loads that attempt and then calls
`get_test_by_id()`, which eagerly loads every question and option in its source
test only to map the response question IDs.

- Sources: `gui/results_view.py:307-353` and `database/db_manager.py:135-164`.
- Scaling: cost follows the entire test size rather than the number of
  questions actually answered in the selected attempt.
- User effect: a short historical attempt from a very large test can still
  open slowly. The existing deferred review-card rendering does not remove
  this initial data-load cost.

### 5. Weighted Mix history lookup is implemented and accepted

`STORY-022` replaces the full attempt-timestamp read with chunked, set-based
lookup of each candidate question's latest response and strictly later attempt
count. Candidate IDs are limited to chunks of 900, and equal completion times
resolve by attempt ID and then response ID.

- Sources: `database/db_manager.py:get_question_history_stats` and
  `services/mix_service.py:64-113`.
- Scaling: no attempt-history list is materialized in Python; database work is
  bounded by the candidate-ID chunk size, although representative timing and
  query-plan evidence is still needed.
- User effect: the prior host-parameter failure path is removed. Large-bank
  responsiveness remains pending benchmark validation.

### 6. Home still eagerly builds hidden cards; per-test count queries are resolved

Home now retrieves counts in one batched call for both its list and the Mix
dialog. It still creates all active and archived test cards while rebuilding
the list, even when their containing group starts collapsed. Review's former
per-test count pattern has been replaced by shared query helpers.

- Sources: `gui/test_selector.py:344-423` and `gui/test_selector.py:854-862`.
- Scaling: Tk widget count grows with the number of tests; count-query work is
  bounded to the initial batched retrieval.
- User effect: accounts with many small tests can see slow Home/Review entry
  despite groups being visually collapsed.

### 7. Startup still eagerly constructs all screens

`App.__init__()` creates all frames before showing Home. This includes the
Analytics frame and its embedded Matplotlib widget.

- Sources: `gui/main_window.py:62-84` and `gui/components/graph_widget.py:24-62`.
- Scaling: mostly fixed startup overhead, not database-size dependent.
- User effect: it adds to perceived launch time after the visual update, even
  when a user only needs Home.

### 8. History remains bounded, with deep-pagination/index concerns

History now loads 50 rows in a background thread rather than loading all
attempts into the screen. It still issues a `COUNT(*)` for every page and uses
offset pagination. Large offsets become progressively more expensive, and
mode-filtered ordering has no matching composite index in the schema.

- Sources: `gui/history_view.py:284-409`, `database/db_manager.py:526-588`, and
  `database/schema.sql:58-64`.
- User effect: initial History load is bounded; repeated Load More requests and
  filtered history can still degrade at very large history sizes.

#### R-010 benchmark and query-plan evidence

On 2026-08-03, R-010 used a disposable local SQLite 3.49.1 database with 10
tests and 100,000 evenly distributed Test/Practice attempts. Each 50-row page
and matching count query was warmed once and measured five times. The fixture
and every temporary candidate index were deleted after measurement.

| Query state | Current page / count | Both candidate indexes page / count | Query-plan change |
| --- | --- | --- | --- |
| Unfiltered first page | 0.13 / 0.97 ms | 0.13 / 0.89 ms | Existing `completed_at` index remains appropriate |
| Mode first page | 2.43 / 6.31 ms | 0.14 / 1.51 ms | Completed-at scan becomes ordered `mode` index search |
| Test + mode first page | 5.35 / 4.05 ms | 0.15 / 0.34 ms | Test-id lookup plus temporary sort becomes ordered composite-index search |
| Unfiltered deep offset (90,000) | 57.38 / 0.87 ms | 57.87 / 0.95 ms | No material change; offset remains linear |
| Mode deep offset (49,000) | 64.51 / 6.48 ms | 32.70 / 1.62 ms | Ordered mode index avoids scanning nonmatching rows, but offset remains linear |
| Test + mode deep offset (4,500) | 14.00 / 4.10 ms | 0.36 / 0.36 ms | Ordered test-and-mode index eliminates the temporary sort |

The indexes are complementary: the mode-only index does not optimize the
test-and-mode order, and the test-and-mode index does not optimize mode-only
filtering. A 10,000-attempt transactional insert took 56.66 ms and grew the
baseline 8.72 MB fixture to 9.62 MB. With both candidate indexes, the insert
took 204.55 ms and the fixture grew from 16.65 MB to 19.61 MB. That measurable
write and storage cost is acceptable for the observed filtered-History read
improvement, subject to reviewer acceptance.

## Follow-Up Status

- Findings 1 and 2 are implemented and accepted through `STORY-018` and
  `STORY-020`.
- Findings 3 and 4 are implemented and accepted through `STORY-021`.
- Finding 6 has batched test counts implemented through `STORY-019`; deferred
  Home card creation remains unimplemented.
- Finding 5 is implemented and accepted through `STORY-022`.
- Findings 7 and 8 remain unimplemented.
- Finding 8 benchmark research is accepted through
  `R-010_history_benchmark_query_plan.md`.

## Remaining Recommendations

1. (Finding 5) Benchmark the accepted Mix query with representative question
   banks and histories before adding indexes.
2. (Finding 6) Create Home test-card widgets only on group expansion; batched test-count
   retrieval is already implemented.
3. (Finding 7) Consider lazy frame construction so Matplotlib does not delay the initial
   Home screen.
4. (Finding 8) Assign a small index-only History story to
   add `(mode, completed_at DESC, id DESC)` and `(test_id, mode,
   completed_at DESC, id DESC)` in both `schema.sql` and a new compatibility
   migration. Preserve the existing page/count interfaces, filters, and sort
   order. Keep keyset pagination as a separate research or implementation item.

## Recommended Story Splits

Keep the remaining work separate so query-semantics changes, Home widget
lifecycle changes, startup navigation changes, and history index decisions can
be reviewed independently:

1. Weighted Mix history-query scalability (Finding 5) is accepted through
   `STORY-022`; benchmark it before deciding whether an index migration is
   justified.
2. Deferred Home group-card construction (Finding 6), including expansion,
   collapse, sorting, archive, and refresh lifecycle coverage.
3. Lazy non-Home frame construction (Finding 7), including navigation and
   `on_show` behavior for every screen.
4. History filter-index migration (Finding 8); keep deep-pagination redesign
   separate.

## Behavior Constraints

- Preserve current scoring, practice-mode locking, review selection, mix
  weighting semantics, and history sort/filter behavior.
- Keep all SQL in the database layer and retain compatibility migration support
  for existing user databases.
- UI changes must maintain usable loading, empty, error, and incremental-load
  states; background work must only update Tk widgets on the UI thread.

## Implementation Risks

- Changing mix history queries can change question-selection distribution.
- Pagination must preserve Review's "Start Review all displayed" semantics and
  give users an explicit way to select beyond the current page if intended.
- New indexes need both fresh-schema entries and migrations for existing local
  databases.
- Virtualized/delayed widgets need careful cancellation when leaving a screen,
  as Results already demonstrates for deferred review rendering.

## States Not Runtime-Tested

This is a static source audit. No production-sized database was available, no
GUI runtime benchmarking was performed, and no screenshots were needed because
no visual or application code changed.

## Dev 2 Quick Start

`STORY-018` through `STORY-024` have addressed the prior Review, Analytics,
shared question-loading, Mix history-query, Home-card, and startup priorities.
Assign only the bounded History filter-index migration; keep deep-pagination
redesign separate. Run the full suite for the future database migration or
shared-service change.
