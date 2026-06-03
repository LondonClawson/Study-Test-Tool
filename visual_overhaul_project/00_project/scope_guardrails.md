# Scope Guardrails

## Hard Boundaries

Do not change these during MVP visual overhaul work:

- Database schema or migrations.
- Scoring service behavior.
- Import/export contracts.
- PDF/DOCX parsing behavior.
- Test session locking, timing, flagging, or mixed-test scoring behavior.
- Navigation model beyond local layout polish.
- Application framework.

## Allowed Visual Changes

- Replace inline colors with shared visual tokens.
- Adjust padding, margins, row heights, and card structure.
- Improve button role styling.
- Improve page headers and section headers.
- Improve status labels and badges.
- Improve empty/loading/error presentation.
- Improve chart colors and label presentation without changing analytics data.

## When To Stop And Ask

Stop and request a product decision if a visual change would:

- Remove or rename a user-facing action.
- Change the order of a workflow.
- Hide a destructive action behind a new interaction model.
- Require new persisted user settings.
- Require a new dependency.
- Require replacing a CustomTkinter control with a substantially different
  behavior model.

## Scope Split Rule

Split the work when a task includes more than one of these:

- A shared component family.
- A major screen.
- A dialog group.
- A test or verification harness change.
- A new design-system decision.

The preferred unit is one component family or one screen pass.
