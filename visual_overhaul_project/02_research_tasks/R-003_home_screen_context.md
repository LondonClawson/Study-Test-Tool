# R-003: Home Screen Context

## Status

Done. R-002 is Done, and this task produced the home screen context summary
before home implementation stories.

## Role

Assign to Dev 1 Research Agent before home implementation stories.

## Goal

Create focused context for home/test selector visual work, including test cards,
group headers, toolbar actions, sort controls, and home-launched dialogs.

## Output

Write the summary to:

```text
visual_overhaul_project/01_context/summaries/home_screen_context.md
```

## Required Inputs

- `visual_overhaul_project/01_context/summaries/gui_architecture_summary.md`.
- `visual_overhaul_project/01_context/summaries/current_visual_state_seed.md`.
- `VISUAL_OVERHAUL_PLAN.md`.

## Source Files

- `study_test_tool/gui/test_selector.py`.
- `study_test_tool/gui/components/collapsible_group.py`.
- `study_test_tool/gui/components/mode_dialog.py`.
- `study_test_tool/gui/components/mix_test_dialog.py`.
- Services only as needed to understand data shown on cards, not to redesign
  behavior.

## Do Not Change

- Do not change application code.
- Do not redesign the home screen.
- Do not change import/export, archive, delete, restore, mix, review, history,
  analytics, or take-test behavior.

## Research Steps

1. Map the home screen structure: title, top action bar, sort toolbar, groups,
   test cards, archived cards, empty state.
2. List every user action and its current visual weight.
3. Identify populated, grouped, archived, and empty states.
4. Note what data appears on each test card.
5. Identify current color and spacing decisions.
6. Capture behavior constraints for import, new test, mix test, review, history,
   analytics, take test, edit, export, archive, delete, restore.

## Summary Must Include

- Home workflow map.
- Current widget structure.
- Action hierarchy recommendation.
- Visual issues by state.
- Required card/list/group patterns.
- Risks and behavior constraints.
- Open design questions.
- Recommended split between layout work and test-card/action work.
- Dev 2 Quick Start notes.

## Done Criteria

- `home_screen_context.md` exists.
- It names exact methods or UI regions future home stories should inspect.
- Context index status for CTX-HOME is updated.
- `00_project/status_board.md` is updated.
- The handoff lists source files inspected and states not inspected.
- The summary passes `00_project/definition_of_ready.md`.
