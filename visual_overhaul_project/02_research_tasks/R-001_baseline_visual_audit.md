# R-001: Baseline Visual Audit

## Status

Ready.

## Role

Assign to Dev 1 Research Agent. This is not an implementation task.

## Goal

Capture the current visual state of the app in light and dark mode so MVP work
can be compared against a real baseline.

## Output

Write the summary to:

```text
visual_overhaul_project/01_context/summaries/baseline_visual_audit.md
```

Save screenshots under:

```text
visual_overhaul_project/01_context/screenshots/baseline/
```

Use subfolders `light/` and `dark/` if both modes are captured.

## Required Inputs

- `VISUAL_OVERHAUL_PLAN.md`.
- `visual_overhaul_project/01_context/summaries/gui_architecture_summary.md`.
- `visual_overhaul_project/01_context/summaries/screen_inventory.md`.
- `visual_overhaul_project/06_handoffs/screenshot_checklist.md`.

## Screens To Capture

Use `visual_overhaul_project/06_handoffs/screenshot_checklist.md` as the
checklist for this section.

- Home/test selector with populated tests.
- Home/test selector empty state if practical.
- Test editor.
- Test taking in normal mode.
- Test taking in practice mode after feedback.
- Results.
- History.
- Analytics.
- Review.
- Mode selection dialog.
- Mix test dialog.
- Import, error, or confirmation dialog where practical.

## Do Not Change

- Do not change application code.
- Do not make visual design decisions.
- Do not fix UI issues found during the audit.
- Do not change local data except temporary setup needed to capture states.

## Screenshot Naming

Use descriptive ASCII file names that include mode and screen, for example:

```text
light_home_populated.png
dark_test_taking_practice_feedback.png
light_mode_dialog.png
```

If a state cannot be captured, list it in the summary with the reason instead of
guessing.

## Research Steps

1. Start the app using the repository instructions.
2. Prepare enough test data to show realistic states. Use existing local data if
   available, or import/create temporary tests.
3. Capture each screen in light mode.
4. Capture each screen in dark mode.
5. For each screen, assess hierarchy, spacing, alignment, readability, action
   clarity, card/list polish, empty/loading/error state, and default-widget
   appearance.
6. Check minimum-window usability where practical and record any clipping,
   overlap, wrapping, or inaccessible controls.
7. Record app-wide issues separately from screen-specific issues.
8. Add screenshot file names to the summary.
9. Write a Dev 2 Quick Start section that explains which screenshots and issues
   future implementation stories should consult first.

## Summary Must Include

- Capture date and environment.
- Data setup used.
- Screenshot inventory.
- App-wide findings.
- Per-screen findings.
- Light/dark differences.
- Minimum window concerns if checked.
- Priority issues that should shape the visual foundation.
- Screens or states that were not captured and why.
- Recommendations for which findings belong in foundation work vs screen work.
- Dev 2 Quick Start notes.
- Blockers or missing states.

## Done Criteria

- The summary file exists.
- Screenshots are stored in the target folder or missing screenshots are
  explicitly explained.
- `01_context/context_index.md` status for CTX-AUDIT-BASELINE is updated.
- `00_project/status_board.md` is updated.
- The handoff lists screenshot folders, missing states, setup data, and runtime
  blockers.
- The summary passes `00_project/definition_of_ready.md`.
