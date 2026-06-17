# STORY-013 Editor Layout Readiness Review

Story/Task:
`STORY-013_editor_layout.md`

Status:
Ready gate passed after PM readiness review on 2026-06-16. Current board state:
`In Progress`.

Purpose:
Clear stale blocker language and give Dev 2 a concrete assignment gate for the
editor layout story. `STORY-013` is now the active implementation lane while
`STORY-012` waits on a targeted changes-requested fix.

Decision:
`STORY-013_editor_layout.md` is Ready. CTX-EDITOR and CTX-FOUNDATION are Ready,
and the accepted shared style, button hierarchy, card/list, and page-header
pilot stories provide enough foundation guidance for an editor-focused layout
pass.

Current Assignment Addendum:
`STORY-013` is now the active Dev 2 implementation lane. Do not move it to
Done until the developer submits the implementation handoff, required screenshot
evidence or exact capture blockers, smoke-check notes, and required test or
skip notes.

Context Checked:
- `visual_overhaul_project/01_context/summaries/editor_context.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/00_project/definition_of_ready.md`
- `visual_overhaul_project/00_project/screenshot_evidence_policy.md`
- `visual_overhaul_project/06_handoffs/STORY-004_shared_style_entrypoints_handoff.md`
- `visual_overhaul_project/06_handoffs/STORY-006_card_and_list_patterns_handoff.md`

Scope Confirmation:
- Keep the story limited to `study_test_tool/gui/test_editor.py` and
  `study_test_tool/gui/components/autocomplete_entry.py` if group autocomplete
  styling is included.
- Preserve the existing editor workflow: metadata save, question add/update,
  cancel edit, delete confirmation, dirty-form warning, option row order,
  correct-answer index handling, group persistence, and service boundaries.
- Do not change validation rules, question data models, persistence behavior,
  native messagebox behavior, or add new editor features.

Required Screenshot Evidence:
Capture under `visual_overhaul_project/01_context/screenshots/after/STORY-013/`
or document exact blockers in the handoff.

Required states:
- New test editor.
- Existing populated test with questions.
- Saved empty test/no questions.
- Multiple-choice add form.
- Essay add form.
- Edit-question mode with Update/Cancel visible.
- Validation warning path.
- Group autocomplete dropdown.
- Minimum-window editor layout.

Quality Notes For Dev 2:
- Preserve dense editing efficiency. The editor is a work surface, not a
  marketing page.
- Keep the two-column model unless minimum-window evidence proves it is not
  usable and the handoff documents the constraint.
- If autocomplete styling is touched, smoke check dropdown placement, hover
  colors, outside-click dismissal, Escape dismissal, and suggestion selection.
- If option rows are styled, keep `option_entries`, `_option_rows`,
  `_option_radios`, `_option_remove_btns`, and `correct_var` in row order.

Verification Expectations:
- Smoke check create test, edit metadata, save, add MC question, add essay
  question, edit question, cancel edit, delete question, validation warning,
  option add/remove, and group autocomplete.
- Run `pytest --rootdir=. study_test_tool/tests/test_group_sort.py` if group or
  autocomplete-adjacent metadata behavior is touched.
- Run additional editor, validation, or service tests if behavior-bearing paths
  are touched.

Priority:
Continue the active `STORY-013` implementation lane if it is already claimed.
Keep `STORY-014A`, `STORY-014B`, and `STORY-014C` behind `STORY-013` unless PM
intentionally opens another lane. Keep `STORY-012` in Changes Requested until
the named retake-state fix is resubmitted and accepted.

Files Updated:
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/04_stories/STORY-013_editor_layout.md`
- `visual_overhaul_project/06_handoffs/STORY-013_editor_layout_readiness_review.md`

Tests:
Not run. This was a PM tracker/readiness documentation update only; no
application code changed.
