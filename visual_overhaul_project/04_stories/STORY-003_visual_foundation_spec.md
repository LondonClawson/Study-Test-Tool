# STORY-003: Visual Foundation Spec

## Status

Done.

## Readiness

- Blocked by: None.
- Unblocked by: `STORY-001_context_batch_one.md`,
  `STORY-002_baseline_visual_audit.md`, and PM/reviewer acceptance.

PM review accepted CTX-AUDIT-BASELINE and CTX-FOUNDATION on 2026-06-15.

## Sprint

Target sprint: Sprint 1.

## User Story

As an implementation agent, I want approved visual foundation decisions so that
screen work can use consistent colors, typography, spacing, buttons, cards, and
states.

## Goal

Turn the audit and style inventory into a documented foundation for MVP visual
implementation.

## Required Context

- `visual_overhaul_project/01_context/summaries/baseline_visual_audit.md`.
- `visual_overhaul_project/01_context/summaries/style_inventory.md`.
- `visual_overhaul_project/01_context/summaries/current_visual_state_seed.md`.
- `VISUAL_OVERHAUL_PLAN.md`.

## Scope

In:

- App background, surfaces, borders, text colors, action colors, and status
  colors for light and dark mode.
- Spacing, radius, and typography rules.
- Page header, card/list row, badge, empty/loading/error, and chart color rules.
- Guidance for where implementation should centralize reusable values.

Out:

- Code changes.
- Icon system.
- Navigation redesign.
- Branding pass.

## Likely Files

- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.

## Implementation Steps

1. Read the baseline audit, style inventory, current visual seed, and source
   plan.
2. Extract foundation decisions from observed research facts.
3. Write semantic roles for color, text, spacing, surfaces, buttons, cards,
   rows, badges, empty states, and chart colors.
4. Record unresolved choices as open decisions, not assumptions.
5. Update context index and status board readiness for CTX-FOUNDATION.
6. Write a handoff naming stories unblocked and decisions still open.

## Acceptance Criteria

- The foundation names semantic roles rather than only raw colors.
- Light and dark mode are both covered.
- Rules are specific enough for implementation stories to apply without a new
  design decision.
- Scope limits and CustomTkinter constraints are documented.
- Any unresolved choices are listed as decisions needed.

## Verification

- Documentation review against `VISUAL_OVERHAUL_PLAN.md`.
- No app tests required because this story does not change code.

## Dev 2 Assignment Notes

- Do not change application code in this story.
- Do not invent visual rules that conflict with completed research summaries.
- If audit or style inventory summaries are missing or weak, return this story
  to Blocked and assign the missing research work.

## Handoff Requirements

- List approved decisions.
- List decisions still open.
- List stories unblocked by the foundation.
