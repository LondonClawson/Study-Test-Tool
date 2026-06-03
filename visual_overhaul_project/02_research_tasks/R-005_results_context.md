# R-005: Results Context

## Status

Blocked until R-001 or R-002 is Done. Assign before results implementation
stories.

## Role

Assign to Dev 1 Research Agent before results implementation stories.

## Goal

Create focused context for results view visual work, including score summary,
details metadata, question review cards, answer comparison, status treatment,
retake behavior, history-loaded results, and mix-test source breakdown.

## Output

Write the summary to:

```text
visual_overhaul_project/01_context/summaries/results_context.md
```

## Required Inputs

- `visual_overhaul_project/01_context/summaries/gui_architecture_summary.md`.
- `visual_overhaul_project/01_context/summaries/current_visual_state_seed.md`.
- `VISUAL_OVERHAUL_PLAN.md`.

## Source Files

- `study_test_tool/gui/results_view.py`.
- `study_test_tool/services/scoring_service.py` only as needed to understand
  displayed score data.
- `study_test_tool/tests/test_scoring_service.py`.
- `study_test_tool/tests/test_mix_service.py`.

## Do Not Change

- Do not change application code.
- Do not redesign the results screen.
- Do not change scoring, attempt persistence, history loading, retake behavior,
  or mix-test source attribution.

## Research Steps

1. Map the two entry modes: just-completed session and history attempt.
2. Identify result states: all correct, partially correct, essay questions,
   flagged questions, missing answers, mixed-test breakdown.
3. Inventory current score header, detail metadata, buttons, review cards, and
   answer comparison layout.
4. Identify behavior that must not change when visual card structure changes.
5. Note where status badges or structured answer panels would improve scan.

## Summary Must Include

- Results workflow map.
- Current widget structure.
- Data fields shown in each state.
- Visual issues and recommended hierarchy.
- Behavior constraints.
- Verification requirements.
- Recommended split if summary/header and review-card work should be separate.
- Dev 2 Quick Start notes.

## Done Criteria

- `results_context.md` exists.
- It gives enough detail for score-summary and review-card stories.
- Context index status for CTX-RESULTS is updated.
- `00_project/status_board.md` is updated.
- The handoff lists source files inspected and states not inspected.
- The summary passes `00_project/definition_of_ready.md`.
