# Assignment Packet Template

Use this when giving one agent one task. Keep the packet short and point to the
single story or research file that owns the work.

Choose the packet type based on the role:

- Research packets assign Dev 1 to produce context.
- Implementation packets assign Dev 2 to consume completed context.

```text
Assignment:
Role:

Primary file:

Read these context summaries first:

Do this:

Do not do this:

Expected output:

Required verification:

Handoff location:

Notes:
```

## Research Example

```text
Assignment: Complete the home screen context research.
Role: Dev 1 Research Agent

Primary file:
visual_overhaul_project/02_research_tasks/R-003_home_screen_context.md

Read these context summaries first:
visual_overhaul_project/01_context/summaries/gui_architecture_summary.md
visual_overhaul_project/01_context/summaries/current_visual_state_seed.md

Do this:
Inspect the home screen files and write home_screen_context.md.

Do not do this:
Do not change application code or redesign the home screen.

Expected output:
visual_overhaul_project/01_context/summaries/home_screen_context.md

Required verification:
Documentation review only.

Handoff location:
Use visual_overhaul_project/06_handoffs/handoff_template.md.
```

## Implementation Example

```text
Assignment: Polish the home screen layout.
Role: Dev 2 Implementation Agent

Primary file:
visual_overhaul_project/04_stories/STORY-008_home_screen_layout.md

Read these context summaries first:
visual_overhaul_project/01_context/summaries/home_screen_context.md
visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md

Do this:
Use the Dev 2 Quick Start in the summaries, then complete only the scoped layout
work in STORY-008.

Do not do this:
Do not redo broad GUI research, redesign test cards, or change import/export,
navigation, persistence, scoring, or test-session behavior.

Expected output:
Completed story scope, updated story status, and a handoff note.

Required verification:
Check populated home, empty home, grouped/collapsed states, toolbar action smoke
checks, light mode, dark mode, and minimum window fit.

Handoff location:
Use visual_overhaul_project/06_handoffs/handoff_template.md.

Notes:
If the required summaries are missing or stale, stop and assign the linked
research task instead.
```
