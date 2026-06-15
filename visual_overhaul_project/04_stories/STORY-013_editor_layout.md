# STORY-013: Editor Layout

## Status

Blocked.

## Readiness

- Blocked by: CTX-FOUNDATION.
- Unblocked by: `R-006_editor_context.md` and
  `STORY-003_visual_foundation_spec.md`.

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

- Smoke check create test, edit test metadata, add MC question, add essay
  question, edit question, delete question, save.
- Run relevant tests if group or validation behavior is touched.
- Visual check light/dark mode.

## Dev 2 Assignment Notes

- Do not change question data models, validation rules, or save/cancel behavior.
- Do not make broad form-framework changes.
- If CTX-EDITOR is missing or stale, stop and assign R-006.

## Handoff Requirements

- List editor states checked.
- List any unresolved form-density issues.
