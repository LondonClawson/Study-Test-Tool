# Research Backlog

## Purpose

Research backlog items produce reusable summaries. They should not become broad
implementation tasks.

Research is first-class project work. Assign these tasks to Dev 1 before
assigning dependent implementation stories to Dev 2.

Use `00_project/status_board.md` for current task state and
`03_backlog/dependency_map.md` for what each research task unblocks.
Use `02_research_tasks/research_task_template.md` for new research tasks.

## Research Task Queue

| Task | Output Summary | Needed Before | Assignment Gate |
| --- | --- | --- | --- |
| `R-001_baseline_visual_audit.md` | `baseline_visual_audit.md` | Visual foundation and MVP comparison | Ready now |
| `R-002_component_style_inventory.md` | `style_inventory.md` | Visual foundation and shared style work | Ready now |
| `R-003_home_screen_context.md` | `home_screen_context.md` | Home screen stories | R-001 or R-002 Done |
| `R-004_test_taking_context.md` | `test_taking_context.md` | Test-taking stories | R-001 or R-002 Done |
| `R-005_results_context.md` | `results_context.md` | Results stories | Done |
| `R-006_editor_context.md` | `editor_context.md` | Editor story | Done |
| `R-007_history_analytics_review_context.md` | `history_analytics_review_context.md` | Secondary screen stories | R-001 or R-002 Done |
| `R-008_dialog_context.md` | `dialog_context.md` | Dialog story | R-001 Done |

## Research Splitting Rule

If a research task takes more than one screen family, split it into a smaller
task and add the new summary to `01_context/context_index.md`.

The research agent should recommend implementation story splits when a future
story would otherwise cover multiple screens or unrelated component families.

## Research Output Quality

A useful summary should be direct enough that an implementation agent can read it
in a few minutes and know which source methods, states, and risks matter.

Each summary must pass `00_project/definition_of_ready.md` before it unblocks an
implementation story.
