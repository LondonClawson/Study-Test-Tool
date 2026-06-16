# STORY-007 Page Header Pattern Assignment

Assignment: Pilot the page header pattern on Home/Test Selector.
Role: Dev 2 Implementation Agent

Primary file:
`visual_overhaul_project/04_stories/STORY-007_page_header_pattern.md`

Read these context summaries first:
`visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
`visual_overhaul_project/01_context/summaries/gui_architecture_summary.md`
`visual_overhaul_project/01_context/summaries/home_screen_context.md`

Do this:
Use Home/Test Selector as the single pilot. Refactor the existing title and
top action area into a consistent page header structure with a page title,
optional concise subtitle/context, and clear right or below-header action
placement. Preserve the current Home/Test Selector workflows and callbacks.
Add only the minimal shared style roles or helper needed to make the pattern
repeatable for later screens.

Do not do this:
Do not redesign test cards, group rows, sort behavior, dialogs, import/export,
navigation, persistence, scoring, or session behavior. Do not introduce an app
wide header component unless the pilot proves a tiny helper is necessary. Do not
change button labels or action meaning.

Implementation plan:
1. Inspect the current Home/Test Selector shell in
   `study_test_tool/gui/test_selector.py`, especially `_build_ui()`.
2. Identify the existing title, action bar, and sort toolbar boundaries so the
   header can improve hierarchy without moving workflow commands to new screens.
3. Add minimal semantic header styles in `study_test_tool/gui/styles.py` only if
   existing typography, surface, and spacing roles are insufficient.
4. Replace the isolated title plus loose action bar with a single header region
   that keeps the product title as the screen identity and groups create/import,
   mix, review, history, and analytics actions predictably.
5. Keep the sort toolbar visually separate from the page header unless a small
   spacing adjustment is needed to preserve hierarchy.
6. Smoke check normal, empty, grouped, archived, and narrow/minimum-size Home
   states for layout fit and light/dark readability.
7. Capture after screenshots for touched Home states if the GUI harness is
   available; otherwise document the exact capture blocker in the handoff.

Expected output:
Completed story scope, updated story status, and a handoff note at
`visual_overhaul_project/06_handoffs/STORY-007_page_header_pattern_handoff.md`.

Required verification:
Run focused tests if behavior-bearing code changes. At minimum, perform a GUI
startup or Home/Test Selector visual smoke check, verify Home navigation
callbacks still point to the same controller actions, and check light/dark plus
minimum-window behavior. Screenshot evidence is required for changed Home
states under `00_project/screenshot_evidence_policy.md`, or the handoff must
document why capture was blocked.

Handoff location:
Use `visual_overhaul_project/06_handoffs/handoff_template.md`.

Notes:
This assignment deliberately avoids accepting `STORY-005` or `STORY-006`.
Those submitted stories remain reviewer/PM work and should not be broadened
inside this header pilot.
