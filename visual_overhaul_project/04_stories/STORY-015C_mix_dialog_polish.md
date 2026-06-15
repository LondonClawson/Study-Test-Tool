# STORY-015C: Mix Dialog Polish

## Status

Blocked.

## Readiness

- Blocked by: `STORY-005_button_hierarchy.md` and list/card pattern guidance.
- Unblocked by: completion of the button hierarchy pilot and either
  `STORY-006_card_and_list_patterns.md` or an approved PM exception.

## Sprint

Target sprint: Sprint 3.

## User Story

As a learner, I want the mix-test dialog to make grouped test selection and
question count setup easy to scan before starting a mixed practice or test.

## Required Context

- `visual_overhaul_project/01_context/summaries/dialog_context.md`.
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.
- Completed handoff for `STORY-005`.
- Completed handoff for `STORY-006`, unless PM explicitly approves a dialog-only
  list treatment.

## Scope

In:

- `MixTestDialog` title/helper hierarchy.
- Select All and Deselect All button roles.
- Group header and child checkbox readability.
- Total/count area and Start Mix Test/Cancel hierarchy.

Out:

- Mix-test selection semantics.
- Group checkbox sync behavior.
- Question count parsing.
- Inline validation for silent invalid starts.

## Likely Files

- `study_test_tool/gui/components/mix_test_dialog.py`.

## Implementation Steps

1. Read CTX-DIALOGS, CTX-FOUNDATION, and completed foundation handoffs.
2. Polish only `MixTestDialog` visual hierarchy and list readability.
3. Preserve `get_result()`, group/child checkbox sync, selected test ID order,
   question count parsing, silent invalid-start behavior, and modal behavior.
4. Verify empty selection remains non-submitting, Select All, Deselect All,
   group toggle, child toggle, valid start, cancel, light mode, and dark mode.

## Acceptance Criteria

- Grouped test selection is easier to scan.
- Utility and primary actions follow accepted button roles.
- Invalid start behavior remains unchanged unless a separate story changes it.
- Modal return paths are unchanged.

## Verification

- Smoke check selection and cancel/start paths.
- Visual check light and dark mode.

## Handoff Requirements

- List selection states checked.
- Confirm `get_result()` behavior stayed unchanged.
- List any deferred validation or copy questions.
