# Status Transition Rules

Use this with `status_board.md`, `context_index.md`, and story or research task
handoffs. Status changes are project-management decisions, not incidental edits.

## Owners

- PM assigns work and moves items to In Progress.
- Research Agent updates the output summary and proposes status changes in the
  handoff.
- Implementation Agent updates the story handoff and proposes status changes in
  the handoff.
- Reviewer or PM marks summaries, research tasks, and stories Ready, Done, or
  Changes Requested.

## Research Task Transitions

- Ready to In Progress: PM assigns the task to Dev 1.
- In Progress to Submitted For Review: Dev 1 completes the summary, handoff,
  context index updates, and status board updates for reviewer acceptance.
- In Progress to Done: reviewer accepts the summary, handoff, context index, and
  status board updates.
- In Progress to Blocked: Dev 1 cannot inspect required files, screens, or app
  states and documents the blocker.

## Context Summary Transitions

- Missing to Ready: reviewer confirms the summary passes the Context Summary
  Ready gate.
- Missing to Submitted For Review: research agent creates the summary and
  proposes it for reviewer acceptance.
- Submitted For Review to Ready: reviewer confirms the summary passes the
  Context Summary Ready gate.
- Seeded to Ready: reviewer confirms the seeded summary is refreshed enough to
  replace task-specific research for dependent stories.
- Ready to Stale: source files changed, design decisions changed, or a story
  needs states the summary does not cover.

## Implementation Story Transitions

- Blocked to Ready: all required summaries are Ready and the story passes the
  Implementation Story Ready gate.
- Ready to In Progress: PM assigns the story to Dev 2.
- In Progress to Submitted For Review: Dev 2 completes the implementation,
  required screenshot evidence or documented capture blocker, verification
  notes, and handoff.
- Submitted For Review to Done: reviewer accepts the implementation, required
  screenshot evidence or documented capture blocker, verification notes, and
  handoff.
- Submitted For Review to Changes Requested: reviewer or PM finds required
  fixes, missing verification, missing screenshot evidence, or acceptance gaps
  and documents the requested changes in the handoff.
- Changes Requested to In Progress: PM returns the story to Dev 2 for the named
  fixes or evidence.
- Changes Requested to Done: reviewer accepts the resubmitted fixes, evidence,
  verification notes, and handoff.
- In Progress to Blocked: Dev 2 finds missing/stale context, unclear scope, or a
  required product decision.

## Required Updates

Whenever status changes, update all relevant files:

- `00_project/status_board.md`.
- `01_context/context_index.md` for summary status changes.
- The owning research task or story file if readiness language changed.
- The handoff note for the completed or blocked assignment.
