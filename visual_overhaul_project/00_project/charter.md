# Visual Overhaul Project Charter

## Mission

Make Study Testing Tool feel like a polished macOS-oriented study product while
preserving current behavior. The work should improve visual hierarchy,
readability, spacing, alignment, action clarity, cards/lists, empty states, and
light/dark usability.

## Source Of Truth

- Primary visual plan: `VISUAL_OVERHAUL_PLAN.md`.
- Current app behavior: live code under `study_test_tool/`.
- Testing expectations: `study_test_tool/tests/`.
- Agent rules: `AGENTS.md`.

Older planning documents may be useful background, but they are not authoritative
where they conflict with the live app.

## MVP Outcome

The MVP is complete when the app no longer reads as default CustomTkinter output
and the main study flows have consistent visual hierarchy across light and dark
mode.

Required MVP screens:

- Home/test selector.
- Test taking.
- Results.
- Test editor.
- History.
- Analytics.
- Review.
- Mode selection, mix test, import/error/confirmation dialogs where practical.

## In Scope

- Visual foundation: colors, type scale, spacing scale, radii, surfaces, borders,
  button roles, status badges, cards, list rows, page headers, and empty states.
- Shared GUI component polish in `study_test_tool/gui/components/`.
- Screen layout polish for existing workflows.
- Screenshot audits and context summaries.
- Focused tests or manual verification where visual changes risk behavior.

## Out Of Scope For MVP

- Scoring behavior changes.
- Import/export behavior changes.
- Database schema changes.
- Test session behavior changes.
- New study features.
- Full navigation redesign.
- Landing page or marketing layout.
- Replacement of CustomTkinter.
- Broad icon system unless one icon solves a specific usability problem.

## Success Measures

- Primary actions are obvious and secondary actions no longer compete visually.
- Repeated surfaces share consistent padding, radius, borders, and text treatment.
- Test-taking is more readable and answer choices feel selectable.
- Results, history, analytics, and review screens feel intentionally designed.
- Empty, loading, and error states are consistent.
- Light and dark modes remain readable at the minimum supported window size.
