# STORY-016: Light/Dark And Minimum-Size Validation

## Status

Blocked.

## Readiness

- Blocked by: completion of core MVP screen stories.
- Unblocked by: `STORY-008` through `STORY-015`.

## Sprint

Target sprint: Sprint 4.

## User Story

As a user, I want the app to remain readable and usable in light mode, dark mode,
and at the minimum supported window size.

## Goal

Validate the completed MVP visual work across appearance modes and minimum
window constraints, then create targeted follow-up fixes.

## Required Context

- `visual_overhaul_project/01_context/summaries/baseline_visual_audit.md`.
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.
- Handoffs from completed screen stories.

## Scope

In:

- Light/dark review of every MVP screen.
- Minimum size review at `MIN_WINDOW_WIDTH` and `MIN_WINDOW_HEIGHT`.
- Text clipping, overlap, and contrast checks.
- Follow-up story creation for issues found.

Out:

- Broad redesign.
- New features.
- Post-MVP icon or branding work.

## Likely Files

- Documentation under `visual_overhaul_project/`.
- GUI files only if small validation fixes are explicitly included in sprint
  planning.

## Implementation Steps

1. Read completed MVP story handoffs, CTX-FOUNDATION, baseline audit, and the
   screenshot checklist.
2. Run a light-mode, dark-mode, and minimum-window pass across MVP screens.
3. Record failures as concrete screen/state follow-ups.
4. Update acceptance matrix evidence.
5. Do not fix issues in this validation story unless the PM explicitly assigns a
   small follow-up.
6. Write a closeout handoff with pass/fail status and remaining risks.

## Acceptance Criteria

- Every MVP screen is checked in light and dark mode.
- Every MVP screen is checked at minimum supported size.
- Clipping, overlap, unreadable contrast, and broken scroll behavior are logged.
- Small fixes are completed if within sprint scope; larger issues become
  follow-up stories.

## Verification

- Screenshot comparison or written visual checklist for every MVP screen.
- Automated tests only if code fixes are made.

## Dev 2 Assignment Notes

- This is validation work, not a broad fix-it pass.
- Do not change application code unless a separate follow-up story is assigned.
- If completed story handoffs are missing, return this story to Blocked.

## Handoff Requirements

- Include validation matrix.
- List issues fixed.
- List follow-up issues with priority.
