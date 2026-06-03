# Visual Overhaul Project Documentation

This directory contains the agile project documentation for the Study Testing
Tool visual overhaul. It is intentionally split into small files so an agent can
work from one task or story file and only the context summaries linked by that
file.

The source plan is [VISUAL_OVERHAUL_PLAN.md](../VISUAL_OVERHAUL_PLAN.md). The
live code under [study_test_tool/gui](../study_test_tool/gui) and the tests are
authoritative when older root documents conflict with the current app.

## How To Use This Documentation

1. Start with `00_project/status_board.md` to see what is ready or blocked.
2. Check `00_project/definition_of_ready.md` before assigning work.
3. Use `03_backlog/dependency_map.md` to choose the next safe assignment.
4. Assign research tasks before implementation stories when context is missing.
5. Read the story or research task assigned to you.
6. Read only the required summaries listed in that file.
7. If a required summary is missing or stale, complete the linked research task
   first and write the updated summary to the specified location.
8. Keep implementation work inside the story scope.
9. Before handoff, update the story status, any touched summaries, and the
   handoff note.

## Directory Map

- `00_project/` - project rules, scope, risks, and agile operating model.
- `01_context/` - reusable context summaries and the context index.
- `02_research_tasks/` - narrow research tasks that produce context summaries.
- `03_backlog/` - backlog index, story template, and acceptance matrix.
- `04_stories/` - task-sized agile stories for implementation or design work.
- `05_sprints/` - sprint sequencing and exit criteria.
- `06_handoffs/` - handoff and review checklists.

## Fast Navigation

- Current state: [status_board.md](00_project/status_board.md).
- Definition of Ready:
  [definition_of_ready.md](00_project/definition_of_ready.md).
- Status transitions:
  [status_transition_rules.md](00_project/status_transition_rules.md).
- Dependency planning: [dependency_map.md](03_backlog/dependency_map.md).
- Context lookup: [context_index.md](01_context/context_index.md).
- Story queue: [backlog_index.md](03_backlog/backlog_index.md).
- Assignment template:
  [assignment_packet_template.md](06_handoffs/assignment_packet_template.md).
- Sprint 0 assignment packets:
  [sprint_00_assignment_packets.md](06_handoffs/sprint_00_assignment_packets.md).
- Handoff template: [handoff_template.md](06_handoffs/handoff_template.md).

## Project Rule

This project changes the visual presentation of the desktop app. It must not
change scoring, import/export behavior, database schema, test session behavior,
or core workflows unless a separate non-visual product decision is approved.
