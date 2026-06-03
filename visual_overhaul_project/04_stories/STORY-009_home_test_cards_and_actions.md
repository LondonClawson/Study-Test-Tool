# STORY-009: Home Test Cards And Actions

## Status

Blocked.

## Readiness

- Blocked by: CTX-FOUNDATION.
- CTX-HOME is Ready from `R-003_home_screen_context.md`.
- Unblocked by: `STORY-003_visual_foundation_spec.md`.

## Sprint

Target sprint: Sprint 1.

## User Story

As a user, I want each test card to make the main study action obvious while
keeping edit, export, archive, delete, and restore actions available but quieter.

## Goal

Polish active and archived test cards, including metadata hierarchy, group
placement, action hierarchy, and destructive action treatment.

## Required Context

- `visual_overhaul_project/01_context/summaries/home_screen_context.md`.
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.
- `visual_overhaul_project/01_context/summaries/style_inventory.md`.

## Scope

In:

- Active test cards.
- Archived test cards.
- Card metadata treatment.
- Take Test, Edit, Export, Archive, Delete, Restore action styling.

Out:

- Home toolbar redesign.
- Changing archive/delete confirmation behavior.
- New icons unless explicitly approved.

## Likely Files

- `study_test_tool/gui/test_selector.py`.
- `study_test_tool/gui/components/collapsible_group.py` if group headers need
  card alignment support.

## Implementation Steps

1. Read CTX-HOME, CTX-FOUNDATION, and completed card/button handoffs.
2. Inspect only the test-card and card-action regions named by CTX-HOME.
3. Apply card/list, metadata, status, and action hierarchy rules to home test
   cards.
4. Preserve take, edit, export, archive, delete, restore, and group behavior.
5. Verify populated, grouped, archived, light, dark, and minimum-window states.
6. Document any card states that could not be checked.

## Acceptance Criteria

- Take Test is the clear primary card action.
- Utility actions are visible but lower emphasis.
- Delete remains clearly destructive.
- Archived cards are visually distinct without becoming hard to read.
- Metadata is easy to scan and does not wrap awkwardly at minimum width.

## Verification

- Visual check for grouped, ungrouped, archived, and empty states.
- Smoke check card actions still call the same workflows.
- Run relevant tests if behavior-bearing code is touched.

## Dev 2 Assignment Notes

- Do not change card data, sorting, group behavior, or action callbacks.
- Do not redesign the overall home shell; that belongs to STORY-008.
- If card/list patterns are not defined yet, return this story to Blocked.

## Handoff Requirements

- List card states checked.
- List any action-role decisions added to foundation docs.
