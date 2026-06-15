# Test-Taking Context

## Metadata

- Summary ID: CTX-TEST-TAKING
- Summary file: `visual_overhaul_project/01_context/summaries/test_taking_context.md`
- Created: 2026-06-03
- Last updated: 2026-06-03
- Produced by research task: `visual_overhaul_project/02_research_tasks/R-004_test_taking_context.md`
- Research agent: Codex
- Source files inspected: `VISUAL_OVERHAUL_PLAN.md`, `visual_overhaul_project/01_context/summaries/gui_architecture_summary.md`, `visual_overhaul_project/01_context/summaries/current_visual_state_seed.md`, `visual_overhaul_project/01_context/summaries/style_inventory.md`, `study_test_tool/config/settings.py`, `study_test_tool/gui/test_taking.py`, `study_test_tool/gui/components/question_widget.py`, `study_test_tool/gui/components/progress_bar.py`, `study_test_tool/gui/components/timer_widget.py`, `study_test_tool/services/test_session.py`, `study_test_tool/tests/test_practice_mode.py`, `study_test_tool/tests/test_test_session.py`
- Screens/states inspected: static source inspection for normal test mode, practice mode, review session, mix test, first question, middle question, last question, flagged question, answered question, unanswered question, checked practice response, multiple-choice response, essay response, correct feedback, incorrect feedback, essay feedback, finish confirmation path, progress-click navigation path
- Screens/states not inspected: runtime light-mode screenshots, runtime dark-mode screenshots, minimum-window manual resize, populated local user data, native messagebox rendering, very long test title, very long question text, very large question count, keyboard-only interaction

## Purpose

Use this summary before implementing test-taking visual stories. It narrows the
current code structure, states, behavior constraints, and visual risks for
`STORY-010_test_taking_shell.md` and
`STORY-011_answer_rows_and_practice_feedback.md`.

## Current Structure

`study_test_tool/gui/test_taking.py` defines `TestTakingFrame`, a
CustomTkinter frame registered by `App.show_frame(...)`. The frame owns the
screen shell, session lifecycle, navigation callbacks, practice feedback, finish
confirmation, scoring handoff, and results navigation.

The shell is built once in `_build_ui()`:

- Top transparent frame with test title on the left, then timer, progress text,
  and flag button packed from the right.
- Center `CTkScrollableFrame` named `question_area`.
- Bottom transparent frame with Previous, Next, optional Check Answer, Finish,
  and a progress bar container.

`on_show(...)` creates a fresh `TestSession` for one of three entry paths:

- Normal test: load one test by `test_id`, randomize questions, show test name.
- Review session: load selected question IDs through `ReviewService`, show
  `Review Session`.
- Mix test: use the provided questions and optional mix name, set `test_id` to
  `None`, and save through the mixed-attempt path on finish.

`QuestionWidget` is rebuilt for each displayed question. Multiple-choice
questions use a radio button plus a separate clickable label per option. Essay
questions use a label and `CTkTextbox`. The widget exposes `get_answer()`,
`set_answer(...)`, and `disable()`; `TestTakingFrame` depends on those methods
for response saving and practice locking.

`ProgressBar` is rebuilt once per session and then recolored on each displayed
question. Its indicators are `CTkButton` widgets, not passive badges, and each
button calls back into `_on_progress_click(index)`.

`TimerWidget` is a `CTkLabel` wrapper around `utils.timer.Timer`. It starts when
the session starts and stops during finish before scoring is saved.

## Important UI States

- Normal test mode: Check Answer is hidden, Finish text is `Finish Test`, and
  final scoring saves one attempt for `session.test_id`.
- Practice mode: Check Answer is packed on the right, Finish text is
  `Finish Practice`, and checked responses are locked.
- Review session: title is `Review Session`, question set is loaded from
  `ReviewService`, and normal attempt saving is used unless it is also a mix
  test.
- Mix test: title is mix name or `Mix Test`, `TestSession.test_id` is `None`,
  and finish uses `save_mixed_attempt(...)` before showing results with
  `attempt_id=None`.
- First question: Previous button is disabled.
- Middle question: Previous and Next are enabled.
- Last question: Next button is disabled.
- Flagged question: flag button text becomes `Unflag`, button color uses
  `COLOR_FLAGGED`, and progress indicator uses flagged color unless the question
  is current.
- Answered question: response exists in `session.responses`; progress indicator
  uses answered color when the question is not current or flagged.
- Unanswered question: no saved response; progress indicator uses unanswered
  color when the question is not current or flagged.
- Checked practice response: answer is restored from
  `session.checked_responses`, input is disabled, feedback is re-rendered, and
  Check Answer is disabled.
- Essay response: `QuestionWidget.get_answer()` returns stripped textbox text
  or `None`; scoring feedback can return `None`, which shows expected-answer
  comparison instead of correct/incorrect status.

## Workflow Map

- Starting a test calls `on_show(...)`, creates a `TestSession`, calls
  `session.start()`, rebuilds the progress bar, starts the timer, and displays
  the first question.
- Displaying a question updates progress text, flag button, Previous/Next
  state, destroys all existing widgets in `question_area`, rebuilds
  `QuestionWidget`, scrolls to top, restores saved response, optionally
  reapplies practice lock and feedback, then updates progress colors.
- Previous, Next, progress-button click, and Finish all call
  `_save_current_answer()` before moving on or completing the test.
- `_save_current_answer()` reads the current `QuestionWidget` and calls
  `TestSession.save_response(question.id, answer or "")`; empty answers remove
  existing responses.
- Check Answer saves the current answer, stores the first checked response with
  `save_checked_response(...)`, scores the current question, shows feedback,
  disables the answer widget, and disables the Check Answer button.
- Flag toggles `session.flagged` for the current question, updates the flag
  button, and refreshes progress colors.
- Finish saves the current answer, calculates unanswered and flagged counts,
  asks for confirmation, stops the timer, records final question time, scores
  the session, saves either normal or mixed attempts, and navigates to results.

## Visual Findings

Observed facts:

- The test title uses title size and bold weight in the top bar. Timer uses
  heading size. Progress text uses body size.
- Top bar items are packed left/right in one horizontal row. Long titles may
  compete with the flag, progress, and timer controls because no truncation or
  wrapping strategy is defined.
- The question area is a scrollable frame with `padx=30`, `pady=10`. Each
  question widget is a full frame packed to fill available space.
- The question text uses body size, `wraplength=600`, and left alignment. It
  does not currently receive heading treatment, larger line spacing, or a
  distinct question panel title style.
- Multiple-choice options are loose transparent rows containing a small radio
  button and a clickable label. Only the label has `cursor="hand2"`; the row
  itself is not clickable.
- Option labels use `wraplength=550`. Visual row selection is handled only by
  the radio button state.
- Essay input is a plain `CTkTextbox` with height 120 and no custom visual state.
- Previous and Next are default themed buttons with equal size. Check Answer is
  green using inline success colors. Finish is red using inline danger colors.
- The visual plan notes Finish should be reconsidered as end-of-flow hierarchy,
  not automatically treated like destructive danger.
- The flag inactive state uses literal `"gray"`; flagged state uses
  `COLOR_FLAGGED`.
- Practice feedback is a rounded `CTkFrame` under the question widget with
  status text. Correct uses `COLOR_CORRECT`; incorrect uses `COLOR_INCORRECT`
  and shows correct answer in `COLOR_CORRECT`; essay uses gray text and expected
  answer copy.
- The progress bar uses compact numbered buttons with width 32, height 28,
  radius 4, `("Helvetica", 11)`, and one-pixel horizontal spacing.
- Progress color priority is current first, then flagged, answered, unanswered.
  A flagged current question appears current, not warning-colored.

## Recommendations For Implementation Stories

- Split shell work and answer/feedback work exactly as the existing stories do.
  `STORY-010` should avoid answer row internals except where container spacing
  affects the shell. `STORY-011` should avoid top and bottom shell layout except
  feedback placement.
- For shell work, focus on a clearer top information layout, question area
  framing, button hierarchy, and progress placement. Keep the progress
  indicators as clickable buttons.
- For answer-row work, consider making each multiple-choice option a stable
  full-width selectable row that controls the same `StringVar`. Preserve label
  click behavior or replace it with equivalent row click behavior.
- Practice feedback should become visually distinct but calm. Keep three
  feedback categories: correct, incorrect with correct answer, and essay with
  expected answer.
- Keep `QuestionWidget.get_answer()`, `set_answer(...)`, and `disable()` as the
  integration points unless a story explicitly updates `TestTakingFrame` in
  lockstep.
- Add tokenized styles only after CTX-FOUNDATION is Ready. Until then, avoid
  choosing new semantic colors in the screen-specific stories.
- If progress indicator styling changes, preserve status priority or document a
  product decision to change it.
- Manual verification should include a short test, a long question, practice
  checked feedback, a flagged question, and jumping through progress buttons.

## Behavior Constraints

- Do not change `App.show_frame(...)` routing or the `on_show(...)` argument
  contract.
- Do not remove `_save_current_answer()` calls before Previous, Next,
  progress-click, or Finish.
- Do not change `TestSession.save_response(...)` empty-answer removal behavior.
- Do not change `TestSession.save_checked_response(...)` first-write-wins
  behavior.
- Do not change final scoring preference for checked responses through
  `TestSession.get_scoring_responses()`.
- Do not change question randomization in normal test mode.
- Do not change review question loading through `ReviewService`.
- Do not change mixed-attempt save routing or the `attempt_id=None` results
  handoff for mix tests.
- Do not change essay scoring semantics; essay feedback and scoring can be
  `None`.
- Do not change timer start/stop behavior or question-time recording during
  navigation.
- Do not replace progress buttons with non-clickable elements.

## Implementation Risks

- Rebuilding `question_area` destroys both the current question widget and any
  feedback frame. New visual child widgets must be recreated in `_display_question()`
  or they will disappear on navigation.
- Practice mode relies on disabling rebuilt widgets after navigating back to a
  checked question. Styling selected/disabled rows must work after
  `set_answer(...)` followed by `disable()`.
- Full-row multiple-choice selection can accidentally desynchronize from
  `_answer_var` if the radio button, label, and row callbacks are not kept
  equivalent.
- Progress indicators are behavior-bearing buttons. Styling them as passive
  status chips would break navigation.
- Current progress color overrides flagged color. Changing this can alter how
  flagged current questions are interpreted.
- Long option labels and question text use fixed wraplength values. Font or
  padding changes can cause awkward wrapping at the 800x600 minimum window.
- Finish styling is a design decision because current code treats it as danger
  while the visual plan suggests normal completion should not look destructive.
- Native finish confirmation cannot be visually aligned with CustomTkinter
  tokens without replacing `messagebox`, which is outside these stories.

## Open Questions

- Should Finish become a primary/confirming action, or remain danger-colored
  because it ends the active session?
- Should flagged current questions show the current color, flagged color, or a
  combined treatment in the progress bar?
- Should Check Answer be classified as success, primary, or practice-specific
  under the future foundation tokens?
- Should very large tests keep one horizontal row of progress buttons, wrap
  indicators, or move to a compact secondary navigation pattern?
- Should answer rows show correct/incorrect row-level highlights after checking,
  or should feedback remain below the question only?

## Dev 2 Quick Start

- Start in `study_test_tool/gui/test_taking.py`; `_build_ui()` owns the shell,
  `on_show(...)` owns entry paths, `_display_question()` owns per-question
  rebuilds, and `_show_feedback(...)` owns practice feedback.
- For shell story work, touch `test_taking.py`, `progress_bar.py`, and
  `timer_widget.py`; keep `question_widget.py` largely unchanged.
- For answer-row and feedback work, touch `question_widget.py` and the feedback
  methods in `test_taking.py`; preserve `get_answer()`, `set_answer(...)`, and
  `disable()` behavior.
- Verify first, middle, and last question navigation because Previous/Next
  disabled state is set in `_display_question()`.
- Verify progress click navigation because each progress indicator must remain
  a clickable control.
- Verify practice mode by selecting an answer, clicking Check Answer,
  navigating away and back, and confirming the checked answer is still disabled.
- Verify essay practice feedback because `is_correct is None` uses a separate
  feedback branch.
- Run `pytest --rootdir=. study_test_tool/tests/test_test_session.py` after any
  session, navigation, response, flag, timing, or progress behavior changes.
- Run `pytest --rootdir=. study_test_tool/tests/test_practice_mode.py` after
  any practice, checked-response, or scoring-handoff changes.

## Refresh Triggers

- Update this summary when `test_taking.py`, `question_widget.py`,
  `progress_bar.py`, `timer_widget.py`, or `test_session.py` changes.
- Update after CTX-FOUNDATION defines button roles, status colors, card/list
  rules, or typography tokens that apply to test-taking.
- Update after runtime light/dark screenshots or minimum-size validation reveal
  issues not covered by static inspection.
- Update if review-session, mix-test, scoring, or practice-mode behavior changes.
