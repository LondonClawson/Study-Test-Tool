# STORY-006: Card And List Patterns

## Status

Submitted For Review.

## Readiness

- Blocked by: None.
- Unblocked by: PM approval of the pilot area.

CTX-FOUNDATION and `STORY-004_shared_style_entrypoints.md` are Done. This story
is assigned with Home test-card outer surfaces as the narrow pilot area.

Use `visual_overhaul_project/06_handoffs/STORY-006_card_and_list_patterns_assignment.md`
as the assignment packet.

## Sprint

Target sprint: Sprint 1.

## User Story

As a user, I want repeated cards and rows to feel consistent so that test,
question, result, history, analytics, and review content is easy to scan.

## Goal

Create and document MVP card/list row patterns, then apply them to one narrow
component family or pilot area.

This story is not junior-ready until the pilot area is named in the assignment
packet. The preferred default is a single repeated surface that already has a
Ready context summary, such as home test-card outer surfaces after CTX-HOME is
Ready.

## Required Context

- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.
- `visual_overhaul_project/01_context/summaries/style_inventory.md`.
- Relevant screen summary for the pilot area.

## Scope

In:

- Padding, border, radius, title, metadata, action placement, and status
  treatment for repeated surfaces.
- One named pilot implementation area: Home test-card outer surfaces, including
  active cards, archived cards, metadata hierarchy, and the existing card action
  row container.

Out:

- Redesigning every card in the app at once.
- Data model changes.
- New interaction behavior.

## Likely Files

- `study_test_tool/gui/styles.py`.
- `study_test_tool/gui/test_selector.py`.
- `study_test_tool/gui/components/collapsible_group.py` only if the group/card
  spacing boundary needs a local adjustment.

## Implementation Steps

1. Read CTX-FOUNDATION, CTX-STYLE-INVENTORY, CTX-HOME, and the completed
   STORY-004 and STORY-005 handoffs.
2. Define the minimal reusable card style entry points needed for the Home
   test-card pilot: surface, archived surface, border, radius, title,
   description, metadata, and internal padding.
3. Apply the pattern only to Home active and archived test-card outer surfaces
   and text hierarchy.
4. Preserve all existing card actions, callbacks, zero-question disabled Take
   Test behavior, grouping, archive/delete confirmations, sorting, and refresh
   behavior.
5. Verify light/dark readability and the named Home pilot states.
6. Document reusable rules and Home-specific exceptions in the handoff.

## Acceptance Criteria

- The card/list pattern is documented and reusable.
- The pilot area visibly follows the pattern.
- The assignment packet names the pilot area before work starts.
- Active and archived Home test cards use semantic surface, border, radius, and
  text roles from the shared style entry point.
- Card content remains at least as scannable as before.
- No unrelated cards are partially migrated without verification.

## Verification

- Visual check of pilot area in light and dark mode.
- Smoke check Home populated, grouped, archived, and zero-question states where
  practical.
- Relevant tests if callbacks or data display code is touched.

## Dev 2 Assignment Notes

- Do not start until the pilot area is named.
- Do not partially migrate unrelated cards or rows.
- If the pilot area's context summary is missing, stop and assign the linked
  research task.

## Handoff Requirements

- Identify the pilot area.
- Document what pattern rules are ready for other stories.
- Document what remains screen-specific.
