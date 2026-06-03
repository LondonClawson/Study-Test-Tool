# Risk Register

## R-001: Behavior Regression From Visual Work

- Risk: GUI refactoring accidentally changes navigation, scoring, session state,
  or import/export behavior.
- Probability: Medium.
- Impact: High.
- Mitigation: Keep GUI changes scoped, run relevant tests, and avoid service or
  database edits unless explicitly required.
- Watch For: Changed method signatures, altered `show_frame` arguments, changed
  response handling, changed persistence calls.

## R-002: CustomTkinter Visual Limits

- Risk: Design expectations exceed what CustomTkinter can cleanly support.
- Probability: Medium.
- Impact: Medium.
- Mitigation: Prefer hierarchy, spacing, color discipline, and reusable frames
  over complex custom rendering.
- Watch For: Fragile widget layering, platform-specific behavior, overbuilt
  custom controls.

## R-003: Dark Mode Contrast Problems

- Risk: Light-mode polish reduces dark-mode readability.
- Probability: High.
- Impact: Medium.
- Mitigation: Every foundation and screen story must include light/dark checks.
- Watch For: Hard-coded light colors, muted gray text, chart backgrounds.

## R-004: Context Summaries Become Stale

- Risk: Agents rely on outdated summaries and miss current behavior.
- Probability: Medium.
- Impact: Medium.
- Mitigation: Summaries include source paths and refresh triggers. Agents update
  summaries when source files changed after summary dates.
- Watch For: Major GUI file edits without summary updates.

## R-005: Scope Expansion Into Product Redesign

- Risk: Visual polish turns into workflow redesign, icon system, navigation
  rebuild, or new study features.
- Probability: Medium.
- Impact: High.
- Mitigation: Use scope guardrails and change control. Move post-MVP ideas to
  backlog instead of implementing them inside MVP stories.
- Watch For: New screens, new persisted settings, broad navigation changes.

## R-006: Dense Screens Lose Efficiency

- Risk: Editor, history, and analytics become prettier but slower to scan.
- Probability: Medium.
- Impact: Medium.
- Mitigation: Treat the app as a productivity tool. Preserve density where
  repeated studying benefits from compact presentation.
- Watch For: Oversized headings, decorative cards, excess vertical whitespace.
