# STORY-005: Button Hierarchy

## Status

Blocked.

## Readiness

- Blocked by: CTX-FOUNDATION.
- Unblocked by: `STORY-003_visual_foundation_spec.md`.

## Sprint

Target sprint: Sprint 1.

## User Story

As a user, I want buttons to communicate priority and risk so that the next best
action is clear without making utility actions visually compete.

## Goal

Define and apply the MVP button role model for shared or high-traffic buttons.

## Required Context

- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.
- `visual_overhaul_project/01_context/summaries/style_inventory.md`.
- `visual_overhaul_project/01_context/summaries/home_screen_context.md` when home
  buttons are included.

## Scope

In:

- Primary, secondary, tertiary/utility, danger, warning, success, and muted
  button role application.
- Hover and disabled-state consistency where supported.
- Role guidance for future screen stories.

Out:

- Icon system.
- Button text changes that alter meaning.
- Moving workflow actions between screens.

## Likely Files

- Shared style entry points from STORY-004.
- High-traffic GUI screen files, only as needed for role application.

## Implementation Steps

1. Read CTX-FOUNDATION and the completed shared style entry-point handoff.
2. Identify the assigned action area and every button role in that area.
3. Apply primary, secondary, tertiary, danger, warning, success, and muted roles
   only where the foundation defines them.
4. Verify callbacks, navigation, and destructive confirmations still behave the
   same.
5. Check light/dark readability for all touched button states.
6. Document role usage and any follow-up areas not migrated.

## Acceptance Criteria

- Main next actions such as Take Test, Save, Continue/Next, and Finish are
  visually distinct from utility actions.
- Destructive actions are recognizable but not louder than the primary workflow.
- Existing callbacks and command wiring are unchanged.
- Button role usage is documented in the handoff or foundation summary.

## Verification

- Visual smoke check for touched screens in light and dark mode.
- Run tests if any behavior-bearing code path is touched.

## Dev 2 Assignment Notes

- Do not rename callbacks or change command wiring.
- Do not restyle every button in the app unless explicitly assigned.
- If the assignment does not name a target area, ask the PM to refine it before
  starting.

## Handoff Requirements

- List changed buttons by role.
- List unresolved role questions.
- Add follow-up stories for screens not covered.
