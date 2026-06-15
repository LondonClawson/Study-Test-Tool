# Baseline Visual Audit

## Purpose

Establish the current visual baseline of Study Testing Tool so Sprint 0 foundation work can target observed UI problems rather than guesses.

## Findings

### Capture Metadata

- Capture date: 2026-06-03.
- Environment: macOS 13.7.8 on x86_64 (`Darwin iMac-2.local`), Python 3.13.4, git branch `main`.
- Runtime state: the SQLite database at `study_test_tool/data/database/study_tool.db` was present but empty for tests, questions, attempts, and responses during inspection; `user_settings` was not present.
- Data setup: no temporary test data was created because the GUI could not be brought to a screenshot-ready state; the audit used the existing empty local database plus source inspection only.
- Launch attempt: `MPLCONFIGDIR=/tmp/rincewind-mpl XDG_CACHE_HOME=/tmp/rincewind-xdg python3 -u projects/Study-Test-Tool/study_test_tool/main.py` emitted only the macOS font-registry startup line (`system_profiler ... XType: Using static font registry.`) and then exited with code `-1` before any window appeared.
- Follow-up probe: a minimal `tkinter.Tk()` instantiation also exited with code `-1` before creating a window or emitting a Python traceback, even when `MPLCONFIGDIR` and `XDG_CACHE_HOME` were redirected to writable temp paths.
- Screenshot status: no runtime screenshots were captured because the local shell could not launch a Tk/CustomTkinter window in this environment. This is the same TQ-1420 blocker: the worker shell cannot produce a screenshot-ready GUI window here, so real screenshots are still pending on a GUI-capable runner.
- Screenshot folder prepared: `visual_overhaul_project/01_context/screenshots/baseline/light/` and `.../dark/`, but both remain empty.

### Screenshot Inventory

No screenshots were captured.

- Missing home/test selector states: populated grouped, populated ungrouped, archived tests, empty state.
- Missing test-taking states: normal unanswered, normal answered, flagged, practice before check, practice after correct feedback, practice after incorrect feedback, essay question.
- Missing results states: all-correct/high score, partial score, essay included, flagged included, mix-test source breakdown, results loaded from history.
- Missing editor states: new test, existing test with questions, multiple-choice edit, essay edit, validation warning.
- Missing data-view states: history populated, history empty/loading, analytics populated, analytics no-data, review with missed questions, review empty.
- Missing dialog states: mode selection, mix test, import/error/confirmation.
- Missing verification shots: light mode, dark mode, and minimum-window-size checks.

### App-Wide Findings

- The app is frame-based with a fixed 1000x700 window and a 800x600 minimum, so dense layouts need to survive a relatively small viewport (`gui/main_window.py:38-43`).
- Appearance is set to `system` and the default theme to `blue`, while many screens also hard-code semantic colors inline; that makes the visual language feel split between theme defaults and ad hoc overrides (`gui/main_window.py:38-39`, `gui/test_selector.py:69-115`, `gui/test_taking.py:75-127`, `gui/history_view.py:40-88`).
- Empty states are mostly plain gray labels instead of designed empty/loading/error surfaces (`gui/test_selector.py:155-161`, `gui/history_view.py:90-129`, `gui/analytics_view.py:109-115`, `gui/review_view.py:149-155`).
- Cards and rows are present, but their padding, radii, and metadata treatment vary by screen, which makes the app feel like a collection of screens rather than one product (`gui/test_selector.py:261-411`, `gui/results_view.py:253-368`, `gui/history_view.py:203-241`, `gui/review_view.py:344-407`).
- The charting layer has its own light/dark color mapping separate from the rest of the app, so analytics will need palette alignment during foundation work (`gui/components/graph_widget.py:29-46`).
- Multiple-choice questions are rendered as radio buttons plus labels rather than full-width selectable answer rows, which is functional but visually less polished (`gui/components/question_widget.py:48-81`).

### Per-Screen Findings

#### Home / Test Selector

- The home screen is the most visually crowded screen: it combines six top-bar actions, a sort toolbar, collapsible groups, active test cards, and archived test cards in one vertical stack (`gui/test_selector.py:55-153`, `gui/test_selector.py:197-259`).
- Button hierarchy is inconsistent. `Take Test` is primary, but `Edit`, `Export`, `Archive`, `Review Missed`, `View History`, `Analytics`, and `Mix Test` all sit at similar visual weight or use one-off semantic colors that do not form a single system (`gui/test_selector.py:69-115`, `gui/test_selector.py:305-347`, `gui/test_selector.py:396-410`).
- Archived cards are visually dimmed, which is good, but they still use the same surface structure and metadata treatment as active cards (`gui/test_selector.py:350-411`).
- The empty state is a single gray sentence, so the first-run experience will likely feel bare (`gui/test_selector.py:155-161`).

#### Test Taking

- The top bar has four competing elements in one line: title, timer, progress text, and flag button. That is likely to feel cramped at the minimum window size and even at the default size when question text is long (`gui/test_taking.py:50-83`).
- The bottom action row mixes navigation, a hidden practice-mode action, and a destructive-looking `Finish Test` button, even though finishing is a normal workflow action (`gui/test_taking.py:88-129`).
- Practice feedback is implemented as plain labels inside a framed area, so the correct/incorrect state is informative but not especially designed (`gui/test_taking.py:356-403`).
- The question widget itself uses radio rows plus text labels, and essay mode drops in a basic textbox, so answer selection feels utilitarian rather than like a polished study app (`gui/components/question_widget.py:30-92`).
- Progress buttons are color-coded by answered/current/flagged state, which is functionally strong, but the palette is still inherited from the app-wide semantic colors rather than a dedicated component system (`gui/components/progress_bar.py:1-69`).

#### Results

- The results screen is mostly text-first: score, time, and review cards are all readable, but the header lacks a stronger summary treatment (`gui/results_view.py:39-81`, `gui/results_view.py:106-154`).
- Review cards do cover correct, incorrect, flagged, and essay cases, but they do so with stacked text blocks rather than a more structured comparison layout (`gui/results_view.py:253-368`).
- Mix-test source breakdown is supported, which is good for the workflow, but it only appears when the session is a mix test (`gui/results_view.py:152-212`).
- `Back to Home` and `Retake Test` are visually similar, so the CTA hierarchy is not especially clear (`gui/results_view.py:60-77`).

#### History

- History uses a table-like layout with a loading label, filters, header row, and clickable rows, but the default row styling is still fairly flat (`gui/history_view.py:34-129`, `gui/history_view.py:203-241`).
- The loading state is just text, and the empty state is also a gray label, so there is no designed “nothing to show yet” treatment (`gui/history_view.py:90-129`).
- The filter row is fairly wide already, so it may become awkward at the minimum window size once longer test names are present (`gui/history_view.py:54-88`).

#### Analytics

- Analytics is the best candidate for app-wide token alignment because it combines tabs, filters, a chart widget, and a weak-topics state machine that uses explicit weak/moderate/strong colors (`gui/analytics_view.py:32-115`, `gui/analytics_view.py:269-321`).
- Empty analytics states are plain labels, so “no data” and “no categories tagged” will not feel distinct enough without design work (`gui/analytics_view.py:173-258`).
- The graph widget already adapts to light and dark appearance mode, but its palette is separate from the rest of the app and should be folded into the visual foundation (`gui/components/graph_widget.py:29-46`, `gui/components/graph_widget.py:68-185`).

#### Review

- Review is structurally dense: scope selection, select/deselect actions, a segmented filter, a selectable question list, a selected-count label, and a primary start-review action all appear above the missed-question list (`gui/review_view.py:39-155`).
- The scope selector is useful but visually heavy, and the screen has several nested scrollable regions that are likely to be fragile at smaller heights (`gui/review_view.py:86-147`, `gui/review_view.py:168-223`).
- Empty review state is again a plain label, so the screen lacks a designed no-missed-questions experience (`gui/review_view.py:149-155`, `gui/review_view.py:322-342`).

#### Editor

- The editor is the densest single screen: top bar, metadata form, save button, two-column content area, question list, scrollable question form, option rows, and essay mode all live together (`gui/test_editor.py:34-240`).
- The layout is functional but likely the highest-risk screen for clipping at the minimum size because both columns can scroll independently and the form has many conditional controls (`gui/test_editor.py:109-240`, `gui/test_editor.py:293-410`).
- Validation warnings are largely delivered through message boxes, so design work will need to pair the screen layout with clearer in-surface validation states (`gui/test_editor.py:413-661`).

#### Dialogs

- The custom dialogs are simple CTk toplevels with clear choices, but they are visually basic and not yet harmonized with a broader modal style (`gui/components/mode_dialog.py:9-85`, `gui/components/mix_test_dialog.py:45-269`).
- Native import/error/confirmation dialogs are still message boxes, so they are functionally correct but not visually part of the app system (`gui/test_selector.py:413-460`, `gui/test_taking.py:440-486`, `gui/test_editor.py:413-661`, `gui/history_view.py:160-163`).

### Light / Dark Differences

- Only a few areas are explicitly theme-aware today. The strongest example is `GraphWidget`, which changes its chart background, text, grid, and line colors based on appearance mode (`gui/components/graph_widget.py:29-46`).
- Archived home cards also use a light/dark tuple for their background color (`gui/test_selector.py:356-358`).
- Most other screen styling is hard-coded with inline colors, so the current light/dark behavior is likely to be mostly inherited CustomTkinter theming plus a few component-specific exceptions rather than a cohesive dual-theme system (`gui/test_selector.py:69-115`, `gui/test_taking.py:75-127`, `gui/review_view.py:93-135`).

### Minimum-Window Concerns

- Not runtime-verified because the GUI could not launch here.
- Source inspection suggests the highest-risk areas are:
  - Home: six-button action bar plus sort toolbar (`gui/test_selector.py:65-149`).
  - Test taking: title, timer, progress, flag, and bottom navigation on one row (`gui/test_taking.py:50-133`).
  - Editor: two-column form with nested scroll frames (`gui/test_editor.py:109-240`).
  - Review: scope selector plus list plus action bar above the missed-question list (`gui/review_view.py:86-147`).
  - History and analytics: filter rows plus table/chart content in a shared vertical budget (`gui/history_view.py:54-121`, `gui/analytics_view.py:52-115`).

### Missing Screenshots and Blockers

- Missing runtime screenshots: all checklist states listed above.
- Blocker: this shell could not produce a screenshot-ready Tk/CustomTkinter window, so the app could not be launched far enough to capture screens locally.
- Blocker detail: both the app entry point and a minimal `tkinter.Tk()` probe exited with code `-1` before any window appeared or Python exception was printed. The app entry point stopped after macOS font-registry startup noise and never reached a usable GUI state, which points to a lower-level GUI/runtime failure in this environment rather than a screen-specific app defect.
- Resulting limitation: the audit is source-backed only and should be refreshed with real screenshots before foundation implementation begins. Real baseline screenshots are still pending.

### Priority Issues for Foundation vs Screen Work

- Foundation work should solve:
  - Shared background/surface/border tokens.
  - Button roles and emphasis levels.
  - Typography scale and metadata treatment.
  - Empty/loading/error state styling.
  - Card/list row consistency.
  - Chart palette alignment with the rest of the app.
- Screen work should solve:
  - Home composition and action ordering.
  - Test-taking shell and practice feedback layout.
  - Results summary and review card structure.
  - Editor two-column density and validation presentation.
  - History row polish and analytics topic card layout.
  - Review scope selection density.
  - Dialog styling and modal hierarchy.

### Dev 2 Quick Start

- Start with this audit and the source files it cites, then confirm the baseline screenshots on a machine that can actually run the GUI.
- Highest-value source files to inspect first for implementation planning:
  - `gui/main_window.py`
  - `gui/test_selector.py`
  - `gui/test_taking.py`
  - `gui/results_view.py`
  - `gui/history_view.py`
  - `gui/analytics_view.py`
  - `gui/review_view.py`
  - `gui/components/graph_widget.py`
  - `gui/components/question_widget.py`
  - `gui/components/mode_dialog.py`
  - `gui/components/mix_test_dialog.py`
- Treat the home screen and test-taking screen as the first visual-priority slices because they drive the rest of the app hierarchy.

## Recommendation

Do not begin visual foundation implementation from this source-only pass alone. Mark the baseline audit blocked until real light/dark screenshots are captured on a GUI-capable machine, then use the resulting evidence to define the shared tokens and component rules before touching any screen layouts.
