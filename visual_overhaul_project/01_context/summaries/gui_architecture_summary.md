# GUI Architecture Summary

## Metadata

- Summary ID: CTX-GUI-ARCH.
- Created: 2026-06-02.
- Last updated: 2026-06-02.
- Produced by: initial project documentation pass.
- Source files inspected: `study_test_tool/gui/main_window.py`,
  `study_test_tool/utils/constants.py`, GUI file inventory.

## Purpose

Use this summary when a story touches screen layout, navigation, page structure,
or shared GUI components. It gives enough orientation to avoid rediscovering the
frame-based architecture.

## Current Structure

The app is a CustomTkinter desktop app. `study_test_tool/gui/main_window.py`
defines `App(ctk.CTk)`, sets appearance mode to `system`, sets the default color
theme to `blue`, creates one container frame, instantiates each screen once, and
uses `show_frame(name, **kwargs)` to raise a screen.

Screen names are constants in `study_test_tool/utils/constants.py`:

- `SCREEN_HOME`
- `SCREEN_EDITOR`
- `SCREEN_TEST_TAKING`
- `SCREEN_RESULTS`
- `SCREEN_HISTORY`
- `SCREEN_REVIEW`
- `SCREEN_ANALYTICS`

Every screen is registered in `App.__init__()` and may implement
`on_show(**kwargs)`. Visual work must preserve the `show_frame` contract because
test-taking, results, history, and review flows pass data through it.

## Major Screen Files

- Home/test selector: `study_test_tool/gui/test_selector.py`.
- Test editor: `study_test_tool/gui/test_editor.py`.
- Test taking: `study_test_tool/gui/test_taking.py`.
- Results: `study_test_tool/gui/results_view.py`.
- History: `study_test_tool/gui/history_view.py`.
- Analytics: `study_test_tool/gui/analytics_view.py`.
- Review: `study_test_tool/gui/review_view.py`.

## Component Files

- Autocomplete entry: `gui/components/autocomplete_entry.py`.
- Collapsible group: `gui/components/collapsible_group.py`.
- Graph widget: `gui/components/graph_widget.py`.
- Mix test dialog: `gui/components/mix_test_dialog.py`.
- Mode dialog: `gui/components/mode_dialog.py`.
- Progress bar: `gui/components/progress_bar.py`.
- Question widget: `gui/components/question_widget.py`.
- Timer widget: `gui/components/timer_widget.py`.

## Behavior Constraints

- GUI screens call services. They should not start using raw SQLite.
- `App.show_frame()` should keep raising frames and calling `on_show`.
- Test-taking close confirmation in `App._on_close()` must remain intact.
- Screen constants should remain the routing source.
- Visual changes should not alter service calls, persistence, scoring, imports,
  exports, or test session semantics.

## Implementation Risks

- Shared styling work may require touching many screens. Split by component
  family or screen to reduce regression risk.
- Hard-coded appearance settings in `main_window.py` and `GraphWidget` affect
  both light and dark mode.
- Some screen files are large. Context summaries should narrow the relevant
  methods before implementation.

## Refresh Triggers

Update this summary if screen registration changes, a screen is renamed, a new
major screen is added, or the navigation contract changes.
