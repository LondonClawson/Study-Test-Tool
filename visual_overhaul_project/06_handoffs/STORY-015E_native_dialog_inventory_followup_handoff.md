# STORY-015E Native Dialog Inventory Follow-Up Handoff

Story/Task: `STORY-015E_native_dialog_inventory_followup.md`
Status: Done
Summary:
PM decision made on 2026-06-17: no native messagebox or file-dialog replacement
is approved for MVP. Native dialogs remain deliberate MVP exceptions. Any future
native-dialog replacement must be created as a separate post-MVP implementation
story.

Files changed:

- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/04_stories/STORY-015E_native_dialog_inventory_followup.md`
- `visual_overhaul_project/06_handoffs/STORY-015E_native_dialog_inventory_followup_handoff.md`

Definition of Ready checked:

- PM decision story was blocked only by the post-MVP native-dialog decision.
- CTX-DIALOGS and CTX-FOUNDATION were Ready before the decision.

Context summaries read:

- `visual_overhaul_project/01_context/summaries/dialog_context.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`

Context summaries created/updated:

- None.

Screens/states checked:

- Source inventory reviewed for native `messagebox` and `filedialog` usage in
  `study_test_tool/gui/`.

Screenshot evidence:

- Not required. This is a docs-only PM decision and no user-visible UI changed.

Tests run:

- `git diff --check`

Tests not run and why:

- Pytest was not run because no application code changed.

Acceptance criteria notes:

- Native message boxes and file dialogs are documented as deliberate MVP
  exceptions.
- Batch PDF `askyesnocancel()` is explicitly protected.
- No native dialog replacement is approved without a future narrow story.

Risks:

- Native dialogs will remain visually inconsistent with CustomTkinter surfaces
  for MVP by design.
- Long report flows may still deserve post-MVP custom treatment after MVP
  closeout.

Follow-up backlog items:

- Consider a post-MVP custom report/confirmation pattern for PDF import
  reports, export warnings, or missing-answer confirmations only after MVP
  validation is complete.
