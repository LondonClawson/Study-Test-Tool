# Research Task Template

Use this template when adding a new research task under `02_research_tasks/`.
Research tasks are Dev 1 assignments. They produce context for Dev 2 and must
not become implementation work.

```text
# R-000: Short Research Name

## Status

Proposed.

## Role

Assign to Dev 1 Research Agent. This is not an implementation task.

## Goal

Describe the focused context this task must produce and which future stories it
unblocks.

## Output

Write the summary to:

visual_overhaul_project/01_context/summaries/example_context.md

## Required Inputs

-

## Source Files

Inspect:

-

## Screens Or States To Inspect

-

## Do Not Change

- Do not change application code.
- Do not redesign the screen or component.
- Do not change behavior, data flow, persistence, scoring, import/export, or
  navigation.

## Research Steps

1. Read the required inputs.
2. Inspect the listed source files and screens.
3. Map workflows, UI states, callbacks, and behavior constraints.
4. Record visual findings as observed facts.
5. Separate recommendations from observed facts.
6. Recommend implementation story splits if needed.
7. Write a Dev 2 Quick Start section.
8. Update context index and status board statuses.

## Summary Must Include

- Producing research task.
- Source files and screens inspected.
- Screens or states not inspected and why.
- Workflow and state map.
- Current widget structure.
- Visual findings.
- Recommendations and story split guidance.
- Behavior constraints.
- Implementation risks.
- Open questions.
- Dev 2 Quick Start notes.

## Done Criteria

- The output summary exists.
- The summary passes `00_project/definition_of_ready.md`.
- `01_context/context_index.md` is updated.
- `00_project/status_board.md` is updated.
- The handoff lists files inspected, states inspected, states skipped, risks,
  and follow-ups.
```
