# Change Control

## Purpose

This project should protect current functionality while improving visuals. Change
control keeps product behavior decisions separate from visual implementation.

## Change Request Triggers

Create a change request or backlog follow-up when work would require:

- A new feature.
- A changed workflow.
- A changed persistence model.
- A new dependency.
- A renamed or removed action.
- A navigation redesign.
- A major design-system decision not covered by the visual foundation.

## Lightweight Change Request Format

Use this format in a handoff note or backlog item:

```text
Change Request:
Reason:
Current behavior:
Proposed change:
Affected screens/files:
Risk:
Decision needed:
```

## Decision Outcomes

- Approved for current story: update the story acceptance criteria before work
  continues.
- Approved for later sprint: add or update a backlog story.
- Rejected: keep current behavior and document the rejected option in the handoff.
- Needs research: create a research task with a specific summary output.
