# STORY-016 Light/Dark And Minimum-Size Validation Assignment

Assignment: Complete the MVP light/dark and minimum-size validation pass.
Role: Dev 2 Validation Agent

Primary file:
`visual_overhaul_project/04_stories/STORY-016_light_dark_and_min_size_validation.md`

Read these context summaries first:

- `visual_overhaul_project/01_context/summaries/baseline_visual_audit.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/06_handoffs/screenshot_checklist.md`
- Completed story handoffs and review notes for `STORY-008` through
  `STORY-015`.

Do this:

- Validate every MVP screen in light mode and dark mode.
- Validate every MVP screen at the minimum supported window size where the
  harness or manual runtime makes that practical.
- Check for text clipping, overlap, unreadable contrast, broken scroll behavior,
  hidden primary actions, and status colors that lose meaning.
- Update or create a validation matrix in the handoff.
- List concrete follow-up issues with priority and screen/state names.

Do not do this:

- Do not redesign screens.
- Do not add features.
- Do not change application code unless the PM explicitly assigns a small
  validation fix.
- Do not treat native message boxes or file dialogs as MVP blockers; they are
  documented exceptions under `STORY-015E`.

Expected output:

- `STORY-016` moved to `Submitted For Review` when validation is complete.
- A handoff at
  `visual_overhaul_project/06_handoffs/STORY-016_light_dark_and_min_size_validation_handoff.md`.
- Validation matrix covering Home, Test Taking, Results, Editor, History,
  Analytics, Review, Mode dialog, Mix dialog, Import Preview dialog, and
  documented native-dialog exceptions.
- Follow-up list with each issue classified as MVP blocker, post-MVP follow-up,
  or accepted limitation.

Required verification:

- Use screenshot comparison or written visual checklist for every MVP screen.
- Run screenshot validation commands for any captured screenshot set.
- Run automated tests only if code fixes are made.
- Run `git diff --check` before handoff.

Handoff location:
`visual_overhaul_project/06_handoffs/STORY-016_light_dark_and_min_size_validation_handoff.md`

Notes:
This is a validation story, not a broad fix-it pass. If a serious issue is
found, document it precisely and ask the PM whether to open a small follow-up
fix story or mark it as a blocker for `STORY-017`.
