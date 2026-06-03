# STORY-012: Results Summary And Review Cards

## Status

Blocked.

## Readiness

- Blocked by: CTX-RESULTS, CTX-FOUNDATION.
- Unblocked by: `R-005_results_context.md` and
  `STORY-003_visual_foundation_spec.md`.

## Sprint

Target sprint: Sprint 2.

## User Story

As a learner, I want results to be clear at a glance and detailed enough to
review mistakes so that I can decide what to study next.

## Goal

Polish the results score summary, metadata, status badges, question review cards,
answer comparison layout, and mix-test source breakdown.

## Required Context

- `visual_overhaul_project/01_context/summaries/results_context.md`.
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.
- Research task if context is missing:
  `visual_overhaul_project/02_research_tasks/R-005_results_context.md`.

## Scope

In:

- Score summary presentation.
- Time and essay metadata.
- Correct/incorrect/essay/flagged status treatment.
- Question review cards.
- User answer vs correct answer layout.
- Mix-test source breakdown styling.

Out:

- Scoring changes.
- Attempt persistence changes.
- Retake workflow changes.

## Likely Files

- `study_test_tool/gui/results_view.py`.
- Shared card/badge style entry points.

## Implementation Steps

1. Read CTX-RESULTS, CTX-FOUNDATION, and the Dev 2 Quick Start notes.
2. Inspect only score summary, metadata, status, review-card, answer comparison,
   and mix-source regions named by CTX-RESULTS.
3. Apply hierarchy, badge, card, and answer-comparison styling.
4. Preserve scoring display values, history-loaded result behavior, and mix
   source attribution.
5. Verify all-correct, partial, essay, flagged, missing answer, mix, and
   history-loaded states where practical.
6. Run scoring/mix tests if data handling is touched.

## Acceptance Criteria

- Score is immediately understandable.
- Statuses are visually distinct and readable in light/dark mode.
- User answer and correct answer are easy to compare.
- Essay self-evaluation content is clearly separated from scored content.
- Mix-test source breakdown remains accurate and easier to scan.

## Verification

- Run relevant scoring/mix tests if result data handling is touched:
  `pytest --rootdir=. study_test_tool/tests/test_scoring_service.py`
  `study_test_tool/tests/test_mix_service.py`.
- Smoke check results from a new session and from history.
- Visual check all-correct, incorrect, essay, and mix states if possible.

## Dev 2 Assignment Notes

- Do not change scoring, attempt persistence, retake behavior, or source
  breakdown calculations.
- Do not polish history rows in this story except for result-load smoke checks.
- If CTX-RESULTS is missing or stale, stop and assign R-005.

## Handoff Requirements

- List result states checked.
- List tests run or skipped.
- Include any follow-up for history-loaded result edge cases.
