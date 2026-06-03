# Screen And Component Inventory

## Metadata

- Summary ID: CTX-SCREEN-INV.
- Created: 2026-06-02.
- Last updated: 2026-06-02.
- Produced by: initial project documentation pass.
- Source files inspected: GUI file inventory and selected screen reads.

## Major Screens

| Screen | File | Priority | Main Visual Concerns |
| --- | --- | --- | --- |
| Home/test selector | `study_test_tool/gui/test_selector.py` | 1 | First impression, dashboard composition, test cards, group headers, button hierarchy, empty state |
| Test taking | `study_test_tool/gui/test_taking.py` | 2 | Core workflow, question readability, answer rows, top bar, timer/progress/flag, practice feedback |
| Results | `study_test_tool/gui/results_view.py` | 3 | Score summary, status badges, answer comparison, mix-test source breakdown |
| Test editor | `study_test_tool/gui/test_editor.py` | 4 | Dense two-column layout, question list cards, form hierarchy, validation/action states |
| History | `study_test_tool/gui/history_view.py` | 5 | Data rows, filters, loading/empty states, clickable row affordance |
| Analytics | `study_test_tool/gui/analytics_view.py` | 6 | Chart theme, tabs, filters, weak-topic cards, no-data state |
| Review | `study_test_tool/gui/review_view.py` | 7 | Scope selection, missed-question list, action hierarchy, empty state |
| Dialogs | `gui/components/mode_dialog.py`, `gui/components/mix_test_dialog.py`, native message boxes | 8 | Dialog hierarchy, selection rows, confirmation/error polish |

## Shared Components

| Component | File | Relevant Stories |
| --- | --- | --- |
| Collapsible group | `study_test_tool/gui/components/collapsible_group.py` | Home cards and group headers |
| Question widget | `study_test_tool/gui/components/question_widget.py` | Test-taking readability and answer rows |
| Progress bar | `study_test_tool/gui/components/progress_bar.py` | Test-taking progress indicators |
| Timer widget | `study_test_tool/gui/components/timer_widget.py` | Test-taking top bar |
| Graph widget | `study_test_tool/gui/components/graph_widget.py` | Analytics chart theme |
| Mode dialog | `study_test_tool/gui/components/mode_dialog.py` | Dialog polish |
| Mix test dialog | `study_test_tool/gui/components/mix_test_dialog.py` | Dialog polish and home workflow |
| Autocomplete entry | `study_test_tool/gui/components/autocomplete_entry.py` | Editor/group entry polish |

## File Size Notes

The largest GUI files are `test_selector.py`, `test_editor.py`,
`test_taking.py`, `review_view.py`, and `results_view.py`. Stories touching
these should rely on screen-specific summaries before implementation.

## Refresh Triggers

Update this inventory when a GUI file is added, removed, renamed, or split into
new components.
