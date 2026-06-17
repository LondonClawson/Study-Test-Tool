# STORY-015E: Native Dialog Inventory Follow-Up

## Status

Done.

## Readiness

- Blocked by: None.
- PM decision made on 2026-06-17: no native messagebox or file-dialog
  replacement is approved for MVP. Native dialogs are deliberate MVP
  exceptions, and any future replacement must be assigned as a separate
  post-MVP story.

## PM Decision

All native message boxes and file dialogs remain native for MVP. This protects
OS-standard file picking, confirmation return contracts, import/export status
flows, and behavior-critical choices such as batch PDF import.

Native dialogs intentionally left native for MVP:

- File open/save dialogs for JSON, text, PDF, DOCX import, missing PDF partner
  selection, and JSON export path selection.
- Import/export status, validation, warning, error, and success message boxes.
- Batch PDF import `askyesnocancel()` where Yes imports all pairs, No imports
  only the selected pair, and Cancel aborts.
- Delete/archive confirmations, editor validation and unsaved-change
  confirmations, finish-test and quit-while-testing confirmations, and history
  load errors.

No native dialog replacement candidate is approved for MVP. Post-MVP candidates
may be considered later for long-content/report flows such as PDF import
reports, export warnings, and missing-answer confirmations, but only through a
new narrow implementation story.

## Sprint

Target sprint: Post-MVP or PM-approved exception.

## User Story

As a maintainer, I want native dialog exceptions documented so MVP visual polish
does not accidentally replace behavior-critical OS dialogs.

## Required Context

- `visual_overhaul_project/01_context/summaries/dialog_context.md`.
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.

## Scope

In:

- Native messagebox and filedialog inventory.
- Recommendation for any one dialog that should become a custom dialog after
  MVP.
- Explicit documentation of dialogs intentionally left native.

Out:

- Replacing native message boxes.
- Replacing native file dialogs.
- Changing confirmation return contracts.
- Copy cleanup unless PM explicitly includes it.

## Likely Files

- Visual-overhaul documentation only, unless PM approves one implementation
  target later.

## Implementation Steps

1. Read CTX-DIALOGS.
2. Confirm whether PM wants all native dialogs left alone for MVP or wants one
   named replacement candidate.
3. If no replacement is approved, document the native-dialog exception list and
   keep this story blocked or close it as not planned.
4. If one replacement is approved later, create a new narrow implementation
   story for that single dialog.

## Acceptance Criteria

- Native message boxes and file dialogs are documented as deliberate MVP
  exceptions.
- Batch PDF `askyesnocancel()` and all confirmation return contracts are
  explicitly protected.
- No native dialog is replaced without a separate PM-approved story.

## Verification

- Documentation review only unless a later implementation story is created.

## Handoff Requirements

- List native dialogs left as MVP choices.
- List any PM-approved post-MVP replacement candidate.
