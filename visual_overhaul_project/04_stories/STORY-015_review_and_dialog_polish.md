# STORY-015: Review And Dialog Polish

## Status

Blocked.

## Readiness

- Blocked by: CTX-DATA-VIEWS, CTX-DIALOGS, CTX-FOUNDATION.
- Unblocked by: `R-007_history_analytics_review_context.md`,
  `R-008_dialog_context.md`, and `STORY-003_visual_foundation_spec.md`.

## Sprint

Target sprint: Sprint 3.

## User Story

As a learner, I want review flows and dialogs to feel clear and consistent so
that selection, confirmation, and mode choices do not feel like default utility
windows.

## Goal

Polish the review screen, mode dialog, mix test dialog, and high-value dialog
states while preserving modal behavior and callbacks.

## PM Refinement Note

Do not assign this as a single junior implementation story. After
`R-007_history_analytics_review_context.md` and `R-008_dialog_context.md` are
complete, split this into narrow stories based on the research summaries.
Expected splits are review screen polish, mode dialog polish, mix dialog polish,
and native dialog inventory/follow-up.

## Required Context

- `visual_overhaul_project/01_context/summaries/history_analytics_review_context.md`.
- `visual_overhaul_project/01_context/summaries/dialog_context.md`.
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.
- Research tasks if context is missing:
  `R-007_history_analytics_review_context.md` and `R-008_dialog_context.md`.

## Scope

In:

- Review scope selection and action hierarchy.
- Missed-question review cards.
- Review empty state.
- Mode selection dialog visual hierarchy.
- Mix test dialog visual hierarchy and selection readability.
- Native message box inventory follow-up recommendations.

Out:

- Review question selection logic changes.
- Mix test generation behavior changes.
- Replacing all native message boxes.
- New dialog framework.

## Likely Files

- `study_test_tool/gui/review_view.py`.
- `study_test_tool/gui/components/mode_dialog.py`.
- `study_test_tool/gui/components/mix_test_dialog.py`.

## Implementation Steps

1. Do not start as a junior implementation assignment until this story is split.
2. Read CTX-DATA-VIEWS, CTX-DIALOGS, CTX-FOUNDATION, and the
   research-recommended split.
3. Create or assign one narrow child story for review screen, mode dialog, mix
   dialog, or native dialog inventory.
4. Implement only the selected child story scope.
5. Verify the exact review/dialog states, callbacks, return values, light mode,
   dark mode, and cancel paths named by the child story.
6. Document native dialogs left as MVP choices or post-MVP follow-ups.

## Acceptance Criteria

- Review screen states are readable and action hierarchy is clear.
- Mode and mix dialogs feel consistent with the foundation.
- Dialog callbacks and return values are unchanged.
- Confirmation and error dialogs that remain native are documented as deliberate
  MVP choices or follow-up items.
- The story has been split before junior implementation assignment, or the PM
  handoff explains why one senior-owned story is being used instead.

## Verification

- Smoke check review session start paths.
- Smoke check mode dialog choices and mix test creation/cancel.
- Run review/mix tests if behavior-bearing paths are touched.
- Visual check light/dark mode.

## Dev 2 Assignment Notes

- Treat this file as a PM refinement placeholder until split stories exist.
- Do not change review selection logic, mix generation behavior, modal return
  values, callbacks, or import/export feedback behavior.
- If CTX-DIALOGS or CTX-DATA-VIEWS is missing or weak, stop and assign the
  relevant research task.

## Handoff Requirements

- List review and dialog states checked.
- List native dialogs left for post-MVP.
