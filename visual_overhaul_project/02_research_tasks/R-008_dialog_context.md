# R-008: Dialog Context

## Status

Blocked until R-001 is Done. Assign before dialog implementation stories.

## Role

Assign to Dev 1 Research Agent before dialog implementation stories.

## Goal

Create focused context for mode selection, mix test, import/error/confirmation,
and other dialog-like interactions. Keep the scope to visual polish and
readability, not workflow redesign.

## Output

Write the summary to:

```text
visual_overhaul_project/01_context/summaries/dialog_context.md
```

## Required Inputs

- `visual_overhaul_project/01_context/summaries/gui_architecture_summary.md`.
- `VISUAL_OVERHAUL_PLAN.md`.

## Source Files

- `study_test_tool/gui/components/mode_dialog.py`.
- `study_test_tool/gui/components/mix_test_dialog.py`.
- Native `tkinter.messagebox` usage across `study_test_tool/gui/`.
- Import/export user feedback paths in `test_selector.py`.

## Do Not Change

- Do not change application code.
- Do not redesign dialogs.
- Do not replace native message boxes.
- Do not change modal behavior, callbacks, return values, import/export
  behavior, or mix-test creation behavior.

## Research Steps

1. Inventory all custom dialogs and native message boxes used by GUI screens.
2. Map the user action that opens each dialog.
3. Record current visual structure and button roles.
4. Identify dialogs that should remain native during MVP.
5. Identify dialogs where polish would materially improve clarity.
6. Note any constraints around modal behavior, return values, and callbacks.

## Summary Must Include

- Dialog inventory.
- Current custom-dialog structure.
- Native message box usage summary.
- Visual issues.
- Behavior constraints.
- Recommended MVP and post-MVP split.
- Recommended implementation story split.
- Dev 2 Quick Start notes.

## Done Criteria

- `dialog_context.md` exists.
- It gives enough detail for dialog polish stories.
- Context index status for CTX-DIALOGS is updated.
- `00_project/status_board.md` is updated.
- The handoff lists source files inspected and dialog states not inspected.
- The summary passes `00_project/definition_of_ready.md`.
