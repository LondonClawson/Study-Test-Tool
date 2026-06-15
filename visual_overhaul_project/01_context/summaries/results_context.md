# Results Context Summary

## Metadata

- Summary ID: CTX-RESULTS.
- Summary file: `visual_overhaul_project/01_context/summaries/results_context.md`.
- Created: 2026-06-03.
- Last updated: 2026-06-03.
- Produced by research task:
  `visual_overhaul_project/02_research_tasks/R-005_results_context.md`.
- Research agent: Codex.
- Source files inspected: `VISUAL_OVERHAUL_PLAN.md`,
  `visual_overhaul_project/01_context/summaries/gui_architecture_summary.md`,
  `visual_overhaul_project/01_context/summaries/current_visual_state_seed.md`,
  `study_test_tool/gui/results_view.py`,
  `study_test_tool/gui/test_taking.py`, `study_test_tool/gui/history_view.py`,
  `study_test_tool/services/scoring_service.py`,
  `study_test_tool/database/db_manager.py`,
  `study_test_tool/models/test_result.py`,
  `study_test_tool/models/question.py`,
  `study_test_tool/tests/test_scoring_service.py`, and
  `study_test_tool/tests/test_mix_service.py`.
- Screens/states inspected: static source inspection for just-completed regular
  test results, just-completed mixed-test results, history-loaded results,
  all-correct multiple-choice scoring, partially correct multiple-choice
  scoring, essay scoring, flagged responses, unanswered responses, missing
  attempt lookup, missing test lookup, and mixed source breakdown.
- Screens/states not inspected: live runtime screenshots, light/dark rendered
  states, minimum-window wrapping behavior, very long answer text, and deleted
  question/test history edge cases beyond static code paths.

## Purpose

Use this summary before implementing results visual stories, especially
`STORY-012_results_summary_and_review_cards.md`. It narrows the results screen
data paths, widget structure, UI states, visual issues, and behavior constraints
so implementation can focus on hierarchy, cards, badges, and answer comparison
without rediscovering scoring or persistence behavior.

## Current Structure

`ResultsViewFrame` in `study_test_tool/gui/results_view.py` owns the results
screen. It creates `ScoringService` and `TestService`, stores retake state in
`_test_id`, `_mode`, `_mix_questions`, and `_mix_name`, then builds a simple
header, button bar, and scrollable review frame.

`_build_ui()` creates:

- `header_frame`, transparent, packed with horizontal padding.
- `score_label`, large bold label for score and percentage.
- `details_label`, gray body label for time and essay metadata.
- Transparent button frame with same-weight `Back to Home` and `Retake Test`
  buttons.
- `review_frame`, a `CTkScrollableFrame` containing review cards and optional
  mixed-source breakdown.

`on_show(attempt_id=None, session=None, score_data=None, **kwargs)` clears only
`review_frame` children. If both `session` and `score_data` are present, it
calls `_show_from_session()`. Otherwise, if `attempt_id` is present, it calls
`_show_from_db()`.

`_show_from_session()` is the just-completed path. It reads live `TestSession`
questions, responses, flags, mode, mixed-test fields, and score dict values. It
sets the score header to `score/total - percentage%`, sets details to elapsed
time plus essay count if present, creates one review card per session question,
and appends the mixed-source breakdown for mixed tests.

`_show_from_db()` is the history path. It loads `TestAttempt` and persisted
`QuestionResponse` rows through `ScoringService.get_attempt_details()`, loads
the current test questions through `TestService.get_test_by_id()`, maps response
question IDs to questions, and creates one review card per persisted response
that still has a matching question.

`_create_review_card()` is the shared card builder. It renders a `CTkFrame` card
with a transparent header row, question number and optional `[Flagged]` suffix,
a right-aligned text status, question text, and either multiple-choice answer
labels or essay answer/expected-answer labels.

`_show_source_breakdown()` groups live mixed-test questions by original
`question.test_id`, looks up each test name, counts only scored multiple-choice
responses, and renders a separate section after the per-question review cards.
This section is not available from history because mixed attempts are saved as
separate per-source attempts rather than one aggregate attempt.

## Important UI States

- Just-completed regular test: `test_taking.py` saves one attempt, then calls
  results with `attempt_id`, `session`, and `score_data`; the live session path
  wins because both `session` and `score_data` are present.
- Just-completed mixed test: `test_taking.py` saves separate per-source attempts,
  then calls results with `attempt_id=None`, `session`, and `score_data`; the
  aggregate results are visible only from the live session path.
- History-loaded attempt: `history_view.py` calls
  `show_frame(SCREEN_RESULTS, attempt_id=attempt.id)`; results are reconstructed
  from saved attempt details and current question records.
- All-correct multiple choice: status text is `Correct`, colored
  `COLOR_CORRECT`; only the user answer is shown.
- Incorrect multiple choice: status text is `Incorrect`, colored
  `COLOR_INCORRECT`; user answer is colored incorrect and correct answer is
  shown below it.
- Missing multiple-choice answer: scoring treats no answer as incorrect, and
  the card displays `(No answer)`.
- Essay question: `is_correct` is `None`, status text is
  `Essay - Self-evaluate`, score percentage excludes the essay, and both user
  answer and expected answer can be displayed.
- Flagged question: header appends `[Flagged]` to the question number. The
  flagged state is persisted in `question_responses.was_flagged` and displayed
  from both live and history paths.
- Mixed source breakdown: each source test shows either
  `Test name: correct/total (percentage%)` for scored multiple-choice questions
  or `Test name: N essay question(s)` when no scored multiple-choice responses
  exist.
- Missing attempt: score label becomes `Results not found.` and the previous
  details label is not explicitly cleared.
- Missing test on history load: score and details remain visible, but no review
  cards are rendered.

## Workflow Map

- Finish path: `TestTakingFrame._on_finish()` saves the current answer, shows a
  native finish confirmation, stops the timer, calls `session.finish_test()`,
  scores with `ScoringService.score_test()`, persists either one regular
  attempt or separate mixed attempts, then navigates to `SCREEN_RESULTS`.
- Results entry: `App.show_frame()` raises the existing results frame and calls
  `on_show(**kwargs)`. Visual work must keep this argument contract intact.
- Review reset: `on_show()` destroys previous children in `review_frame` before
  building new cards. Header labels are reconfigured by successful data paths.
- Retake regular test: `_on_retake()` navigates to `SCREEN_TEST_TAKING` with
  `test_id=self._test_id` and `mode=self._mode`.
- Retake mixed test: `_on_retake()` navigates to `SCREEN_TEST_TAKING` with the
  original `questions`, `mode`, and `mix_test_name`. Do not discard
  `_mix_questions` when restyling.
- History path: `HistoryViewFrame._on_row_click()` passes only `attempt_id`.
  Results must continue to load attempt details through services rather than
  raw SQLite.

## Visual Findings

- The score header is visually simple and centered, with score, total, and
  percentage collapsed into one text string. It is readable but does not create
  a clear score summary area.
- Details metadata is a gray text line. Time and essay self-evaluation metadata
  are not separated into scannable fields.
- `Back to Home` and `Retake Test` have equal visual weight and placement. The
  primary next action is not identified.
- Review cards use default `CTkFrame` surfaces with `corner_radius=8`, small
  vertical spacing, and minimal internal hierarchy.
- Statuses are text labels rather than badges. Correct/incorrect colors exist,
  but essay and flagged states are low emphasis.
- Flagged state is appended to the question number as `[Flagged]`, making it
  easy to miss when scanning the right-side result status.
- Multiple-choice answer comparison is vertical text. Incorrect cards show both
  answers, but correct cards only show the user answer, so card heights and
  scan patterns vary.
- Essay review content is plain stacked labels. It does not visually separate
  self-evaluation from scored multiple-choice content beyond status text.
- Question text uses `FONT_SIZE_SMALL` and `wraplength=600`, which may be too
  small for review reading and may not adapt cleanly to narrow or wide windows.
- Mixed-source breakdown is appended after all question cards. It uses colored
  text lines but no structured rows, making source attribution less prominent
  than the question review.
- Missing attempt and missing test paths are visually plain. Missing attempt can
  leave stale detail text because only review cards are cleared on show.

## Recommendations For Implementation Stories

- Keep `STORY-012` as one results story if the visual foundation supplies card,
  badge, button, and metadata patterns. Split it if the foundation is still
  broad: first score summary and metadata, then review cards and source
  breakdown.
- Create a score summary band or compact panel at the top with separate score,
  percentage, time, and essay metadata fields.
- Define status badges for correct, incorrect, essay, and flagged. Flagged
  should be visible as a secondary badge, not only bracketed header text.
- Rework answer comparison into structured answer rows or panels with stable
  labels for "Your answer" and "Correct answer"/"Expected answer".
- Make essay cards visually distinct from scored multiple-choice cards while
  keeping the `None` score behavior unchanged.
- Treat the mixed-source breakdown as a small summary section with rows or
  mini-cards, but keep the current grouping and score calculation.
- Preserve the existing scrollable results layout unless a shared page pattern
  replaces it after the visual foundation is approved.
- Add a clear empty/error visual state for `Results not found.` and missing test
  details if that falls within the approved story scope.

## Behavior Constraints

- Do not change `ScoringService.score_test()`: essays must remain unscored
  (`None`), no-answer multiple-choice responses must remain incorrect, and
  percentage must be based on scored multiple-choice responses only.
- Do not change `ScoringService.save_mixed_attempt()`: mixed tests must continue
  saving separate per-source attempts for analytics.
- Do not change the `on_show()` contract or the precedence of live
  `session + score_data` over `attempt_id`.
- Do not change retake behavior for regular or mixed tests.
- Do not replace service calls with raw SQLite access.
- Do not alter persisted response ordering from `get_attempt_details()` unless
  a separate behavior story approves it.
- Do not make the mixed-source breakdown appear in history by inventing an
  aggregate mixed attempt; history currently shows saved per-source attempts.
- Preserve display values: score, total, percentage, time, essay count,
  user answer, correct answer, expected answer, and flagged state.

## Implementation Risks

- Clearing only `review_frame` means header fields can retain stale values in
  error paths. If visual work adds more header widgets, reset them intentionally
  without changing successful data behavior.
- `_create_review_card()` is used by both live and history paths. Styling changes
  must work with live `session.responses` values and persisted
  `QuestionResponse.user_answer` values.
- `is_correct is None` means essay, not unknown. Do not use truthiness checks
  that collapse essay and incorrect states.
- `if not is_correct` currently shows the correct answer for incorrect and essay
  would be unsafe in multiple-choice code if question type checks change.
- Long question/answer text uses fixed wrap lengths. Visual changes should avoid
  clipping or overlap at the app minimum window size.
- Mixed-source breakdown uses `question.test_id`; mixed-test visual work must
  preserve original source IDs carried by `MixService`.
- History-loaded attempts depend on current question records. If a question was
  deleted or unavailable, the current code skips that response card.

## Open Questions

- Should `Retake Test` or `Back to Home` be the primary action after viewing
  results?
- Should correct multiple-choice cards show the correct answer explicitly for
  consistency, or keep the current shorter correct-card display?
- Should mixed-source breakdown appear above question review as part of the
  score summary or remain after the question cards?
- Should history-loaded mixed attempts disclose that they are per-source saved
  attempts rather than the original aggregate mixed session?
- Should missing/deleted question responses be surfaced as unavailable review
  rows instead of silently skipped?

## Dev 2 Quick Start

- Start in `study_test_tool/gui/results_view.py`; the main methods are
  `_build_ui()`, `on_show()`, `_show_from_session()`, `_show_from_db()`,
  `_create_review_card()`, `_show_source_breakdown()`, and `_on_retake()`.
- Read `STORY-012_results_summary_and_review_cards.md` after CTX-FOUNDATION is
  ready; do not implement before shared tokens and button/card/badge roles are
  approved.
- Keep one shared review-card path unless the story explicitly approves separate
  live/history card builders.
- Verify live session results, history-loaded results, incorrect answers,
  essays, flagged questions, missing answers, and mixed-source breakdown.
- Preserve the exact score data fields from `ScoringService.score_test()`.
- If touching answer rendering, guard essay `None` scores explicitly with
  `is_correct is None`.
- If touching source breakdown, run scoring and mix tests because per-source
  attribution matters for analytics.
- Do not touch `test_taking.py`, `scoring_service.py`, or `db_manager.py` for
  pure visual styling unless a data bug is deliberately in scope.

## Refresh Triggers

- Update this summary if `results_view.py`, `test_taking.py` finish navigation,
  `history_view.py` result navigation, `ScoringService.score_test()`,
  `ScoringService.save_mixed_attempt()`, `DatabaseManager.get_attempt_details()`,
  or the approved visual foundation changes.
