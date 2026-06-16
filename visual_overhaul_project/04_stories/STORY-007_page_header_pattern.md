# STORY-007: Page Header Pattern

## Status

Submitted For Review.

## Readiness

- Blocked by: None.
- Unblocked by: PM approval of Home/Test Selector as the pilot screen/path.

CTX-FOUNDATION and `STORY-004_shared_style_entrypoints.md` are Done. This story
is assigned with Home/Test Selector as the narrow pilot screen. Use
`visual_overhaul_project/06_handoffs/STORY-007_page_header_pattern_assignment.md`
as the assignment packet.

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
- One pilot screen: Home/Test Selector.

Out:

- Persistent navigation redesign.
- Renaming screens.
- Moving workflows between screens.

## Likely Files

- `study_test_tool/gui/test_selector.py`.
- `study_test_tool/gui/styles.py` only if minimal shared header roles are needed.

## Implementation Steps

1. Read CTX-FOUNDATION and the relevant pilot screen context.
2. Confirm Home/Test Selector as the assigned pilot screen.
3. Define title, subtitle, metadata, and action placement rules.
4. Apply the header pattern only to the assigned Home/Test Selector area.
5. Verify minimum-window behavior and light/dark readability.
6. Document reusable header rules and follow-up screens.

## Acceptance Criteria

- Header pattern improves hierarchy without creating a marketing-style layout.
- The Home/Test Selector pilot preserves existing navigation behavior.
- The pattern can be used by later home, results, editor, history, analytics, and
  review stories.

## Verification

- Visual check at normal and minimum window sizes.
- Navigation smoke check for the pilot screen.

## Dev 2 Assignment Notes

- Do not introduce a shared header component unless the assignment explicitly
  names that as the implementation path.
- Do not move navigation semantics or controller calls.
- Keep the pilot limited to Home/Test Selector.

## Handoff Requirements

- Document final header pattern.
- Note which screens should adopt it next.
