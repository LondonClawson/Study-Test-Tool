# Home Screen Context

## Metadata

- Summary ID: CTX-HOME.
- Summary file: `visual_overhaul_project/01_context/summaries/home_screen_context.md`.
- Created: 2026-06-03.
- Last updated: 2026-06-03.
- Produced by research task: `visual_overhaul_project/02_research_tasks/R-003_home_screen_context.md`.
- Research agent: Codex.
- Source files inspected: `study_test_tool/gui/test_selector.py`,
  `study_test_tool/gui/components/collapsible_group.py`,
  `study_test_tool/gui/components/mode_dialog.py`,
  `study_test_tool/gui/components/mix_test_dialog.py`,
  `study_test_tool/models/test.py`, and targeted service/database method lookup
  for home card data and archive behavior.
- Context summaries read:
  `visual_overhaul_project/01_context/summaries/gui_architecture_summary.md`,
  `visual_overhaul_project/01_context/summaries/current_visual_state_seed.md`,
  `visual_overhaul_project/01_context/summaries/style_inventory.md`.
- Screens/states inspected: static source inspection for home empty state,
  populated active tests, grouped tests, ungrouped tests, archived tests, zero
  question tests, import and PDF batch report paths, mix-test launch path,
  mode-selection dialog, group archive confirmation, export warnings, delete
  confirmation, and home navigation actions.
- Screens/states not inspected: runtime light/dark screenshots, native file
  dialog rendering, native messagebox rendering, minimum window wrapping, and
  actual populated local user data density.

## Purpose

Use this summary for home/test selector visual stories, especially
`STORY-008_home_screen_layout.md` and
`STORY-009_home_test_cards_and_actions.md`. It maps the current structure,
states, visual issues, action hierarchy, and behavior constraints without
redesigning the screen.

## Home Workflow Map

The home screen is `TestSelectorFrame` in `study_test_tool/gui/test_selector.py`.
It is registered as `SCREEN_HOME` by `App` and refreshes data through
`on_show()`, which calls `_refresh_test_list()`.

Main workflows:

- Import: `_on_import()` opens a native file picker for JSON, text, PDF, or DOCX.
  PDF/DOCX paths route through `_import_pdf()`, may ask for a partner file, may
  offer folder batch import, and may show `_show_pdf_folder_report()`.
- Create: `_on_new_test()` navigates to `SCREEN_EDITOR` with `test_id=None`.
- Mix: `_on_mix_test()` filters active tests to those with questions, opens
  `MixTestDialog`, opens `ModeSelectionDialog`, selects mixed questions, then
  navigates to `SCREEN_TEST_TAKING` with `questions` and `mix_test_name`.
- Review missed: `_on_review_missed()` navigates to `SCREEN_REVIEW`.
- History: `_on_view_history()` navigates to `SCREEN_HISTORY`.
- Analytics: `_on_analytics()` navigates to `SCREEN_ANALYTICS`.
- Take test: `_on_take_test(test)` checks for missing correct answers, opens
  `ModeSelectionDialog`, then navigates to `SCREEN_TEST_TAKING`.
- Edit: `_on_edit_test(test)` navigates to `SCREEN_EDITOR` with the test ID.
- Export: `_on_export_test(test)` validates export, may show warnings, opens a
  native save dialog, and writes JSON.
- Archive/unarchive/delete: `_on_archive_test()`, `_on_unarchive_test()`,
  `_on_archive_group()`, and `_on_delete_test()` call `TestService` then refresh
  the list. Delete is permanent and confirms that questions and history are also
  deleted.

## Current Widget Structure

`_build_ui()` creates the static shell:

- Centered page title label: "Study Testing Tool".
- Top action bar `btn_frame`: Import, New Test, Mix Test on the left; Analytics,
  View History, Review Missed on the right.
- Sort toolbar `sort_frame`: "Sort by:" label, `_sort_menu`, and
  `_collapse_all_btn`.
- Scrollable list: `self.test_list_frame`.
- Empty label: `self.empty_label`, packed only when there are no active or
  archived tests.

`_refresh_test_list()` builds dynamic content:

- Preserves group expansion state from `self._group_widgets`.
- Fetches active tests with `test_service.get_all_tests()` and archived tests
  with `test_service.get_archived_tests()`.
- Sorts active tests through `_sort_tests()`.
- Groups active tests by `test.group_name`; named groups are alphabetical and
  "Ungrouped" is last.
- Creates `CollapsibleGroup` per active group. Named groups receive an
  `archive_callback`; "Ungrouped" does not.
- Creates an "Archived Tests" `CollapsibleGroup` when archived tests exist.
- Calls `_create_test_card()` for active tests and `_create_archived_test_card()`
  for archived tests.

`CollapsibleGroup` renders a transparent shell with a transparent header row.
The header is a wide text button containing an arrow, group name, and count.
Named active groups also show an "Archive Group" button. The content frame is
packed or forgotten by `toggle()`.

## Card Data

Active and archived card data comes from the `Test` dataclass and question
count lookup:

- `test.name`.
- `test.description`, falling back to "No description".
- `test.group_name`, when present.
- `test_service.get_question_count(test.id)`.

`_create_test_card()` disables "Take Test" when question count is zero.
Archived cards use the same data and expose only "Unarchive" and "Delete".

## Current Action Hierarchy

Observed hierarchy:

- Global creation/import actions are left aligned, while review/history/analytics
  are right aligned. Their sizes are equal, which makes the top bar read as two
  clusters but not a clear priority sequence.
- "Mix Test" is visually elevated with a unique purple color.
- "Review Missed" is visually elevated with warning orange.
- "Analytics" uses gray while "View History" uses the default primary CTk
  button style.
- On active cards, "Take Test" is first and default primary, but Edit, Export,
  Archive, and Delete have similar size and button treatment. Export is green,
  Archive/Edit are gray variants, and Delete is danger red.
- On archived cards, "Unarchive" is primary and "Delete" is danger.
- Group archive is a gray button in the group header.

Recommended hierarchy for implementation stories:

- Keep "Take Test" as the strongest card action.
- Treat Edit, Export, and Archive as secondary or utility actions; avoid giving
  Export a success/outcome color unless the foundation explicitly reserves green
  for export.
- Keep Delete as danger but visually lower frequency until needed.
- Re-evaluate Mix Test after the foundation: it may need an accent/special role,
  but it should not compete with the primary first-run actions on every state.
- Make Review Missed a caution/review action only if product intent is to
  elevate remediation above history and analytics; otherwise it can be a
  secondary navigation action.
- Give the top action bar a clearer primary action cluster and utility
  navigation cluster without changing command routing.

## Visual Findings

Observed facts:

- Home relies on the default CustomTkinter frame background and blue theme for
  much of its surface.
- The title is centered and isolated; there is no page subtitle, count summary,
  or visual relationship between the title and the action toolbar.
- The action bar and sort toolbar are separate transparent rows with fixed-width
  text buttons.
- The sort control is compact and functional, but the collapse/expand toggle
  state is expressed only by button text.
- Test cards use `CTkFrame(corner_radius=8)` with no explicit border. Padding is
  simple: `padx=15`, `pady=10` inside, `pady=5`, `padx=5` outside.
- Card metadata uses gray text and text separators: `"  |  "`.
- Group headers are wide primary-colored text buttons. They function correctly,
  but read more like large links than section headers.
- Group expansion defaults to collapsed for newly loaded groups because
  `_refresh_test_list()` uses `old_group_states.get(group, False)`.
- Empty state is a single gray label in the scroll frame.
- Archived cards use a tuple muted surface `("#d0d0d0", "#2a2a2a")` and gray
  title text, which may reduce readability in both light and dark modes.
- Current button colors mix shared constants, inline hex values, literal
  `"gray"`, and CustomTkinter default colors.

## Visual Issues By State

Empty state:

- The message is clear but visually plain and does not reinforce the two likely
  next actions: import or create.
- It is only a label inside the scrollable list, so the surrounding page can feel
  unfinished when there is no data.

Populated active state:

- Test cards are readable, but action buttons dominate the right side and all
  actions are similarly dense.
- Long test names or descriptions may crowd the horizontal button cluster at
  smaller widths.
- Metadata hierarchy is weak because description, question count, and group all
  use gray text with similar size and spacing.

Grouped state:

- Grouping behavior is useful and should remain, but group headers need a more
  intentional section pattern. The current toggle button width is fixed at 400,
  which may not adapt gracefully.
- The "Archive Group" action is immediately visible beside every named group,
  giving a bulk-destructive-ish action high presence.

Archived state:

- Archived tests are separated under an "Archived Tests" group, which is a good
  behavioral boundary.
- Archived card styling is dimmed, but the muted title and muted surface could
  make important restore/delete actions harder to scan.

Zero-question state:

- "Take Test" is disabled for zero-question tests. Future visual work must keep
  that disabled state visible and explainable through card metadata or affordance
  only if wording changes are approved.

Dialog-launched state:

- Home launches both CustomTkinter modal dialogs and native dialogs. Visual
  stories can polish `ModeSelectionDialog` and `MixTestDialog`, but native file
  and message dialogs should be treated as behavior constraints for MVP.

## Required Card/List/Group Patterns

Home implementation stories should define or reuse:

- A test-card pattern with stable title, description, metadata, and action
  regions.
- A compact metadata row pattern for question count and group name.
- A disabled primary action style for zero-question tests.
- A utility action pattern for Edit, Export, Archive, and group archive.
- A danger action pattern for Delete.
- An archived card treatment that preserves readability while signaling inactive
  status.
- A section/group header pattern with clear expand/collapse affordance and
  optional trailing group action.
- A designed empty state pattern that can later be shared with history,
  analytics, and review.

## Behavior Constraints

- Preserve `on_show()` refresh behavior and `App.show_frame()` routing.
- Do not move GUI persistence into raw database calls; home should keep using
  `TestService`, `QuestionService`, `ImportService`, `ExportService`, and
  `MixService`.
- Preserve active versus archived data sources:
  `get_all_tests()` and `get_archived_tests()`.
- Preserve active sorting values: "Last Updated", "Name (A-Z)", "Name (Z-A)",
  and "Date Created".
- Preserve named group ordering and "Ungrouped" last.
- Preserve expansion state across refreshes where current code supports it.
- Preserve the disabled Take Test state when `q_count == 0`.
- Preserve missing-answer warning before starting a normal test.
- Preserve mix-test filtering to tests with at least one question.
- Preserve group archive confirmation and delete confirmation wording unless a
  separate product/content decision changes it.
- Preserve native file dialog and messagebox behavior during MVP visual work.

## Risks

- Changing card layout without testing narrow windows may cause long names or the
  right-side action cluster to overlap.
- Replacing gray globally could confuse muted text, disabled-like controls,
  secondary buttons, archive actions, and empty states.
- Styling group headers as non-buttons would break expand/collapse unless the
  click target is preserved.
- Hiding archive/delete too aggressively could make existing workflows harder to
  find. Any move to menus or icon-only controls should include tooltips and
  visible affordances.
- Dialog styling is split: `ModeSelectionDialog` and `MixTestDialog` are
  app-controlled, but messageboxes and file dialogs are native.

## Open Design Questions

- Should Import or New Test be the primary top-level action in an empty home
  state, or should both be equal?
- Should Mix Test remain a special accent action or become a secondary workflow
  action after the home screen is visually organized?
- Should Review Missed stay warning-colored, or should warning be reserved for
  risk/status feedback?
- Should Archive Group remain visible in every group header, move to a lower
  emphasis action, or require a menu pattern that does not yet exist?
- Should archived cards show reduced emphasis only on metadata, or on the whole
  card surface?

## Recommended Story Split

Keep the existing home split:

- `STORY-008_home_screen_layout.md`: page structure, title/header area, top
  action bar grouping, sort toolbar, empty state, scrollable list spacing, and
  group header layout.
- `STORY-009_home_test_cards_and_actions.md`: active card styling, archived card
  styling, card metadata hierarchy, disabled Take Test state, action hierarchy,
  and utility/danger button treatment.

Do not combine these with visual foundation work. Home stories should consume
the shared tokens/button/card decisions once `CTX-FOUNDATION` is ready.

## Dev 2 Quick Start

- Start in `study_test_tool/gui/test_selector.py`; inspect `_build_ui()`,
  `_refresh_test_list()`, `_create_test_card()`, and
  `_create_archived_test_card()`.
- For group work, inspect `study_test_tool/gui/components/collapsible_group.py`,
  especially `_build_header()`, `_make_label()`, and `toggle()`.
- For launched dialog context, inspect `ModeSelectionDialog._build_ui()` and
  `MixTestDialog._build_ui()`, but keep dialog polish separate unless the story
  explicitly includes it.
- Use `style_inventory.md` before changing colors. It identifies current
  button-role conflicts and repeated hover colors.
- Preserve all command callbacks and service calls; visual changes should be
  limited to layout, spacing, typography, colors, and reusable visual helpers.

## Refresh Triggers

- Any change to `study_test_tool/gui/test_selector.py` home layout, card data,
  action set, sorting, grouping, archive behavior, or import/mix launch flow.
- Any change to `CollapsibleGroup` header behavior or group archive placement.
- Any approved foundation decision that changes button roles, card/list
  patterns, empty states, or group header rules.
