# Editor Context Summary

## Metadata

- Summary ID: CTX-EDITOR
- Summary file: `visual_overhaul_project/01_context/summaries/editor_context.md`
- Created: 2026-06-03
- Last updated: 2026-06-03
- Produced by research task: `visual_overhaul_project/02_research_tasks/R-006_editor_context.md`
- Research agent: Codex
- Source files inspected: `study_test_tool/gui/test_editor.py`, `study_test_tool/gui/components/autocomplete_entry.py`, `study_test_tool/services/test_service.py`, `study_test_tool/services/question_service.py`, `study_test_tool/tests/test_group_sort.py`, `visual_overhaul_project/01_context/summaries/gui_architecture_summary.md`, `visual_overhaul_project/01_context/summaries/current_visual_state_seed.md`, `visual_overhaul_project/01_context/summaries/style_inventory.md`, `VISUAL_OVERHAUL_PLAN.md`
- Screens/states inspected: static source inspection for new test, edit existing test, unsaved metadata, no questions, populated question list, add multiple-choice question, add essay question, edit question, cancel edit, dirty-form confirmation, option add/remove, disabled option removal at two options, validation warnings, essay missing-answer warning, question delete confirmation, group autocomplete dropdown
- Screens/states not inspected: runtime light/dark screenshots, minimum-window rendering, keyboard traversal, native messagebox rendering, long question/option text at runtime, live autocomplete overlay z-order against all macOS window states

## Purpose

Use this summary before editor visual work, especially `STORY-013_editor_layout.md`.
It narrows the relevant code paths and states for polishing the editor metadata
area, question list, add/edit form, option rows, essay expected-answer field, and
save/cancel action hierarchy without changing editor behavior.

## Current Structure

`TestEditorFrame` in `study_test_tool/gui/test_editor.py` owns the full editor
screen. It is instantiated once by the main app and refreshed through
`on_show(test_id=None, **kwargs)`.

The layout has three main regions:

- Top bar: transparent frame with a gray `< Back` button and `title_label`.
- Metadata block: transparent grid with test name, description, group
  autocomplete, and a green `Save Test` button spanning the three metadata rows.
- Main content: two equal-width columns. The left column is a framed question
  list with a `CTkScrollableFrame`; the right column is a framed scrollable
  add/edit question form.

The question form contains:

- `question_text` textbox.
- `type_selector` segmented button with Multiple Choice and Essay values.
- Optional category entry.
- Multiple-choice `options_frame`, containing radio buttons, option entries,
  per-row remove buttons, and a gray `+ Add Option` button.
- Essay `essay_frame`, hidden until Essay is selected.
- Main add/update button and hidden gray `Cancel Edit` button.

`AutocompleteEntry` wraps a `CTkEntry` and creates an overlay dropdown on the
toplevel window. It mirrors `get`, `delete`, `insert`, `configure`, and
`set_values`, so editor code treats it like an entry.

The editor calls `TestService` for test metadata and group names. It calls
`QuestionService` for question list loading, add, update, and delete. Visual
work should keep this service boundary intact.

## Important UI States

- New test: `on_show(test_id=None)` clears metadata, sets title to `New Test`,
  resets the question form, and shows `No questions yet.` because `_test_id` is
  `None`.
- Unsaved new test with question attempt: `_on_add_question` blocks with the
  `Save First` warning until `_on_save_test` creates the test.
- Edit existing test: `on_show(test_id=...)` loads name, description, group,
  title `Edit Test`, resets the form, and refreshes existing questions.
- No questions: `no_questions_label` is packed into the question list for new or
  empty saved tests.
- Populated question list: each question is rendered by `_create_question_card`
  with truncated text, type metadata, optional no-answer warning, Edit, and Del.
- Add multiple-choice question: default state uses four option rows, a selected
  correct radio index of zero, and requires at least two non-empty options.
- Option add/remove: add rebuilds rows from current text; remove rebuilds rows,
  adjusts correct selection, and disables remove buttons when only two rows
  remain.
- Add essay question: selecting Essay hides MC options and shows expected answer.
  Empty expected answer triggers a warning but still saves after the warning.
- Edit question: `_on_edit_question` checks dirty form state, populates fields,
  changes form title to `Edit Question`, changes main button to
  `Update Question`, and shows `Cancel Edit`.
- Cancel edit: `_cancel_edit` resets the form to Add Question state.
- Dirty form navigation: `_on_back` asks before discarding unsaved question form
  changes, then returns to `SCREEN_HOME`.
- Delete question: `_on_delete_question` confirms with a native messagebox and
  refreshes the list after deletion.
- Group autocomplete: `on_show` refreshes suggestion values from
  `test_service.get_group_names()`.

## Workflow Map

- Home navigates to the editor through `App.show_frame(SCREEN_EDITOR, test_id=...)`.
- `on_show` is the screen reset point. It must keep resetting `_test_id`,
  `_editing_question_id`, form state, metadata fields, group suggestions, and
  the question list.
- Saving metadata uses `_on_save_test`. It validates required test name, creates
  a new test when `_test_id` is `None`, or updates the existing `Test`.
- Adding/updating questions uses `_on_add_question`. It validates saved test
  state, question text, MC option count, and selected correct option text.
- The MC option rows are index-sensitive. `_rebuild_option_rows`,
  `correct_var`, `option_entries`, `_option_rows`, `_option_radios`, and
  `_option_remove_btns` must stay in lockstep.
- Editing a question is stateful through `_editing_question_id`; successful
  update clears that state and hides Cancel Edit.
- `_get_form_snapshot` and `_form_is_dirty` protect against losing unsaved
  question edits. Visual work must not omit fields from the snapshot.
- Question deletion and validation feedback rely on native messageboxes; visual
  polish cannot fully style those dialogs without a separate dialog story.

## Visual Findings

The editor already has a useful functional skeleton, but it reads as default
CustomTkinter because hierarchy and semantic roles are mostly encoded through
position and a few inline colors.

- The top bar uses a small gray text button for Back and a large title. It does
  not yet match any shared page-header pattern.
- Metadata labels are left-column grid labels with fixed-width entries. The
  green Save Test button has strong visual weight but sits beside all fields,
  which makes the metadata section feel more like a form utility area than a
  clear save checkpoint.
- The divider is a plain gray `CTkFrame`, separate from any future border token.
- Main content uses two equal columns. This supports dense editing, but at small
  widths both columns can compete for space, and no minimum-size behavior has
  been verified.
- Left and right columns are framed panels, but section padding is shallow and
  titles are centered. The visual relationship between list and form is
  functional rather than strongly organized.
- Question cards use `corner_radius=6`, compact vertical spacing, small text,
  and side-by-side Edit/Del actions. The card content is scannable for short
  questions, but long text is manually truncated before wrapping, so visual
  changes should test long prompts.
- The no-answer warning uses a warning icon character and inline warning color.
  It is useful, but should eventually align with shared warning treatment.
- Edit buttons are gray and Del buttons are red. Both are visible on every card;
  destructive actions may need lower emphasis while remaining easy to find.
- The form has many labels, text fields, and controls in one scrollable stack.
  It is dense and efficient but lacks grouping between question text, type,
  category, answer data, and final actions.
- Multiple-choice option rows are transparent frames with an unlabeled radio,
  expanding entry, and small remove button. The remove button already uses
  light/dark tuple colors, but it is visually custom and not tied to shared
  utility-button styling.
- The `+ Add Option` and `Cancel Edit` buttons are gray; Add/Update Question
  inherits the default CustomTkinter primary style. The primary action changes
  text correctly, but the edit mode could be more visually explicit.
- Essay expected answer appears as a plain textbox under a hidden frame. There
  is no helper text clarifying that an empty expected answer is allowed but
  warned.
- Empty state is a muted gray label with no shared empty-state treatment.
- `AutocompleteEntry` places its dropdown as a toplevel overlay with a frame and
  transparent buttons. It may need tokenized surface, border, hover, and z-order
  checks if the metadata region is restyled.

## Recommendations For Implementation Stories

- Keep `STORY-013` as one editor-focused implementation story after
  CTX-FOUNDATION is Ready. It is cohesive enough if limited to editor surfaces
  and `AutocompleteEntry` styling.
- Introduce a consistent page-header treatment for Back plus title only if
  `STORY-007_page_header_pattern.md` or CTX-FOUNDATION has already defined the
  pattern. Otherwise keep editor header changes local and conservative.
- Treat the metadata block as a compact test-details panel: align labels,
  preserve fixed editing efficiency, and make Save Test the clear primary action
  for metadata without confusing it with Add/Update Question.
- Preserve the two-column desktop editing model, but add responsive constraints
  or minimum-width checks so the question list and form do not become cramped at
  the app minimum size.
- Standardize question cards with the future card/list pattern: consistent
  padding, muted metadata, warning treatment, and utility/destructive action
  roles.
- Group the form visually into question prompt, type/category, answer content,
  and form actions. Avoid adding extra workflow steps.
- Make edit mode visible through the form title, Update Question primary action,
  and Cancel Edit secondary action. Do not introduce a modal edit flow.
- Style option rows as stable list rows while preserving radio-index behavior
  and remove-button disabled state.
- Keep essay expected answer visually subordinate to question text but clearly
  part of answer data.
- If implementation touches autocomplete, style the dropdown through semantic
  surface/hover tokens and smoke check overlay placement.

## Behavior Constraints

- Do not change the need to save a test before adding questions.
- Do not change validation rules for test name, question text, multiple-choice
  option count, selected correct option text, or essay expected-answer warning.
- Do not change question ordering or the way question cards enumerate `Q1`,
  `Q2`, etc. from the service-returned list.
- Do not change MC option order, correct radio index behavior, or the two-option
  minimum for remove buttons.
- Do not change `QuestionService.update_question` replacement semantics for
  options.
- Do not bypass `TestService` or `QuestionService`.
- Do not change group persistence, distinct group suggestions, or empty group
  handling.
- Do not remove dirty-form confirmation before editing another question or
  navigating back.
- Do not convert native messageboxes as part of editor layout work unless a
  dialog-specific story explicitly approves it.

## Implementation Risks

- `AutocompleteEntry.configure` forwards to the inner entry, so styling the
  wrapper frame alone may not affect the visible entry.
- `AutocompleteEntry` globally unbinds `Button-1` on the toplevel when closing
  the dropdown. Do not add competing global click bindings without testing.
- Option rows are rebuilt on every add/remove. Any per-row visual state must be
  rebuilt consistently.
- The correct radio value uses row indexes, but empty option rows are skipped
  during save. A visual change that hides, reorders, or filters rows could break
  correct-answer validation.
- Long question text is manually truncated to 80 characters before label wrap.
  Card redesign may need runtime checks for long text rather than relying on the
  current truncation.
- The editor has nested scrollable frames only in the main columns, not the
  whole page. Changing pack/grid relationships can create clipping or scrolling
  conflicts.
- Native messageboxes interrupt the flow. Visual smoke checks should account for
  warning and confirmation dialogs even if they are not restyled.

## Open Questions

- Should Save Test remain a metadata-only action, or should future copy make
  that distinction clearer from Add/Update Question?
- Should destructive question deletion stay visible on every question card, or
  move to a quieter utility position under the card/list pattern?
- Should the editor eventually support a single-column layout at narrow widths,
  or is the macOS desktop minimum size expected to preserve two columns?
- Should empty essay expected answers continue to show only a native warning, or
  should the form include a persistent helper/warning treatment after the visual
  foundation is available?

## Dev 2 Quick Start

- Start in `study_test_tool/gui/test_editor.py`; the relevant methods are
  `_build_ui`, `on_show`, `_refresh_question_list`, `_create_question_card`,
  `_on_type_change`, `_rebuild_option_rows`, `_update_remove_button_state`,
  `_on_save_test`, `_on_add_question`, `_on_edit_question`, `_reset_form`, and
  `_on_back`.
- Read CTX-FOUNDATION before choosing colors, spacing, button roles, card
  treatment, or border/radius values.
- Keep the existing top metadata plus two-column content structure unless a
  foundation or layout story explicitly changes that pattern.
- Verify new test, saved empty test, existing populated test, MC add, essay add,
  edit existing question, cancel edit, delete confirmation, validation warnings,
  option add/remove, and group autocomplete.
- Preserve `_editing_question_id` and `_clean_snapshot` behavior while moving or
  restyling controls.
- When styling option rows, keep `option_entries`, `_option_rows`,
  `_option_radios`, `_option_remove_btns`, and `correct_var` in row order.
- If `AutocompleteEntry` is styled, check dropdown placement, hover colors,
  click outside dismissal, Escape dismissal, and suggestion selection.
- Run `pytest --rootdir=. study_test_tool/tests/test_group_sort.py` if group
  behavior or autocomplete-adjacent metadata code changes.
- Run an editor smoke check in light and dark mode because no runtime
  screenshots were captured for this research task.

## Refresh Triggers

Update this summary if `test_editor.py`, `AutocompleteEntry`, group-name
behavior, question validation, option-row behavior, editor navigation, shared
visual tokens, page-header patterns, card/list patterns, or dialog strategy
changes.
