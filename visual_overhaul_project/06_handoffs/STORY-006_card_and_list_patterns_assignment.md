# STORY-006 Card And List Patterns Assignment

Assignment: Implement the Home test-card pilot for card/list patterns.
Role: Dev 2 Implementation Agent

Primary file:
`visual_overhaul_project/04_stories/STORY-006_card_and_list_patterns.md`

Read these context summaries first:
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/01_context/summaries/style_inventory.md`
- `visual_overhaul_project/01_context/summaries/home_screen_context.md`
- `visual_overhaul_project/06_handoffs/STORY-004_shared_style_entrypoints_handoff.md`
- `visual_overhaul_project/06_handoffs/STORY-005_button_hierarchy_handoff.md`

Named pilot area:
Home test-card outer surfaces in `study_test_tool/gui/test_selector.py`,
covering active cards, archived cards, metadata hierarchy, and the existing card
action row container. `CollapsibleGroup` spacing may be touched only if the card
boundary requires a local adjustment.

Implementation plan:
1. Extend `study_test_tool/gui/styles.py` only as needed with small card/list
   helpers or constants that reuse existing semantic colors, radius, spacing,
   and typography roles.
2. Replace Home active-card inline surface defaults with explicit semantic card
   surface, border, radius, padding, title, description, and metadata treatment.
3. Replace archived-card inline tuple gray styling with semantic muted surface
   and readable text roles while preserving the inactive/archive signal.
4. Keep the existing action buttons, command callbacks, group ordering,
   collapsed-state persistence, sorting, zero-question disabled Take Test state,
   and confirmation flows unchanged.
5. Avoid migrating results, editor, review, analytics, dialogs, or generic group
   headers beyond the named pilot.
6. Document reusable card/list rules, Home-specific exceptions, verification
   evidence, and follow-up migration targets in the story handoff.

Do not do this:
- Do not redesign the full Home layout or top toolbar.
- Do not introduce a generic card component before the pilot proves the pattern.
- Do not change services, database access, import/export, navigation, scoring,
  mix-test behavior, or test/session state.
- Do not migrate unrelated cards or rows in other screens.

Expected output:
Completed `STORY-006` implementation scope, updated story status/tracker files,
and a handoff note at
`visual_overhaul_project/06_handoffs/STORY-006_card_and_list_patterns_handoff.md`.

Required verification:
- `PYTHONPATH=study_test_tool python3 -m py_compile study_test_tool/gui/styles.py study_test_tool/gui/test_selector.py`
- App startup smoke check when GUI runtime is available.
- Visual smoke check of Home active, archived, grouped/collapsed, empty, and
  zero-question states in light and dark mode where practical.
- `git diff --check`

Notes:
If implementation discovers that the Home context is stale or card/list rules
need a product decision outside this pilot, stop and mark the story Blocked with
the blocker documented in the handoff.

PM review note:
After implementation, the only refactor candidate was extracting a shared helper
for the active/archived card label stack in `test_selector.py`. Recommendation:
defer that extraction until a second card family adopts the pattern, because
keeping the first pilot's role choices explicit makes review easier and avoids a
premature generic card abstraction.
