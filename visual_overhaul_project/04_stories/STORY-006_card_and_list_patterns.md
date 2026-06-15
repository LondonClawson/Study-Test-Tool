# STORY-006: Card And List Patterns

## Status

Blocked.

## Readiness

- Blocked by: a named pilot area.
- Unblocked by: PM approval of the pilot area.

CTX-FOUNDATION and `STORY-004_shared_style_entrypoints.md` are Done. This story
is still blocked until PM names one narrow card/list pilot area.

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
- One named pilot implementation area.

Out:

- Redesigning every card in the app at once.
- Data model changes.
- New interaction behavior.

## Likely Files

- Shared style entry points.
- One named pilot screen or component, such as home test cards or results review
  cards.

## Implementation Steps

1. Confirm the assignment packet names one pilot area.
2. Read CTX-FOUNDATION and the context summary for the pilot area.
3. Define card/list rules for padding, border, radius, title, metadata, status,
   and actions.
4. Apply the pattern only to the named pilot area.
5. Verify light/dark mode and the named pilot states.
6. Document reusable rules and screen-specific exceptions.

## Acceptance Criteria

- The card/list pattern is documented and reusable.
- The pilot area visibly follows the pattern.
- The assignment packet names the pilot area before work starts.
- Card content remains at least as scannable as before.
- No unrelated cards are partially migrated without verification.

## Verification

- Visual check of pilot area in light and dark mode.
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
