# Dialog Context Summary

## Metadata

- Summary ID: CTX-DIALOGS.
- Summary file:
  `visual_overhaul_project/01_context/summaries/dialog_context.md`.
- Created: 2026-06-15.
- Last updated: 2026-06-15.
- Produced by research task:
  `visual_overhaul_project/02_research_tasks/R-008_dialog_context.md`.
- Research agent: Codex.
- Source files inspected: `VISUAL_OVERHAUL_PLAN.md`,
  `visual_overhaul_project/01_context/summaries/gui_architecture_summary.md`,
  `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`,
  `study_test_tool/gui/components/mode_dialog.py`,
  `study_test_tool/gui/components/mix_test_dialog.py`,
  `study_test_tool/gui/components/import_preview_dialog.py`,
  `study_test_tool/gui/test_selector.py`,
  `study_test_tool/gui/test_editor.py`,
  `study_test_tool/gui/test_taking.py`,
  `study_test_tool/gui/main_window.py`, and
  `study_test_tool/gui/history_view.py`.
- Screens/states inspected: static source inspection for mode selection, mix
  test selection, import preview, import partner selection, batch PDF import
  choice, import report, no-mixable-tests state, missing-answer confirmation,
  export warnings, delete/archive confirmations, editor validation, unsaved
  changes, finish-test confirmation, quit-test confirmation, and history load
  error.
- Screens/states not inspected: live rendered light/dark dialogs, OS-native
  messagebox appearance, macOS file picker appearance, keyboard traversal,
  screen reader behavior, long localized text, and minimum-window runtime
  screenshots.

## Purpose

Use this summary before splitting or implementing dialog polish work, especially
the dialog portions of `STORY-015_review_and_dialog_polish.md`. It maps current
dialog entry points, visual structure, behavior constraints, and recommended
MVP boundaries so implementation can improve clarity without changing modal
return values, callbacks, import/export behavior, review logic, or mix-test
creation behavior.

## Dialog Inventory

Custom `CTkToplevel` dialogs:

- `ModeSelectionDialog` in `mode_dialog.py`: opened from
  `TestSelectorFrame._on_take_test()` and `_on_mix_test()` before navigation to
  test-taking. Returns `MODE_TEST`, `MODE_PRACTICE`, or `None`.
- `MixTestDialog` in `mix_test_dialog.py`: opened from
  `TestSelectorFrame._on_mix_test()` after tests with questions are collected.
  Returns selected test IDs and requested question count, or `None`.
- `ImportPreviewDialog` in `import_preview_dialog.py`: opened from
  `TestSelectorFrame._confirm_and_commit_import()` after JSON, text, PDF, or
  DOCX preview generation. Returns `(confirmed, group_name)` or `None`.

Native file dialogs:

- `filedialog.askopenfilename()` in `_on_import()` selects JSON, text, PDF, or
  DOCX import input.
- `filedialog.askopenfilename()` in `_import_pdf()` selects a missing matching
  Questions or Answers partner file.
- `filedialog.asksaveasfilename()` in `_on_export_test()` selects a JSON export
  path.

Native message boxes:

- Home/import/export: import errors, import success, multi-pair PDF choice, PDF
  import report, no mixable tests, no selected mix questions, missing answers
  before test-taking, export validation, export warnings, export success, delete
  test confirmation, and archive group confirmation.
- Editor: required test name, test created/updated success, save-first warning,
  question text and option validation, missing essay expected-answer warning,
  unsaved-change confirmations, and delete-question confirmation.
- Test taking and app close: missing review questions, missing test, empty test,
  finish test/practice confirmation with unanswered and flagged counts, and
  quit-while-testing confirmation.
- History: load failure error.

## Current Custom Dialog Structure

`ModeSelectionDialog` is a fixed 360 x 220 modal with parent centering,
`transient(parent)`, and `grab_set()`. It uses a centered heading, a transparent
button row, `Test Mode` as the default blue CTk button, `Practice Mode` as a
green success-colored button, and a single gray helper label. Closing the
window returns `None`.

`MixTestDialog` is a fixed 450 x 560 modal with parent centering,
`transient(parent)`, and `grab_set()`. It has a centered title, gray helper
label, Select All and Deselect All utility buttons, a scrollable grouped
checkbox list, total-available label, question-count entry, and Start Mix
Test/Cancel action row. Group checkboxes control child test checkboxes and child
changes sync the group state. Invalid OK states currently return silently.

`ImportPreviewDialog` is a fixed 620 x 560 modal with parent centering,
`transient(parent)`, and `grab_set()`. It summarizes importable and skipped
tests, offers an optional group entry, renders preview rows in a scrollable
frame, disables Import when no preview is importable, and returns confirmation
plus group override. Rows use status text and color, but otherwise rely on
default CTk frame surfaces.

## Native Dialog Usage Summary

Native message boxes carry short transactional states where OS-standard behavior
is acceptable for MVP: confirmations, validation warnings, import/export status,
and unexpected errors. The highest-impact native dialog is the batch PDF import
choice because it uses a three-way `askyesnocancel()` contract where `Yes`
imports all pairs, `No` imports only the selected pair, and `Cancel` aborts.
That return contract must remain unchanged.

Native file dialogs are behavior-only integration points with the OS. They
should remain native for MVP. Visual polish should focus on the custom CTk
dialogs and on making pre/post file-dialog message text clearer only if a later
story explicitly includes copy cleanup.

## Visual Findings

- Custom dialogs use fixed sizes, centered headings, gray helper text, and
  mostly default CTk surfaces. They work, but they do not yet use the accepted
  foundation roles for dialog surface, text hierarchy, borders, or button roles.
- `ModeSelectionDialog` gives Practice Mode stronger visual color than Test
  Mode because it uses success green. Practice is a mode, not a success state;
  this can compete with the primary path.
- `ModeSelectionDialog` has minimal explanatory structure. The helper text only
  explains practice mode, so Test Mode has no parallel description.
- `MixTestDialog` has useful grouping behavior, but group headers and child rows
  look like plain checkboxes in a default scroll frame. Dense lists may be hard
  to scan when many tests or long names exist.
- `MixTestDialog` silently ignores invalid start attempts: no selected tests,
  non-numeric count, and non-positive count. That is a behavior and feedback
  issue; visual stories should not change it unless explicitly approved.
- `ImportPreviewDialog` is the most information-heavy dialog. Ready/skipped
  rows, warning/error messages, and group assignment would benefit from clearer
  row surfaces, status badges, and hierarchy.
- Native message boxes are visually inconsistent with CustomTkinter by nature.
  Replacing all of them would create risk and is outside MVP scope.
- Error and report dialogs can contain long generated text, especially PDF
  import reports and export warnings. Any future custom replacement must handle
  wrapping and scrolling intentionally.

## Behavior Constraints

- Do not change `ModeSelectionDialog.get_mode()` return values or close/cancel
  behavior.
- Do not change mix-test selection semantics, group checkbox sync, selected test
  ID ordering, question count parsing, or `MixTestDialog.get_result()`.
- Do not change `ImportPreviewDialog.get_result()`, group override handling,
  import button disablement when no previews are importable, or commit timing.
- Preserve `transient(parent)`, `grab_set()`, parent centering, and
  `wait_window()` modal behavior for custom dialogs.
- Do not replace native file dialogs during MVP.
- Do not replace native message boxes as part of broad visual polish. The
  batch PDF `askyesnocancel()` and all `askyesno()` confirmations are behavior
  gates and must keep their return handling.
- Do not change import/export services, mix service selection behavior,
  test-taking navigation, scoring, archive/delete persistence, or editor save
  validation.

## Recommended MVP And Post-MVP Split

MVP:

- Polish `ModeSelectionDialog` with foundation dialog surfaces, balanced mode
  descriptions, and button roles that treat Test as primary and Practice as a
  secondary or clearly differentiated mode action without using success as the
  main meaning.
- Polish `MixTestDialog` list readability, group headers, total/count area, and
  action hierarchy while preserving silent validation behavior unless a separate
  product decision approves inline validation.
- Polish `ImportPreviewDialog` row surfaces, ready/skipped status treatment,
  warnings/errors, and group entry hierarchy. Keep import behavior unchanged.
- Keep native message boxes and file dialogs as deliberate MVP choices.

Post-MVP:

- Consider a custom confirmation/report pattern only for high-volume or
  long-content dialogs such as PDF import reports, export warnings, and missing
  answer confirmations.
- Consider copy and validation improvements for silent `MixTestDialog` invalid
  start states as a behavior story, not a visual-only polish task.
- Consider keyboard focus defaults and accessibility review for all modal
  dialogs after the visual MVP is stable.

## Recommended Implementation Story Split

- `STORY-015A_mode_dialog_polish`: `ModeSelectionDialog` only. Verify close,
  Test Mode, Practice Mode, light mode, dark mode, and parent centering.
- `STORY-015B_mix_dialog_polish`: `MixTestDialog` only. Verify empty selection
  remains non-submitting, select all, deselect all, group toggle, child toggle,
  valid start, cancel, light mode, and dark mode.
- `STORY-015C_import_preview_dialog_polish`: `ImportPreviewDialog` only. Verify
  all-ready previews, skipped/error previews, mixed warnings, no-importable
  previews, group override, import, cancel, light mode, and dark mode.
- `STORY-015D_native_dialog_inventory_followup`: documentation or product
  decision story for message boxes and file dialogs. Do not implement unless PM
  chooses to replace a specific native dialog after MVP.

## Dev 2 Quick Start

- Read `visual_foundation_decisions.md` before styling any custom dialog.
- Start with one custom dialog story. Do not bundle mode, mix, import preview,
  and native message boxes into one junior implementation assignment.
- Reuse shared style entry points from `STORY-004` once accepted. If those
  helpers are still only submitted for review, wait for PM acceptance or keep
  the dialog story blocked.
- Keep all existing public methods and modal contracts unchanged:
  `get_mode()`, `get_result()`, `wait_window()`, and callback wiring.
- Use source inspection plus runtime smoke checks for every return path because
  these dialogs gate navigation, import commits, and mix-test creation.

## Open Questions

- Should silent invalid starts in `MixTestDialog` remain exactly as-is for MVP,
  or should a later behavior story add inline validation?
- Should import preview polish be grouped with dialog polish or with later
  import workflow polish?
- Should any native message box be replaced before MVP closeout, or should all
  native dialogs remain documented exceptions?

## Refresh Triggers

Update this summary if custom dialog structure changes, new CTk dialogs are
added, messagebox/filedialog usage changes, import preview behavior changes,
or `STORY-004` chooses style helper names that materially affect dialog
implementation.
