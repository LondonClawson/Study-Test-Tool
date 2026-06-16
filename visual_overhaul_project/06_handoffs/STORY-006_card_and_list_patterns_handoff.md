# STORY-006 Card And List Patterns Handoff

Story/Task:
`STORY-006_card_and_list_patterns.md`

Status:
Submitted For Review. Implementation is complete and waiting for PM/reviewer
acceptance.

Summary:
Implemented the Home test-card pilot for shared card/list patterns. Active and
archived Home cards now use semantic card surfaces, borders, radius, spacing,
and text roles from `gui.styles`. Existing Home workflows, callbacks, sorting,
grouping, archive/delete confirmations, and zero-question disabled Take Test
behavior were preserved.

Files changed:
- `study_test_tool/gui/styles.py`
- `study_test_tool/gui/test_selector.py`
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/04_stories/STORY-006_card_and_list_patterns.md`
- `visual_overhaul_project/06_handoffs/STORY-006_card_and_list_patterns_assignment.md`
- `visual_overhaul_project/06_handoffs/STORY-006_card_and_list_patterns_handoff.md`

Definition of Ready checked:
Yes. `CTX-FOUNDATION`, `CTX-STYLE-INVENTORY`, and `CTX-HOME` were Ready, and the
assignment packet named Home test-card outer surfaces as the pilot area before
implementation.

Context summaries read:
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/01_context/summaries/style_inventory.md`
- `visual_overhaul_project/01_context/summaries/home_screen_context.md`
- `visual_overhaul_project/06_handoffs/STORY-004_shared_style_entrypoints_handoff.md`
- `visual_overhaul_project/06_handoffs/STORY-005_button_hierarchy_handoff.md`

Context summaries created/updated:
None.

Screens/states checked:
- Home/Test Selector startup smoke check reached the GUI main loop with no
  immediate console error.
- Code-level preservation checked for active cards, archived cards, grouped
  rendering, collapsed-state persistence, sorting, and zero-question disabled
  Take Test behavior.
- Empty state was intentionally left unchanged because it is outside the named
  card/list pilot.

Tests run:
- `PYTHONPATH=study_test_tool python3 -m py_compile study_test_tool/gui/styles.py study_test_tool/gui/test_selector.py`
- `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 study_test_tool/main.py`
- `git diff --check`

Tests not run and why:
Full pytest was not run because this implementation only changed GUI styling
helpers and Home card style kwargs. No service, database, scoring, import,
session, or navigation behavior changed.

Acceptance criteria notes:
- The reusable pilot rules are represented by `CARD_ROLES`, `TEXT_ROLES`,
  `get_card_style()`, and `get_text_style()` in `gui.styles`.
- Active Home cards use the default semantic surface, border, card radius, card
  title, description, and metadata roles.
- Archived Home cards use the muted semantic surface and muted text hierarchy
  while preserving visible Unarchive and Delete actions.
- No unrelated cards, rows, dialogs, results, editor, review, analytics, or
  group header patterns were migrated.

Risks:
- Runtime visual inspection was limited to startup smoke verification; no
  screenshot packet was captured in this chunk.
- `get_text_style()` currently covers Home card text roles only. Later card
  families should extend it only as their pilot stories require.

Follow-up backlog items:
- PM/reviewer should decide whether to accept the Home card/list pilot before
  unblocking dependent card stories.
- Defer extracting a shared active/archived card label-stack helper until a
  second card family adopts the pattern; keeping the first pilot explicit makes
  review easier and avoids a premature generic card abstraction.
