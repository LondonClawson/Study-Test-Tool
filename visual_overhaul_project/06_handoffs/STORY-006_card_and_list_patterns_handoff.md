# STORY-006 Card And List Patterns Handoff

Story/Task:
`STORY-006_card_and_list_patterns.md`

Status:
Submitted For Review. Returned to Dev 2 for the PM-requested expanded Home card
visual evidence pass; evidence has been captured and validated.

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
- Captured expanded Home active-card state in light and dark mode:
  `home_expanded_cards`.
- Captured expanded Home archived-card state in light and dark mode:
  `home_expanded_archived_cards`.
- Code-level preservation checked for active cards, archived cards, grouped
  rendering, collapsed-state persistence, sorting, and zero-question disabled
  Take Test behavior.
- Empty state was intentionally left unchanged because it is outside the named
  card/list pilot.

Screenshot evidence:
- `visual_overhaul_project/01_context/screenshots/after/STORY-006/light/light_home_expanded_cards.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-006/light/light_home_expanded_archived_cards.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-006/dark/dark_home_expanded_cards.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-006/dark/dark_home_expanded_archived_cards.png`

Tests run:
- `PYTHONPATH=study_test_tool python3 -m py_compile study_test_tool/gui/styles.py study_test_tool/gui/test_selector.py`
- `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 study_test_tool/main.py`
- `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --states home_expanded_cards home_expanded_archived_cards --output visual_overhaul_project/01_context/screenshots/after/STORY-006`
- `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --mode both --states home_expanded_cards home_expanded_archived_cards --output visual_overhaul_project/01_context/screenshots/after/STORY-006`
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

PM review decision:
Changes requested on 2026-06-16. The implementation may be scoped correctly, but
the submitted evidence does not prove the card/list acceptance criteria because
the available Home screenshots show groups collapsed. The pilot area is Home
test-card outer surfaces, so review needs visible active and archived cards.

PM requested changes:
- Capture or add reviewable visual evidence for expanded Home cards in light and
  dark mode.
- Evidence must show active card surface, border, radius, title, description,
  metadata, and action row treatment.
- Evidence must show archived card muted surface and muted text hierarchy.
- Evidence must include grouped rendering and the archived group where practical.
- Resubmit with screenshot paths or a documented capture blocker. Startup smoke
  and code-level preservation checks are not sufficient for this visual story.

Dev 2 evidence update:
Captured the requested expanded Home card evidence on 2026-06-16. The screenshot
harness wrote and validated four screenshots under
`visual_overhaul_project/01_context/screenshots/after/STORY-006/`.

Risks:
- Remaining review risk is visual acceptance judgment only; the requested
  screenshot packet now exists and validated successfully.
- `get_text_style()` currently covers Home card text roles only. Later card
  families should extend it only as their pilot stories require.

Follow-up backlog items:
- PM/reviewer should decide whether to accept the Home card/list pilot before
  unblocking dependent card stories.
- PM should consider a small process-doc follow-up to make state-scoped
  screenshot validation explicit in `00_project/screenshot_evidence_policy.md`.
  The useful pattern for story-specific evidence is
  `--validate-only --mode both --states <state...> --output <story-output-dir>`;
  full-directory validation checks the complete baseline manifest and is noisy
  for intentionally narrow story evidence packets.
- Defer extracting a shared active/archived card label-stack helper until a
  second card family adopts the pattern; keeping the first pilot explicit makes
  review easier and avoids a premature generic card abstraction.
