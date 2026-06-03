# Component And Style Inventory

## Metadata

- Summary ID: CTX-STYLE-INVENTORY
- Summary file: `visual_overhaul_project/01_context/summaries/style_inventory.md`
- Created: 2026-06-02
- Last updated: 2026-06-02
- Produced by research task: `visual_overhaul_project/02_research_tasks/R-002_component_style_inventory.md`
- Research agent: Codex
- Source files inspected: `study_test_tool/config/settings.py`, `study_test_tool/utils/constants.py`, all files under `study_test_tool/gui/`
- Screens/states inspected: static source inspection for home/test selector, editor, test-taking, results, history, review, analytics, mode dialog, mix dialog, progress bar, timer, graph widget, autocomplete entry, question widget, and collapsible group
- Screens/states not inspected: runtime light/dark screenshots, populated local user data states, file dialog appearance, native messagebox rendering, minimum-window layout

## Purpose

This summary inventories current visual constants, inline styling, repeated
component structures, and style duplication for the visual foundation stories.
`STORY-003_visual_foundation_spec.md`, shared component stories, and screen
polish stories should use this before introducing tokens or reusable helpers.

## Current Structure

The app uses CustomTkinter frames for each screen and small reusable components
under `study_test_tool/gui/components/`.

- Screen frames: `test_selector.py`, `test_editor.py`, `test_taking.py`,
  `results_view.py`, `history_view.py`, `review_view.py`, and
  `analytics_view.py`.
- Reusable components: `collapsible_group.py`, `autocomplete_entry.py`,
  `progress_bar.py`, `question_widget.py`, `timer_widget.py`,
  `graph_widget.py`, `mode_dialog.py`, and `mix_test_dialog.py`.
- Shared constants currently live in `config/settings.py`: app/window sizes,
  core semantic colors, topic health colors, font family, font sizes, question
  type strings, and weak topic threshold.
- Screen names, test modes, and file dialog types live in `utils/constants.py`;
  it has no visual constants.
- `main_window.py` sets `ctk.set_appearance_mode("System")` and
  `ctk.set_default_color_theme("blue")`, so unstyled CTk widgets inherit the
  CustomTkinter blue theme and system light/dark behavior.

## Important UI States

- Home/test selector: no tests empty state, active tests grouped by group name,
  ungrouped tests, archived tests, empty tests with disabled Take Test, import
  success/failure reports, group archive confirmation, delete/export warnings.
- Editor: new test, edit test, no questions, multiple-choice form, essay form,
  editing existing question, missing answer warning, option remove buttons
  disabled when only two options remain.
- Test-taking: test mode, practice mode, mix test, review session, flagged
  question, unanswered question, answered question, current question, disabled
  previous/next, practice feedback for correct/incorrect/essay, locked checked
  response, finish confirmation with unanswered and flagged counts.
- Results: just-completed session, history attempt, mix test source breakdown,
  correct/incorrect/essay statuses, flagged review cards, no result found.
- History: loading state, empty history, populated table rows, row click to
  results, test and mode filters.
- Review: no active tests, no missed questions, selected scope summary,
  grouped scope selector, all missed/frequently missed tabs, selected count,
  start review with selected or all visible questions.
- Analytics: no data, score trends, test comparison, study activity, weak topics
  by test/group/category, category-empty message, light/dark chart themes.
- Dialogs: mode selection, mix test selection, native messageboxes, native file
  dialogs.

## Workflow Map

- `App.show_frame(name, **kwargs)` raises screens and calls `on_show`, so visual
  changes must preserve screen initialization and refresh behavior.
- Home screen actions navigate to editor, test-taking, history, review, and
  analytics, or open import/export/mix/mode dialogs.
- Test cards call services to count questions; disabled Take Test depends on a
  zero question count.
- Editor metadata, question list, and add/edit form share one screen; visual
  changes must preserve `_editing_question_id`, dirty-form confirmation, and
  multiple-choice row order.
- Test-taking saves the current answer before navigation, progress clicks, and
  finish; practice mode locks the first checked response and disables the answer
  widget.
- Results can render from an in-memory session or a stored attempt; retake must
  preserve regular versus mix-test routing.
- Review and mix dialogs both use grouped test checkbox logic; group checkbox
  visual changes must preserve parent/child selection synchronization.
- Analytics reuses a single graph widget and swaps visible content with
  `pack_forget`; graph color changes must refresh on draw.

## Visual Findings

Observed facts:

- `config/settings.py` defines core colors: primary `#1f6aa5`, success
  `#2fa572`, danger `#d9534f`, warning `#f0ad4e`, unanswered `#6c757d`,
  current `#2fa572`, correct `#2fa572`, incorrect `#d9534f`, and topic weak,
  moderate, strong colors.
- `config/settings.py` defines font family `Helvetica` and title, heading, body,
  and small sizes. A few components bypass these with literal font sizes:
  progress buttons use `("Helvetica", 11)`, editor metadata uses size `11`, and
  mode dialog uses `FONT_SIZE_BODY - 2`.
- Many screens use `fg_color="transparent"` for top bars, action bars, metadata
  rows, and inner row containers. This is consistent, but it is repeated inline.
- `"gray"` is the most common inline visual token. It is used for back buttons,
  secondary buttons, muted labels, separators, flag buttons, essay status, empty
  states, and loading states. These roles are not semantically separated.
- Secondary button gray is sometimes `"gray"` and sometimes `#6c757d` with
  hover `#5a6268`.
- Danger hover `#c9302c` appears in home, editor, and test-taking while danger
  base color is a shared constant.
- Success base color appears as both `COLOR_SUCCESS` and inline `#2fa572`;
  hover `#258a5e` is repeated in test-taking, review, and mode dialog.
- Warning base color appears as `COLOR_WARNING`, `COLOR_FLAGGED`, and inline
  `#f0ad4e`; warning hover `#d9972d` is inline on the home screen.
- Mix Test has a unique purple action color `#7b2d8e` and hover `#5e2270`.
  No current constant expresses special/compound test actions.
- Home archived cards use tuple colors `("#d0d0d0", "#2a2a2a")`.
- Autocomplete dropdown and option remove buttons use tuple grays such as
  `("gray10", "gray90")`, `("gray80", "gray30")`, and
  `("gray20", "gray80")`.
- GraphWidget owns chart theme colors separately from `config/settings.py`:
  dark background `#2b2b2b`, text `#ffffff`, grid `#404040`, line/bar
  `#4a9eff`; light background `#ffffff`, text `#333333`, grid `#e0e0e0`,
  line/bar `#1f6aa5`.
- Cards use `corner_radius=8` on home cards, archived cards, analytics topic
  cards, results sections/cards, review cards, and practice feedback. Editor
  question cards use `corner_radius=6`; history table rows use
  `corner_radius=4`; autocomplete dropdown uses `corner_radius=4`; progress
  buttons use `corner_radius=4`.
- Borders are effectively absent in current screen code. No common
  `border_color` or `border_width` usage was found in GUI source.
- Page headers repeat a top transparent frame with a back button and title on
  editor, test-taking, history, review, and analytics. Results uses a centered
  score header without a back button; home uses a centered app title.
- Action bars repeat horizontal transparent frames with CTkButton children. The
  visual priority of actions is inconsistent: primary, navigation, secondary,
  warning, danger, and utility actions often share similar size and placement.
- Empty states are plain muted CTkLabels packed into the relevant scroll frame
  or content frame. They have different strings and padding but no shared visual
  pattern.
- List/card structures repeat: home test cards, archived test cards, editor
  question cards, results review cards, review missed-question cards, analytics
  weak-topic cards, and history rows.
- Dialogs are split between CustomTkinter top-level dialogs and native Tk
  messageboxes/file dialogs. Native dialogs cannot be fully styled through the
  app's CustomTkinter token system.

Inline style inventory by file:

- `test_selector.py`: home title, button bar, sort toolbar, test cards, archived
  cards, gray secondary buttons, purple mix button, warning review button,
  green export button, danger delete buttons, archived tuple card colors, muted
  labels.
- `collapsible_group.py`: transparent group shell/header, primary text toggle,
  tuple hover colors, gray Archive Group button.
- `test_editor.py`: top bar, metadata form, gray back button, success Save Test,
  gray divider, two-column framed panels, question cards with radius 6, warning
  no-answer label, gray add/cancel/edit buttons, transparent option rows,
  tuple-styled remove buttons.
- `test_taking.py`: top bar, gray flag button, success Check Answer, danger
  Finish, practice feedback card, correct/incorrect/essay text colors, progress
  container.
- `progress_bar.py`: clickable status buttons using shared status colors,
  hard-coded Helvetica 11 font, radius 4, compact size.
- `question_widget.py`: transparent option rows and shared body font; no status
  colors.
- `results_view.py`: centered score header, muted details, result cards, mix
  source section, status labels using correct/incorrect/gray, answer labels.
- `history_view.py`: top bar, gray back button, filters, table header, loading
  and empty muted labels, rows with radius 4.
- `review_view.py`: top bar, filter row, framed scope selector, gray secondary
  action, green Start Review, question cards, muted metadata, incorrect miss
  rate.
- `analytics_view.py`: top bar, gray back button, tab/filter rows, empty muted
  label, weak topic cards with a colored indicator and progress bar.
- `mix_test_dialog.py`: modal title, muted helper text and totals, grouped
  checkbox list, primary Start Mix Test, gray Cancel/Deselect.
- `mode_dialog.py`: modal title, default Test Mode, green Practice Mode, muted
  helper text.
- `autocomplete_entry.py`: transparent shell, overlay dropdown frame, tuple
  text and hover colors.
- `graph_widget.py`: local chart color palette for light/dark modes.

## Recommendations For Implementation Stories

- Start with semantic tokens in one shared GUI style module rather than adding
  more constants to unrelated modules. Candidate tokens: primary, secondary,
  tertiary/ghost, success, danger, warning, accent/special, muted text, surface,
  surface-muted, border/subtle divider, chart background/text/grid/series.
- Add button role helpers before changing every screen. Candidate roles:
  primary, secondary, ghost, success, warning, danger, and special. Include
  hover colors so screens stop repeating hover literals.
- Add small typography helpers or named font tuples for title, heading, body,
  small, small-bold, and compact. Preserve Python 3.9 compatibility.
- Standardize card/list surfaces with shared radius and padding decisions:
  general card radius 8, compact row radius 4 or 6, and explicit muted/archived
  surface colors.
- Standardize page headers after button tokens exist. Candidate helper:
  `build_page_header(parent, title, back_command=None)` or a small component if
  it matches the existing component style.
- Keep data-specific widgets local where behavior is coupled: progress buttons,
  graph rendering, autocomplete overlay placement, editor option rows, and
  grouped checkbox synchronization.
- Treat native `messagebox` and file dialogs as behavior-only for MVP visual
  work; record their wording and flows, but do not promise full visual styling.
- Split broad foundation work if needed: first tokens/button roles, then cards
  and page headers, then screen-specific adoption.

## Behavior Constraints

- Do not change service calls, import/export behavior, scoring, session state,
  review scope logic, or database access from visual stories.
- Preserve `on_show` refresh behavior and `controller.show_frame(...)` routing.
- Preserve disabled/enabled states: zero-question Take Test, practice Check
  Answer after locking, previous/next bounds, option remove when only two
  options remain.
- Preserve group expansion state on home refresh and group checkbox
  synchronization in review and mix dialog.
- Preserve chart data inputs and redraw lifecycle in `GraphWidget`.
- Preserve native dialogs and confirmation flows unless a separate product
  decision changes dialog behavior.

## Implementation Risks

- A single "gray" replacement could accidentally make secondary buttons, muted
  text, separators, disabled-like buttons, essay statuses, and empty states look
  identical or incorrect because they currently share one literal.
- Centralizing card creation too early could hide screen-specific behavior in
  home cards, editor cards, results cards, and review cards.
- Progress indicators are interactive CTkButtons, not passive badges; changing
  them to labels or non-buttons would break question navigation.
- Autocomplete dropdown is placed on the toplevel with absolute coordinates.
  Changing frame colors or z-order can break overlay readability.
- Matplotlib chart colors are not CTk widget colors; they need a separate chart
  palette or adapter.
- CustomTkinter tuple colors are useful for light/dark-specific states. A token
  system must preserve tuple support where the current code uses it.
- Some labels use fixed wraplength values. Visual typography changes can cause
  truncation or awkward wrapping on minimum window sizes.

## Open Questions

- Should "Mix Test" remain a distinct special/accent action, or should it become
  a normal secondary action after the home screen hierarchy is revised?
- Should `COLOR_SUCCESS` remain the visual color for practice mode and Start
  Review, or should success be reserved for outcome/status feedback only?
- Should archived tests use a separate muted card surface token, lower text
  contrast, or both?
- Should page header back buttons become ghost/secondary text buttons, icon
  buttons, or remain text buttons for MVP?
- Should charts use the same primary color as UI actions or a separate data
  visualization palette?

## Dev 2 Quick Start

- Begin with `config/settings.py` and a new or existing GUI-focused style entry
  point; do not mix visual helper functions into service or database modules.
- Search for `fg_color="gray"` and `text_color="gray"` first. Separate these
  into secondary action, muted text, divider, flag inactive, and essay-neutral
  roles before replacing them.
- Add hover tokens for existing semantic colors: danger `#c9302c`, success
  `#258a5e`, warning `#d9972d`, secondary `#5a6268`, and special `#5e2270`.
- Pilot button hierarchy on `test_selector.py` only after role names are clear:
  Take Test primary, destructive Delete danger, Archive/Edit/Export secondary or
  tertiary, Review Missed warning only if product keeps it elevated.
- For card/list pattern work, compare home cards, editor question cards,
  results review cards, review cards, analytics topic cards, and history rows
  before extracting a helper.
- Keep `ProgressBar`, `AutocompleteEntry`, and `GraphWidget` specialized; use
  tokens inside them but avoid forcing them into a generic card/button helper.
- Verify both light and dark appearance when replacing tuple colors or chart
  colors.
- Do not change native `messagebox` and file dialog behavior during visual
  token work.

## Refresh Triggers

- Any change to `study_test_tool/config/settings.py` visual constants.
- Any new shared style module, component helper, or button/card/page-header
  abstraction.
- Any visual implementation story that changes `study_test_tool/gui/` styling.
- Any switch away from CustomTkinter's default blue theme or system appearance
  mode.
- Any completed screenshot audit that contradicts static findings in this
  inventory.
