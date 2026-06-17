# MVP Acceptance Matrix

Use this matrix during sprint reviews and MVP closeout.

| Area | Acceptance Criteria | Evidence |
| --- | --- | --- |
| App-wide action hierarchy | Primary actions are obvious, secondary and utility actions do not compete, destructive actions are clear but not overemphasized | Completed story handoffs plus `STORY-016` light/dark validation screenshots |
| Layout consistency | Screen margins, section spacing, card padding, and headers follow the approved foundation | `visual_foundation_decisions.md`, completed story handoffs, and `STORY-016` screen-family validation matrix |
| Light/dark mode | Both modes remain readable and status colors keep meaning | `01_context/screenshots/after/STORY-016/` contains 138 validated light/dark screenshots |
| Home | Tests are easy to identify, metadata is scannable, groups and archived tests are distinct, empty state is intentional | `STORY-008`, `STORY-009`, and `STORY-016` Home screenshot evidence |
| Test taking | Question text dominates, answers feel selectable, progress/timer/flag are visible without distraction, practice feedback is calm | `STORY-010`, `STORY-011`, and `STORY-016` Test Taking evidence; long-answer stress remains a closeout classification item |
| Results | Score is immediately understandable, statuses are distinct, user/correct answers are easy to compare, mix breakdown is readable | `STORY-012` and `STORY-016` Results evidence, including `results_minimum_partial_score` |
| Editor | Metadata and question editing areas are organized, question list is scannable, add/update/cancel states are clear | `STORY-013` and `STORY-016` Editor evidence; long editor content remains a closeout classification item |
| History | Rows feel like a polished data list, filters are usable, empty/loading states are intentional | `STORY-014A` and `STORY-016` History evidence; long test names remain a closeout classification item |
| Analytics | Charts match app theme, weak-topic cards are scannable, no-data state is intentional | `STORY-014B`, `STORY-014C`, and `STORY-016` Analytics evidence; single-day Study Activity wide-bar presentation is a post-MVP candidate |
| Review and dialogs | Review selection is clear, dialogs have hierarchy, confirmation/error states remain understandable | `STORY-015A` through `STORY-015E` and `STORY-016` Review/dialog evidence; native dialogs are accepted MVP exceptions |
| Behavior preservation | Core workflows, scoring, import/export, database, and test sessions are unchanged | Story handoff verification notes; final test summary remains in scope for `STORY-017` |

## STORY-017 Closeout Review Notes

Dev 2 reviewed this matrix on 2026-06-17 for
`STORY-017_mvp_visual_regression_pass.md`.

| Area | Closeout Classification | Notes |
| --- | --- | --- |
| App-wide action hierarchy | Pass | Accepted story handoffs plus the `STORY-016` light/dark validation set show the visual foundation applied across primary, secondary, warning, danger, special, and disabled actions. No open MVP blocker found. |
| Layout consistency | Pass | Baseline screenshots validate the before state, and `STORY-016` validates the accepted after state across every harness-supported MVP screen family. Minimum-window evidence exists where practical for main screens. |
| Light/dark mode | Pass | Baseline folder validates 42 light/dark before screenshots; `after/STORY-016/` validates 138 light/dark after screenshots. No unreadable contrast blocker was found in the accepted evidence. |
| Home | Pass with post-MVP stress follow-up | `STORY-008`, `STORY-009`, and `STORY-016` cover populated, empty, expanded, archived, and minimum states. Extreme long test names, descriptions, and group names remain post-MVP stress-fixture coverage. |
| Test taking | Pass with post-MVP stress follow-up | `STORY-010`, `STORY-011`, and `STORY-016` cover shell, answer rows, practice feedback, essay, review, mix, and minimum states. Very long answer/question text remains post-MVP stress-fixture coverage. |
| Results | Pass with post-MVP stress follow-up | `STORY-012` retake-state fix was accepted, and `STORY-016` adds minimum Results evidence. Long answer/essay comparison content remains post-MVP stress-fixture coverage. |
| Editor | Pass with post-MVP stress follow-up | `STORY-013` minimum evidence contamination was fixed and accepted. Long prompts, long option text, and long group names remain post-MVP stress-fixture coverage. |
| History | Pass with accepted non-visual follow-up | `STORY-014A` and `STORY-016` cover populated, filtered, loading, empty, and minimum states. Long History test names remain post-MVP stress-fixture coverage. The pre-existing History loading exception callback issue is non-visual and not introduced by this overhaul. |
| Analytics | Pass with post-MVP chart follow-up | `STORY-014B`, `STORY-014C`, and `STORY-016` cover chart shell, Weak Topics, no-data, and minimum states. The single-day Study Activity wide bar is readable but visually heavy; classify as post-MVP chart-readability work. |
| Review and dialogs | Pass with accepted MVP exceptions | `STORY-015A` through `STORY-015D` cover custom Review, Mode, Mix, and Import Preview states. `STORY-015E` accepted native messageboxes and file dialogs as deliberate MVP exceptions. Larger source lists and long dialog row names remain post-MVP stress-fixture coverage. |
| Behavior preservation | Pass | Full closeout run passed: `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests` returned 231 passed with 13 existing collection warnings. Story-level handoffs/reviews also document focused GUI smokes, screenshot validation, and service tests for touched workflows. |

Final closeout classification:

- MVP blockers: none found in the accepted evidence, screenshot validation, or
  full pytest run.
- Post-MVP follow-ups: long-content stress screenshot fixtures across Home, Test
  Taking, Results, Editor, History, Analytics Weak Topics, Review, Mix dialog,
  and Import Preview; Analytics Study Activity one-day bar readability.
- Accepted MVP limitations: native messageboxes and file dialogs remain native;
  custom dialogs were validated as fixed-size modals rather than separate
  minimum-host states; seeded screenshot data is representative but not
  exhaustive for arbitrary user-authored content.
