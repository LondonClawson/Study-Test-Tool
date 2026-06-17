# STORY-009 Home Test Cards And Actions Review

Story/Task:
`STORY-009_home_test_cards_and_actions.md`

Status:
Done. Accepted by PM/reviewer on 2026-06-16.

Summary:
Accepted the submitted Home card/action implementation. Active cards, archived
cards, disabled Take Test treatment, metadata chips, and card action hierarchy
match the story scope. I found no required blocker in callback wiring,
screenshot evidence, or focused verification.

Files reviewed:
- `study_test_tool/gui/test_selector.py`
- `visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `visual_overhaul_project/04_stories/STORY-009_home_test_cards_and_actions.md`
- `visual_overhaul_project/06_handoffs/STORY-009_home_test_cards_and_actions_handoff.md`
- `visual_overhaul_project/01_context/screenshots/after/STORY-009/`

Context checked:
- `visual_overhaul_project/01_context/summaries/home_screen_context.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/06_handoffs/STORY-009_home_test_cards_and_actions_readiness_review.md`
- `visual_overhaul_project/00_project/screenshot_evidence_policy.md`
- `visual_overhaul_project/00_project/status_transition_rules.md`

Acceptance notes:
- Take Test is the dominant active-card action, while Edit, Export, and Archive
  are quieter utility actions.
- Delete remains visibly destructive without competing with the primary study
  action.
- Zero-question cards keep Take Test disabled and show a muted disabled
  treatment.
- Archived cards are visually distinct and still keep Unarchive/Delete readable.
- Metadata chips improve scannability in the sampled full-size and
  minimum-width states.
- Existing callbacks are preserved for Take Test, Edit, Export, Archive,
  Delete, Unarchive, and Archive Group.

Screenshot evidence reviewed:
- `visual_overhaul_project/01_context/screenshots/after/STORY-009/light/light_home_expanded_cards.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-009/dark/dark_home_expanded_cards.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-009/light/light_home_expanded_archived_cards.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-009/dark/dark_home_expanded_archived_cards.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-009/light/light_home_minimum_populated.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-009/dark/dark_home_populated_grouped.png`

Verification:
- `python3 -m compileall -q study_test_tool/gui/test_selector.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/test_selector.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --mode both --states home_populated_grouped home_expanded_cards home_expanded_archived_cards home_minimum_populated --output visual_overhaul_project/01_context/screenshots/after/STORY-009`
- `git diff --check`

Results:
- Syntax check passed.
- Black check passed.
- Screenshot validation passed: 8 screenshots.
- `git diff --check` passed.

Tests not run:
No pytest subset was run for this story because the submitted implementation is
GUI presentation work and the handoff documents focused GUI smoke coverage for
the card actions. No service, database, import/export, persistence, scoring, or
session behavior changed.

Risks and follow-up:
- The sampled minimum-width screenshots cover normal seeded names and groups,
  not extreme text. Later validation should include a very long test name,
  description, and group name.
- Metadata chips remain local to Home card construction, which is acceptable for
  this pilot and avoids premature shared abstraction.
