# R-002: Component And Style Inventory

## Status

Done.

## Role

Assign to Dev 1 Research Agent. This is not an implementation task.

## Goal

Inventory current visual constants, inline styling, repeated components, and
visual duplication so the visual foundation solves observed problems.

## Output

Write the summary to:

```text
visual_overhaul_project/01_context/summaries/style_inventory.md
```

Update these seed summaries if new facts are found:

```text
visual_overhaul_project/01_context/summaries/gui_architecture_summary.md
visual_overhaul_project/01_context/summaries/screen_inventory.md
```

## Required Inputs

- `visual_overhaul_project/01_context/summaries/current_visual_state_seed.md`.
- `study_test_tool/config/settings.py`.
- `study_test_tool/gui/`.

## Source Files

Inspect:

- `study_test_tool/config/settings.py`.
- All files under `study_test_tool/gui/`.
- `study_test_tool/utils/constants.py` for screen names and modes.

## Do Not Change

- Do not change application code.
- Do not introduce new constants, components, or style helpers.
- Do not decide the final visual foundation.
- Do not update implementation stories except to note blockers or follow-ups in
  the handoff.

## Search Targets

Use static inspection and targeted searches for:

- `fg_color`, `bg_color`, `hover_color`, `text_color`, `border_color`.
- `corner_radius`, `border_width`, `font`, `padx`, `pady`.
- Hard-coded status colors, grays, reds, greens, yellows, and chart colors.
- Repeated `CTkFrame`, `CTkButton`, `CTkLabel`, `CTkScrollableFrame`,
  `CTkTabview`, list row, card, badge, and dialog patterns.

## Research Steps

1. List existing color constants and font constants.
2. Search for inline `fg_color`, `hover_color`, `text_color`, `corner_radius`,
   font tuples, and hard-coded gray/status colors.
3. Group findings by semantic role: primary, secondary, tertiary, danger,
   warning, success, muted, status, surface, border, chart.
4. Identify repeated surfaces: page headers, action bars, cards, rows, badges,
   empty states, progress indicators, dialogs, form labels.
5. Identify where shared components already exist and where screen-local
   duplication should remain local.
6. Note any CustomTkinter constraints that should affect the foundation.
7. Separate observed facts from recommendations.
8. Write a Dev 2 Quick Start section for `STORY-003` and later foundation
   stories.

## Summary Must Include

- Current constants.
- Inline style inventory by file.
- Repeated visual patterns.
- Candidate shared tokens.
- Candidate shared components or helper functions.
- Risks from centralizing too much.
- Recommended first foundation changes.
- Recommended story splits if one foundation story is too broad.
- Dev 2 Quick Start notes.

## Done Criteria

- `style_inventory.md` exists.
- It gives enough detail for `STORY-003_visual_foundation_spec.md`.
- Context index status for CTX-STYLE-INVENTORY is updated.
- `00_project/status_board.md` is updated.
- The handoff lists source files inspected, search terms used, and any files or
  states not inspected.
- The summary passes `00_project/definition_of_ready.md`.
