# STORY-015B: Mode Dialog Polish

## Status

Done.

## Readiness

- Blocked by: None.
- Unblocked by: accepted completion of the button hierarchy pilot.

## Sprint

Target sprint: Sprint 3.

## User Story

As a learner, I want the mode selection dialog to make Test and Practice choices
clear without implying Practice is a success outcome.

## Required Context

- `visual_overhaul_project/01_context/summaries/dialog_context.md`.
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.
- Completed handoff for `STORY-005`.

## Scope

In:

- `ModeSelectionDialog` visual hierarchy.
- Balanced descriptions for Test and Practice mode.
- Foundation dialog surface, text, spacing, and button roles.

Out:

- Mode return values.
- Navigation flow.
- New dialog framework.
- Native message boxes.

## Likely Files

- `study_test_tool/gui/components/mode_dialog.py`.

## Implementation Steps

1. Read CTX-DIALOGS, CTX-FOUNDATION, and the completed button hierarchy handoff.
2. Apply foundation surface, text, spacing, and button roles to
   `ModeSelectionDialog` only.
3. Preserve `get_mode()`, close/cancel behavior, `transient(parent)`,
   `grab_set()`, parent centering, and `wait_window()`.
4. Verify close, Test Mode, Practice Mode, light mode, dark mode, and parent
   centering.

## Acceptance Criteria

- Test Mode is the primary action.
- Practice Mode is not styled as a success outcome.
- Both choices have clear, balanced visual hierarchy.
- All modal return paths are unchanged.

## Verification

- Screenshot evidence is required under
  `visual_overhaul_project/01_context/screenshots/after/STORY-015B/`.
- Capture or document a blocker for light and dark Mode Selection states
  covering initial dialog display, Test Mode action, Practice Mode action, and
  close/cancel path where practical.
- Smoke check Test, Practice, and close/cancel paths.
- Visual check light and dark mode.

## Handoff Requirements

- List dialog states checked.
- List screenshot evidence paths or exact capture blockers for every required
  dialog state.
- Confirm `get_mode()` return values stayed unchanged.
- Confirm modal close/cancel behavior stayed unchanged.
- List smoke checks run or explain why they were skipped.
