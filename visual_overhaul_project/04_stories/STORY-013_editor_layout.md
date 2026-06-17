# STORY-013: Editor Layout

## Status

Submitted For Review.

## Readiness

- Blocked by: None.
- Unblocked by: `R-006_editor_context.md`,
  `STORY-003_visual_foundation_spec.md`, accepted shared style entry points,
  and accepted button/card/page-header pilots.

CTX-EDITOR and CTX-FOUNDATION are Ready. `STORY-004`, `STORY-005`,
`STORY-006`, and `STORY-007` are Done, so the editor has accepted style,
button, card/list, and page-header guidance available for implementation.
Dev 2 implementation submitted for PM/reviewer acceptance.

## Sprint

Target sprint: Sprint 3.

## User Story

As a test author, I want the editor to feel organized and efficient so that I can
manage questions without visual clutter or lost context.

## Goal

Polish the editor layout, metadata section, question list cards, form hierarchy,
option rows, and add/update/cancel action states.

## Required Context

- `visual_overhaul_project/01_context/summaries/editor_context.md`.
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`.
- Research task if context is missing:
  `visual_overhaul_project/02_research_tasks/R-006_editor_context.md`.

## Scope

In:

- Editor page header and metadata layout.
- Question list card presentation.
- Add/edit form visual hierarchy.
- Multiple-choice option row styling.
- Essay expected-answer panel styling.
- Save/add/update/cancel button hierarchy.

Out:

- Validation rule changes.
- Question CRUD behavior changes.
- New editor features.

## Likely Files

- `study_test_tool/gui/test_editor.py`.
- `study_test_tool/gui/components/autocomplete_entry.py` if group entry styling is
  included.

## Implementation Steps

1. Read CTX-EDITOR, CTX-FOUNDATION, and the Dev 2 Quick Start notes.
2. Inspect only metadata, question list, form, option row, essay answer, and
   save/cancel regions named by CTX-EDITOR.
3. Polish layout hierarchy while preserving dense editing efficiency.
4. Preserve validation, save/cancel, question ordering, group, and persisted
   data behavior.
5. Verify new test, edit test, no questions, multiple-choice, essay, validation
   warning, light, dark, and minimum-window states.
6. Run group/editor-adjacent tests if behavior-bearing paths are touched.

## Acceptance Criteria

- Existing editor workflows still work for new and existing tests.
- Question list is scannable.
- Add vs update vs cancel state is visually clear.
- Validation warnings remain noticeable.
- Dense editing efficiency is preserved at minimum window size.

## Verification

- Screenshot evidence is required under
  `visual_overhaul_project/01_context/screenshots/after/STORY-013/`.
- Capture or document a blocker for light and dark states covering new test,
  existing populated test with questions, saved empty test/no questions,
  multiple-choice add form, essay add form, edit-question mode, validation
  warning, group autocomplete dropdown, and minimum-window editor layout where
  practical.
- Smoke check create test, edit test metadata, add MC question, add essay
  question, edit question, delete question, save.
- Run `pytest --rootdir=. study_test_tool/tests/test_group_sort.py` if group
  behavior or autocomplete-adjacent metadata code changes.
- Run relevant editor, validation, or service tests if behavior-bearing paths
  are touched.

## Dev 2 Assignment Notes

- Do not change question data models, validation rules, or save/cancel behavior.
- Do not make broad form-framework changes.
- If CTX-EDITOR is missing or stale, stop and assign R-006.

## Handoff Requirements

- List editor states checked.
- List screenshot paths or exact capture blockers for every required state.
- List any unresolved form-density issues.
- Confirm validation rules, question CRUD behavior, group persistence, dirty
  form protection, and save/cancel behavior stayed unchanged.
