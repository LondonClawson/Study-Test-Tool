# STORY-017: MVP Visual Regression Pass

## Status

Blocked.

## Readiness

- Blocked by: Sprint 4 validation and completed MVP handoffs.
- Unblocked by: `STORY-016_light_dark_and_min_size_validation.md`.

## Sprint

Target sprint: Sprint 4.

## User Story

As the product owner, I want one final MVP review so that the visual overhaul can
be accepted without hidden workflow or presentation regressions.

## Goal

Close the MVP by comparing before/after evidence, acceptance criteria, tests,
and remaining risks.

## Required Context

- `visual_overhaul_project/03_backlog/acceptance_matrix.md`.
- `visual_overhaul_project/01_context/summaries/baseline_visual_audit.md`.
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.
- Completed story handoffs.

## Scope

In:

- Acceptance matrix review.
- Before/after screenshot comparison.
- Behavior-preservation check.
- Test run summary.
- Final MVP risks and post-MVP backlog recommendations.

Out:

- New visual implementation except small approved closeout fixes.
- Post-MVP iconography, navigation redesign, branding, or micro-interactions.

## Likely Files

- `visual_overhaul_project/06_handoffs/`.
- Acceptance matrix and sprint closeout docs.
- GUI files only for approved closeout fixes.

## Implementation Steps

1. Read the acceptance matrix, baseline audit, foundation decisions, and all MVP
   story handoffs.
2. Compare before/after evidence for every MVP screen.
3. Confirm behavior-preservation evidence is present for touched workflows.
4. Record unresolved visual regressions or missing evidence as follow-up backlog
   items.
5. Update closeout docs and status board states.
6. Write a final MVP handoff summary.

## Acceptance Criteria

- Every acceptance matrix row has evidence or a documented exception.
- Before/after comparison shows clear improvement on priority screens.
- No known core behavior regression remains unaddressed.
- Remaining issues are classified as MVP blocker, post-MVP follow-up, or accepted
  limitation.

## Verification

- Full relevant pytest suite if substantive code changes were made during MVP.
- Manual visual review summary.
- Product owner acceptance or explicit list of blockers.

## Dev 2 Assignment Notes

- This is closeout review work, not new visual implementation.
- Do not make code changes in this story unless a separate closeout-fix
  assignment exists.
- If evidence is missing, document the gap and create a follow-up instead of
  guessing.

## Handoff Requirements

- Final MVP closeout note.
- Test run summary.
- Post-MVP backlog recommendations.
