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
It has now been superseded for implementation planning by
`baseline_visual_audit.md` and `visual_foundation_decisions.md`; keep this file
only as early seed context.

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

- Minimum window layout behavior has not been verified.
- Native message boxes still need separate inventory if a future story replaces
  them with custom dialogs.
- Some detailed runtime states remain uncaptured, including editor validation
  warnings and expanded archived cards.

## Required Follow-Up

Use `baseline_visual_audit.md`, `style_inventory.md`, and
`visual_foundation_decisions.md` before assigning implementation stories.

## Refresh Triggers

Refresh only if implementation planning still relies on this seed summary after
the baseline audit or visual foundation changes.
