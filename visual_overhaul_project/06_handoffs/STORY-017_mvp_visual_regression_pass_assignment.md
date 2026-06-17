# STORY-017 MVP Visual Regression Pass Assignment

Assignment: Complete the final MVP visual regression and closeout pass.
Role: Dev 2 Closeout Agent

Primary file:
`visual_overhaul_project/04_stories/STORY-017_mvp_visual_regression_pass.md`

Read these first:

- `visual_overhaul_project/03_backlog/acceptance_matrix.md`
- `visual_overhaul_project/01_context/summaries/baseline_visual_audit.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/06_handoffs/STORY-016_light_dark_and_min_size_validation_handoff.md`
- `visual_overhaul_project/06_handoffs/STORY-016_light_dark_and_min_size_validation_review.md`
- Completed story handoffs and PM review notes for `STORY-008` through
  `STORY-015E`

Do this:

- Verify every acceptance-matrix row has evidence or a documented exception.
- Compare baseline evidence against accepted after evidence for each MVP screen
  family.
- Confirm behavior-preservation evidence exists for touched workflows.
- Classify remaining items as one of: MVP blocker, post-MVP follow-up, or
  accepted limitation.
- Produce a final MVP closeout handoff with a test-run summary and post-MVP
  backlog recommendations.

Pay special attention to:

- Long-content stress coverage gaps from `STORY-016`.
- The single-day Analytics Study Activity wide-bar presentation.
- Native messageboxes and file dialogs documented under `STORY-015E`.
- Any acceptance-matrix row whose evidence is still too generic to support
  product-owner acceptance.

Do not do this:

- Do not redesign screens.
- Do not add features.
- Do not change application code unless the PM explicitly approves a small
  closeout fix.
- Do not silently accept missing evidence. If evidence is missing, document the
  gap and classify it.

Expected output:

- `STORY-017` moved to `Submitted For Review` when closeout is complete.
- A final closeout handoff at
  `visual_overhaul_project/06_handoffs/STORY-017_mvp_visual_regression_pass_handoff.md`.
- Acceptance-matrix review notes.
- Test-run summary.
- Final list of blockers, post-MVP follow-ups, and accepted limitations.

Required verification:

- Run `git diff --check`.
- Run relevant screenshot validation if new screenshots are captured.
- Run the relevant pytest suite if any application code changes are made.
- If no application code changes are made, state why pytest was not run or
  summarize the existing test evidence used for behavior preservation.

Handoff location:
`visual_overhaul_project/06_handoffs/STORY-017_mvp_visual_regression_pass_handoff.md`

Notes:
This is closeout review work. The goal is a defensible final quality decision,
not another broad implementation pass.
