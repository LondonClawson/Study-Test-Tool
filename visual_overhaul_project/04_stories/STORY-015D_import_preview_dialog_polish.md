# STORY-015D: Import Preview Dialog Polish

## Status

Submitted For Review.

## Readiness

- Blocked by: None.
- Unblocked by: accepted completion of the button hierarchy and card/list
  pattern pilots.

## Sprint

Target sprint: Sprint 3.

## User Story

As a learner importing study material, I want the import preview dialog to make
ready, skipped, warning, and error rows easy to understand before committing.

## Required Context

- `visual_overhaul_project/01_context/summaries/dialog_context.md`.
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.
- Completed handoff for `STORY-005`.
- Completed handoff for `STORY-006`, unless PM explicitly approves a dialog-only
  row treatment.

## Scope

In:

- `ImportPreviewDialog` row surfaces and status treatment.
- Ready/skipped/warning/error hierarchy.
- Optional group entry hierarchy.
- Import/Cancel action hierarchy and disabled Import state.

Out:

- Import parsing or commit behavior.
- Group override behavior.
- Native file dialogs.
- Import report message boxes.

## Likely Files

- `study_test_tool/gui/components/import_preview_dialog.py`.

## Implementation Steps

1. Read CTX-DIALOGS, CTX-FOUNDATION, and completed foundation handoffs.
2. Polish only `ImportPreviewDialog` visual hierarchy and preview rows.
3. Preserve `get_result()`, group override handling, disabled Import behavior
   when no preview rows are importable, and modal behavior.
4. Verify all-ready previews, skipped/error previews, mixed warnings,
   no-importable previews, group override, import, cancel, light mode, and dark
   mode.

## Acceptance Criteria

- Importable and skipped rows are visually distinct and readable.
- Warnings/errors are clear without changing parser or commit behavior.
- Disabled Import remains obvious when no previews can be imported.
- Modal return paths are unchanged.

## Verification

- Screenshot evidence is required under
  `visual_overhaul_project/01_context/screenshots/after/STORY-015D/`.
- Capture or document a blocker for light and dark Import Preview states
  covering all-ready previews, skipped/error previews, mixed warnings,
  no-importable previews with disabled Import, group override, import-ready
  state, and cancel path where practical.
- Smoke check import, cancel, group override, and no-importable states.
- Visual check light and dark mode.

## Handoff Requirements

- List preview states checked.
- List screenshot evidence paths or exact capture blockers for every required
  preview state.
- Confirm `get_result()` and disabled Import behavior stayed unchanged.
- Confirm import parsing, commit behavior, group override behavior, and modal
  cancel paths stayed unchanged.
- List smoke checks run or explain why they were skipped.
