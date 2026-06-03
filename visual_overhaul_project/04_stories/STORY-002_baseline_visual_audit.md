# STORY-002: Baseline Visual Audit

## Status

Ready.

## Readiness

- Blocked by: None.
- Unblocked by: N/A.

## Sprint

Target sprint: Sprint 0.

## PM Assignment Note

This is a coordination wrapper, not an implementation story. Assign
`R-001_baseline_visual_audit.md` to Dev 1 for the actual audit work.

## User Story

As the project manager, I want the baseline audit research completed and
reviewed so MVP visual improvements can be compared against the current app.

## Goal

Assign `R-001_baseline_visual_audit.md` to a Dev 1 Research Agent, then review
the screenshot inventory and audit summary for implementation readiness.

## Required Context

- `VISUAL_OVERHAUL_PLAN.md`.
- `visual_overhaul_project/01_context/summaries/gui_architecture_summary.md`.
- `visual_overhaul_project/01_context/summaries/screen_inventory.md`.
- Research task: `visual_overhaul_project/02_research_tasks/R-001_baseline_visual_audit.md`.

## Scope

In:

- Assigning the baseline audit research task.
- Reviewing app-wide baseline screenshots.
- Reviewing per-screen visual audit findings.
- Reviewing light/dark comparison notes.
- Ensuring missing states are documented.

Out:

- Code changes.
- Visual foundation decisions.
- Redesign proposals beyond audit notes.
- Performing implementation work.

## Likely Files

- `visual_overhaul_project/01_context/summaries/baseline_visual_audit.md`.
- `visual_overhaul_project/01_context/screenshots/baseline/`.

## Implementation Steps

1. Assign `R-001_baseline_visual_audit.md` using the research assignment packet
   template.
2. Confirm screenshots are named and stored under the required baseline folder,
   or missing states are explained.
3. Review `baseline_visual_audit.md` against
   `00_project/definition_of_ready.md`.
4. Update context index and status board states.
5. List any blockers that prevent foundation work from starting.

## Acceptance Criteria

- Major screens and key dialogs are captured or explicitly marked unavailable.
- Audit notes separate app-wide issues from screen-specific issues.
- The summary identifies the highest-priority issues that should shape the
  foundation.
- Context index status for CTX-AUDIT-BASELINE is updated.
- The summary includes a Dev 2 Quick Start for foundation and validation work.
- The handoff makes clear that no application code changed.

## Verification

- Documentation and screenshot review.
- No app tests required because this story does not change code.
- Confirm `baseline_visual_audit.md` passes the Context Summary Ready checklist.

## Handoff Requirements

- List screenshot folders and missing states.
- List any setup data used.
- List environment or runtime blockers.
