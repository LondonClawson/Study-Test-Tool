# STORY-015E: Native Dialog Inventory Follow-Up

## Status

Blocked.

## Readiness

- Blocked by: PM post-MVP decision.
- Unblocked by: explicit PM approval to replace or redesign a specific native
  messagebox or file-dialog flow.

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
