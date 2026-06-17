Story/Task:
`STORY-009_home_test_cards_and_actions.md`

Status:
Submitted For Review. PM/reviewer acceptance is still required; this is not
marked Done.

Summary:
Polished Home active and archived test-card internals without changing card
data, sorting, grouping, import/export behavior, archive/delete confirmations,
or navigation callbacks. Active cards now separate the primary Take Test action
from quieter utility actions, use compact metadata chips for question count and
group name, and show a muted disabled Take Test treatment for zero-question
cards. Archived cards use a muted surface with an archived badge, metadata
chips, and clear Unarchive/Delete actions.

Files changed:
- `study_test_tool/gui/test_selector.py`
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/04_stories/STORY-009_home_test_cards_and_actions.md`
- `visual_overhaul_project/06_handoffs/STORY-009_home_test_cards_and_actions_handoff.md`
- `visual_overhaul_project/01_context/screenshots/after/STORY-009/`

Definition of Ready checked:
Yes. `STORY-009` was Ready and unblocked after PM accepted `STORY-008`. CTX-HOME,
CTX-FOUNDATION, and CTX-STYLE-INVENTORY were Ready, and the PM readiness review
confirmed the story scope.

Context summaries read:
- `visual_overhaul_project/01_context/summaries/home_screen_context.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/01_context/summaries/style_inventory.md`
- `visual_overhaul_project/06_handoffs/STORY-005_button_hierarchy_handoff.md`
- `visual_overhaul_project/06_handoffs/STORY-006_card_and_list_patterns_handoff.md`
- `visual_overhaul_project/06_handoffs/STORY-007_page_header_pattern_handoff.md`
- `visual_overhaul_project/06_handoffs/STORY-008_home_screen_layout_handoff.md`
- `visual_overhaul_project/06_handoffs/STORY-008_home_screen_layout_review.md`
- `visual_overhaul_project/06_handoffs/STORY-009_home_test_cards_and_actions_readiness_review.md`

Context summaries created/updated:
None.

Screens/states checked:
- Populated grouped/collapsed Home cards in light and dark mode.
- Expanded active Home cards in light and dark mode.
- Expanded archived Home cards in light and dark mode.
- Zero-question disabled Take Test treatment in light and dark mode.
- Minimum-window populated Home layout in light and dark mode.
- Focused GUI smoke for Take Test, Edit, Export, Archive, Delete, Unarchive,
  Archive Group, and zero-question disabled Take Test wiring.

Screenshot evidence:
- `visual_overhaul_project/01_context/screenshots/after/STORY-009/light/light_home_populated_grouped.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-009/light/light_home_expanded_cards.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-009/light/light_home_expanded_archived_cards.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-009/light/light_home_minimum_populated.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-009/dark/dark_home_populated_grouped.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-009/dark/dark_home_expanded_cards.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-009/dark/dark_home_expanded_archived_cards.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-009/dark/dark_home_minimum_populated.png`

Tests run:
- `python3 -m compileall -q study_test_tool/gui/test_selector.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/test_selector.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- Focused GUI smoke with seeded temporary data for Take Test, Edit, Export,
  Archive, Delete, Unarchive, Archive Group, and zero-question disabled Take
  Test wiring.
- `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --states home_populated_grouped home_expanded_cards home_expanded_archived_cards home_minimum_populated --output visual_overhaul_project/01_context/screenshots/after/STORY-009`
- `git diff --check`

Tests not run and why:
Full pytest was not run because this story changed Home GUI card presentation
only. No service, database, scoring, import/export implementation, persistence,
session, or callback logic changed. The focused GUI smoke covered card command
wiring.

Acceptance criteria notes:
- Take Test is the largest and clearest active card action.
- Edit and Export are visually lower-emphasis tertiary actions.
- Archive remains a secondary utility action.
- Delete remains visible and destructive without sharing the primary action row.
- Archived cards are visually distinct through muted card surface, muted title
  hierarchy, archived badge, and metadata chips while retaining readable
  Unarchive/Delete actions.
- Zero-question cards retain disabled Take Test behavior with a muted disabled
  visual treatment.
- Metadata now separates question count and group name into compact chips rather
  than a single pipe-delimited gray line.

Risks:
- Card action layout is now a two-column action block. It fits the sampled
  800x600 minimum-window state, but very long action labels or localized text
  should be rechecked during validation.
- Metadata chips are implemented locally inside Home card construction, not as
  a shared abstraction. That is intentional for this Home card pilot.

Follow-up backlog items:
- Later minimum-size validation should include a very long test name,
  description, and group name to stress the new card action block and metadata
  chips.
