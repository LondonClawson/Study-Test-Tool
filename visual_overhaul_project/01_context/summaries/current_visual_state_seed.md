# Current Visual State Seed Summary

## Metadata

- Summary ID: CTX-VISUAL-SEED.
- Created: 2026-06-02.
- Last updated: 2026-06-02.
- Produced by: initial static code read plus `VISUAL_OVERHAUL_PLAN.md`.
- Source files inspected: `VISUAL_OVERHAUL_PLAN.md`, `config/settings.py`,
  `gui/main_window.py`, `gui/test_selector.py`, `gui/test_taking.py`,
  `gui/results_view.py`, and component inventory.

## Purpose

This is a seed summary, not a finished audit. It captures known visual issues
from the plan and static code so Sprint 0 research agents can start quickly.
Replace or augment it after the baseline screenshot audit.

## Static Findings

The visual plan identifies scattered styling, inconsistent button weight,
inconsistent color use, default-looking cards, uneven patterns across results,
history, analytics, and plain empty/loading states.

The static code read supports those findings:

- `config/settings.py` contains basic color and font constants, but many GUI
  files still use inline colors such as gray, purple, green, orange, and red.
- `main_window.py` uses CustomTkinter `blue` theme and system appearance.
- Buttons often use equal size and similar placement even when their semantic
  roles differ.
- Cards use `CTkFrame` with small radii, but card padding, metadata treatment,
  and action placement vary by screen.
- Empty states are frequently gray labels.
- Multiple-choice answers in `QuestionWidget` are radio buttons plus labels,
  not full selectable answer rows.
- `GraphWidget` has its own light/dark colors that are separate from app-level
  tokens.

## Screen-Level First Pass

- Home: top button bar mixes import, creation, mix test, review, history, and
  analytics. Test cards include many same-weight actions. Groups use a text
  button as a header.
- Test taking: the top bar carries title, timer, progress, and flag state.
  Bottom navigation uses previous, next, practice check answer, and finish. The
  finish button currently uses a danger color even though finishing is a normal
  end-of-flow action.
- Results: score header is simple text. Review cards exist, but status,
  answer comparison, and mix-test breakdown need stronger scanability.
- Editor: two-column layout exists and has many form states. It likely needs
  organization and hierarchy without losing density.
- History/analytics/review: data views use basic rows/cards and gray empty text.
  Charts require theme alignment.

## Unknowns

- Actual screenshots in light and dark mode have not been captured.
- Minimum window layout behavior has not been verified.
- Populated and empty state visuals need runtime inspection.
- Dialog behavior and native message boxes need separate inventory.

## Required Follow-Up

Run `02_research_tasks/R-001_baseline_visual_audit.md` and
`02_research_tasks/R-002_component_style_inventory.md` before writing the visual
foundation spec.

## Refresh Triggers

Replace this seed summary after baseline screenshots are captured or after the
visual foundation is approved.
