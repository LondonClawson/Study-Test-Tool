# STORY-015 Split Handoff

Story/Task:
`STORY-015_review_and_dialog_polish.md`

Status:
Done. Parent story split by PM on 2026-06-15.

Summary:
Split the broad review/dialog polish placeholder into five narrow child stories:
review screen polish, mode dialog polish, mix dialog polish, import preview
dialog polish, and native dialog inventory follow-up. The parent story should
not be assigned for implementation.

Files changed:
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/04_stories/STORY-015_review_and_dialog_polish.md`
- `visual_overhaul_project/04_stories/STORY-015A_review_screen_polish.md`
- `visual_overhaul_project/04_stories/STORY-015B_mode_dialog_polish.md`
- `visual_overhaul_project/04_stories/STORY-015C_mix_dialog_polish.md`
- `visual_overhaul_project/04_stories/STORY-015D_import_preview_dialog_polish.md`
- `visual_overhaul_project/04_stories/STORY-015E_native_dialog_inventory_followup.md`
- `visual_overhaul_project/06_handoffs/STORY-015_split_handoff.md`

Definition of Ready checked:
Yes for split quality. The child stories each name required context, scope,
likely files, constraints, verification, and handoff evidence. They remain
Blocked until their named foundation dependencies are complete.

Context summaries read:
- `visual_overhaul_project/01_context/summaries/history_analytics_review_context.md`
- `visual_overhaul_project/01_context/summaries/dialog_context.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`

Context summaries created/updated:
None.

Screens/states checked:
Static documentation review only. Child stories name the runtime states Dev 2
must verify.

Tests run:
`git diff --check`.

Tests not run and why:
Pytest was not run because this is PM documentation and tracker work only. No
application code changed.

Acceptance criteria notes:
The parent `STORY-015` is no longer a large implementation assignment. Review,
mode dialog, mix dialog, import preview dialog, and native dialog follow-up work
now have separate scoped story files.

Risks:
The child stories are intentionally not Ready yet. `STORY-005`, card/list
guidance, and page header work should land before assigning review or dialog
polish.

Follow-up backlog items:
Keep `STORY-015E_native_dialog_inventory_followup.md` blocked until PM makes a
post-MVP decision about native dialog replacement.
