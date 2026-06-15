# STORY-007: Page Header Pattern

## Status

Blocked.

## Readiness

- Blocked by: a named pilot screen/path.
- Unblocked by: PM approval of the pilot screen/path.

CTX-FOUNDATION and `STORY-004_shared_style_entrypoints.md` are Done. This story
is still blocked until PM names one pilot screen or explicitly chooses a shared
helper path.

## Sprint

Target sprint: Sprint 1 or Sprint 2.

## User Story

As a user, I want each screen to have a familiar header structure so that title,
context, navigation, and primary actions are predictable.

## Goal

Define and pilot a reusable page header pattern for major screens.

## Required Context

- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.
- `visual_overhaul_project/01_context/summaries/gui_architecture_summary.md`.
- Relevant screen summary for the pilot area.

## Scope

In:

- Header title, optional subtitle/context, back/navigation placement, and action
  placement.
- One pilot screen.

Out:

- Persistent navigation redesign.
- Renaming screens.
- Moving workflows between screens.

## Likely Files

- One GUI screen file selected during sprint planning.
- Shared component file only if the pilot proves reuse is useful.

## Implementation Steps

1. Read CTX-FOUNDATION and the relevant pilot screen context.
2. Confirm the assigned pilot screen or shared helper path.
3. Define title, subtitle, metadata, and action placement rules.
4. Apply the header pattern only to the assigned pilot area.
5. Verify minimum-window behavior and light/dark readability.
6. Document reusable header rules and follow-up screens.

## Acceptance Criteria

- Header pattern improves hierarchy without creating a marketing-style layout.
- The pilot screen preserves existing navigation behavior.
- The pattern can be used by later home, results, editor, history, analytics, and
  review stories.

## Verification

- Visual check at normal and minimum window sizes.
- Navigation smoke check for the pilot screen.

## Dev 2 Assignment Notes

- Do not introduce a shared header component unless the assignment explicitly
  names that as the implementation path.
- Do not move navigation semantics or controller calls.
- If the pilot screen is not named, return the story for PM refinement.

## Handoff Requirements

- Document final header pattern.
- Note which screens should adopt it next.
