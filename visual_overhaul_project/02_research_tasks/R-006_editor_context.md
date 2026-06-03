# R-006: Editor Context

## Status

Blocked until R-001 or R-002 is Done. Assign before editor implementation
stories.

## Role

Assign to Dev 1 Research Agent before editor implementation stories.

## Goal

Create focused context for test editor visual work, including test metadata,
question list cards, add/edit form states, multiple-choice option rows, essay
expected answer, validation, and save/cancel actions.

## Output

Write the summary to:

```text
visual_overhaul_project/01_context/summaries/editor_context.md
```

## Required Inputs

- `visual_overhaul_project/01_context/summaries/gui_architecture_summary.md`.
- `visual_overhaul_project/01_context/summaries/current_visual_state_seed.md`.
- `VISUAL_OVERHAUL_PLAN.md`.

## Source Files

- `study_test_tool/gui/test_editor.py`.
- `study_test_tool/gui/components/autocomplete_entry.py`.
- `study_test_tool/tests/test_group_sort.py` if group behavior is relevant.
- Service files only as needed to understand displayed fields.

## Do Not Change

- Do not change application code.
- Do not redesign the editor screen.
- Do not change validation, save/cancel behavior, question ordering, group
  behavior, or persisted test/question data.

## Research Steps

1. Map editor states: new test, edit existing test, no questions, question list,
   adding question, editing question, multiple-choice, essay, validation warning.
2. Identify current two-column layout behavior and minimum-size risks.
3. Inventory current buttons and their roles.
4. Document current question card contents and actions.
5. Note visual opportunities that preserve dense editing efficiency.

## Summary Must Include

- Editor workflow/state map.
- Current widget structure.
- Visual issues by region.
- Action hierarchy recommendation.
- Behavior constraints and validation risks.
- Verification requirements.
- Recommended split if metadata, question list, and form work should be separate.
- Dev 2 Quick Start notes.

## Done Criteria

- `editor_context.md` exists.
- It gives enough detail for an editor layout story.
- Context index status for CTX-EDITOR is updated.
- `00_project/status_board.md` is updated.
- The handoff lists source files inspected and states not inspected.
- The summary passes `00_project/definition_of_ready.md`.
