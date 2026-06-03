# Visual Overhaul Plan

## Purpose

Study Testing Tool is functionally useful, but the current interface still looks
like a developer tool. This project is a visual overhaul only. The goal is to
make the app feel like a polished desktop study product without changing core
features, workflows, scoring behavior, importing behavior, persistence, or test
logic.

The design should feel calm, focused, and practical. This is a study and test
prep app, so the interface should prioritize readability, confidence,
repeat-use comfort, and clear action hierarchy over decorative visuals.

## Visual Direction

The target visual style is a polished macOS-oriented productivity app:

- Quiet, focused, and useful.
- Clear hierarchy between primary, secondary, utility, and destructive actions.
- More whitespace and better alignment, but not a sparse marketing-style UI.
- Cards and panels that feel intentional rather than default framework widgets.
- Strong readability during test-taking and review.
- Consistent light and dark mode behavior.

The overhaul should not introduce a landing page, marketing layout, or major
navigation behavior changes during MVP.

## MVP Design Principles

- Preserve current workflows and behavior.
- Make primary actions obvious without making the interface loud.
- Keep the interface dense enough for repeated studying, but give important
  content enough spacing to breathe.
- Prefer readability and confidence over decoration.
- Use color for meaning and hierarchy, not ornament.
- Make destructive actions available but visually secondary until needed.
- Keep the app feeling like a desktop productivity tool, not a web landing page.
- Work within CustomTkinter's strengths and limitations.

## Current UI Issues

- Visual styling is scattered across individual screen files.
- Many buttons have similar visual weight even when their importance differs.
- Colors are used inconsistently for primary, secondary, warning, success, and
  destructive actions.
- Cards exist, but many still look like default frames with labels placed inside.
- Test-taking, results, history, and analytics screens use different visual
  patterns.
- Empty states and loading states are plain text.
- The app relies heavily on text buttons where icons or quieter utility controls
  would eventually improve polish.
- The default CustomTkinter look is visible throughout the app.

## Pre-MVP Visual Audit

Before implementing the visual overhaul, capture the current state of the app and
define what needs to improve on each screen.

Audit steps:

- Capture screenshots of each major screen in light mode.
- Capture screenshots of each major screen in dark mode.
- Include realistic states where possible, such as populated test lists, empty
  states, test-taking, practice feedback, results, history, and analytics.
- Review each screen for hierarchy, spacing, alignment, readability, action
  clarity, and default-widget appearance.
- Identify which issues are app-wide and which are screen-specific.
- Use the audit to confirm MVP scope before coding begins.

Screens to audit:

- Home/test selector.
- Test editor.
- Test taking.
- Results.
- History.
- Analytics.
- Review.
- Mode selection dialog.
- Mix test dialog.
- Import/error/confirmation dialogs.

## MVP Visual Improvements

### 1. Define the Visual Foundation

Start with app-wide visual decisions before redesigning individual screens.

Define:

- App background color.
- Surface/card colors.
- Border colors.
- Primary, secondary, danger, warning, success, and muted colors.
- Text colors for primary, secondary, muted, disabled, and inverse text.
- Spacing scale.
- Border radius rules.
- Standard font sizes and weights.
- Standard button styles.
- Standard card/list row styles.

This should reduce inline styling across GUI files and give every screen a
shared foundation.

The visual foundation should come after the audit, so the design system solves
specific observed problems instead of only replacing colors and fonts.

### 2. Unify Screen Layouts

Give each major screen a consistent structure:

- Top app/header area.
- Page title.
- Optional subtitle or context text.
- Main content area.
- Consistent horizontal margins.
- Consistent footer/action area where needed.

Screens in scope:

- Home/test selector.
- Test editor.
- Test taking.
- Results.
- History.
- Analytics.
- Review.

### 3. Polish the Home Screen First

The home screen is the app's first impression and should be the first MVP screen
after the visual foundation.

Improve:

- Overall dashboard-like composition.
- Test card styling and readability.
- Group header styling.
- Empty state for no tests.
- Sort/filter toolbar spacing.
- Action hierarchy.

The `Take Test` action should be visually primary. Edit, export, archive, and
delete should feel secondary or utility-level instead of having equal weight.

### 4. Improve Button Hierarchy

Define consistent button roles:

- Primary: main next action, such as `Take Test`, `Save Test`, or `Finish`.
- Secondary: neutral actions, such as `Back`, `History`, or `Analytics`.
- Tertiary: low-emphasis utility actions.
- Danger: destructive actions, such as `Delete`.
- Warning: cautionary actions, such as `Review Missed` or flag-related states.

Current visual colors such as gray, purple, orange, green, and red should be
rationalized into a smaller, intentional palette.

### 5. Upgrade the Test-Taking Screen

The test-taking screen is the core workflow and should receive the second major
MVP pass after the home screen.

Improve:

- Top bar layout for test title, progress, timer, and flag state.
- Question panel readability.
- Multiple-choice answer rows.
- Essay answer input styling.
- Bottom navigation and progress indicator.
- Practice-mode answer feedback.

Multiple-choice answers should feel like selectable answer rows rather than
loose radio buttons and labels.

### 6. Polish Cards and Lists

Standardize repeated surfaces:

- Test cards.
- Question cards.
- Results review cards.
- History rows.
- Analytics topic cards.
- Collapsible group headers.

Cards should use consistent padding, radius, border, spacing, title treatment,
metadata treatment, and action placement.

### 7. Improve Typography

Create a more intentional type scale:

- App/page title.
- Section heading.
- Card title.
- Body text.
- Metadata text.
- Labels and helper text.

The app can continue using a system-safe font, but hierarchy should come from
consistent size, weight, spacing, and muted text treatment.

### 8. Improve Results View

Results should feel like a clear summary, not just a list of labels.

Improve:

- Score summary presentation.
- Time and essay-question metadata.
- Correct/incorrect/essay status badges.
- Question review cards.
- User answer vs. correct answer layout.
- Mix-test source breakdown styling.

### 9. Improve History and Analytics Presentation

History and analytics should feel like polished data views.

Improve:

- History table/list row styling.
- Header alignment and row spacing.
- Selected/clickable row affordance.
- Analytics chart colors.
- Weak-topic card styling.
- Empty/no-data states.

### 10. Polish Empty, Loading, and Error States

Replace plain gray text with designed states.

Improve:

- No tests.
- No history.
- No analytics data.
- Loading history.
- Failed data loading.
- Import/conversion summaries where practical.

Messages should be short, useful, and visually consistent.

## Shared Component Inventory

The MVP should standardize these reusable visual pieces before or during the
screen-specific redesigns:

- Page headers.
- Section headers.
- Primary buttons.
- Secondary buttons.
- Tertiary/utility buttons.
- Danger buttons.
- Status badges.
- Test cards.
- Question cards.
- Results review cards.
- History rows.
- Analytics topic cards.
- Collapsible group headers.
- Empty states.
- Loading states.
- Multiple-choice answer rows.
- Essay answer panels.
- Progress indicators.
- Timer display.
- Form labels and helper text.

The goal is not to create a large framework. The goal is to remove repeated
inline styling and make common UI surfaces feel consistent.

## Post-MVP Visual Improvements

### 1. Icon System

Add icons for common actions after the main visual hierarchy is stable.

Candidates:

- Back.
- Import.
- New test.
- Mix test.
- Edit.
- Export.
- Archive.
- Delete.
- Analytics.
- History.
- Review.
- Flag.
- Previous and next.

Icons should reduce text noise and improve scanability, but they should not make
core actions ambiguous.

### 2. Navigation Refinement

Consider a more persistent navigation model if the app continues growing.

Possible directions:

- Sidebar navigation.
- Top navigation bar.
- More consistent back behavior.
- Stronger active-screen indication.

This should stay post-MVP because it can affect perceived workflow structure,
even if the actual features do not change.

### 3. Responsive Layout Pass

Improve behavior at smaller window sizes.

Focus areas:

- Home action rows.
- Test cards with many actions.
- Test editor two-column layout.
- Test-taking question panel.
- Results review cards.
- History table columns.

The app should remain usable at its minimum supported window size.

### 4. Light and Dark Theme Tuning

The app currently follows system appearance, but the visual language should be
hand-tuned for both light and dark mode.

Include:

- Separate background colors.
- Separate surface colors.
- Text contrast checks.
- Chart colors for both themes.
- Status colors that remain readable in both themes.

### 5. Dialog Polish

Polish custom dialogs and eventually reduce reliance on plain native message
boxes where the experience benefits from richer presentation.

Candidates:

- Mode selection.
- Mix test.
- Import summaries.
- Batch import reports.
- Confirmation dialogs.
- Unsaved changes prompts.

### 6. Micro-Interactions

Add small interaction polish where CustomTkinter supports it.

Examples:

- Better hover states.
- Active answer states.
- Disabled states.
- Current question emphasis.
- Checked-answer feedback.
- Clickable row feedback.

These should remain subtle and functional.

### 7. Chart Styling Upgrade

Improve embedded analytics charts beyond MVP color alignment.

Include:

- Cleaner gridlines.
- Better axis label spacing.
- Better long-label handling.
- More polished title treatment.
- Improved empty chart states.

### 8. App Branding Pass

Add a modest identity layer once the product UI is stable.

Possible additions:

- App icon.
- Refined app name treatment.
- Optional accent color.
- Installer and launcher visual consistency.

This should support the app's study-tool identity without making the interface
feel decorative or distracting.

## Recommended Implementation Order

1. Run the pre-MVP visual audit.
2. Define the visual foundation.
3. Apply the visual foundation to shared components.
4. Redesign the home screen.
5. Redesign the test-taking screen.
6. Redesign the results screen.
7. Redesign the test editor.
8. Redesign history and analytics.
9. Polish review flows and dialogs.
10. Add post-MVP iconography and theme refinements.

## Screen Priority Ranking

1. Home/test selector.
2. Test taking.
3. Results.
4. Test editor.
5. History.
6. Analytics.
7. Review.
8. Dialogs.

This order prioritizes first impression, core studying workflow, and the screens
users see most often.

## MVP Completion Criteria

The MVP visual overhaul is complete when:

- The home screen no longer looks like default framework output.
- The test-taking screen feels polished, readable, and focused.
- Buttons have consistent visual hierarchy.
- Cards and list rows use consistent styling.
- Results are easier to scan.
- History and analytics feel intentionally designed.
- Empty and loading states are visually consistent.
- Light and dark mode remain usable.
- No core workflows or behavior have changed.

## Before and After Acceptance Criteria

Use these checks when comparing the pre-MVP audit screenshots to the finished
MVP screens.

### App-Wide

- Primary actions are visually obvious.
- Secondary and utility actions do not compete with primary actions.
- Destructive actions are clearly marked but not overemphasized.
- Screen margins, section spacing, and card padding are consistent.
- Labels, metadata, and helper text use consistent muted styling.
- Light and dark mode both remain readable.
- Minimum window size remains usable.
- The app no longer looks like unstyled default CustomTkinter output.

### Home

- The user can quickly identify available tests.
- The main action for each test is clear.
- Test metadata is easy to scan.
- Groups and archived tests are visually distinct.
- Empty state looks intentional.

### Test Taking

- Question text is the dominant content.
- Answer choices look selectable and are easy to read.
- Timer, progress, and flag state are visible without distracting from the
  question.
- Previous, next, check answer, and finish actions have clear hierarchy.
- Practice feedback is clear and calm.

### Results

- Score summary is immediately understandable.
- Correct, incorrect, and essay statuses are visually distinct.
- User answer and correct answer are easy to compare.
- Mix-test source breakdown is readable.

### Editor

- Test metadata and question editing areas feel organized.
- The question list is scannable.
- Add/update/cancel states are visually clear.
- Validation warnings remain noticeable.

### History and Analytics

- History rows feel like a polished data list.
- Filters are easy to find and use.
- Charts match the app theme.
- Weak-topic cards are easy to scan.
- No-data states are intentional.

## Risks and Constraints

- CustomTkinter has visual limits compared with a modern web UI toolkit.
- The biggest polish gains will come from hierarchy, spacing, color discipline,
  and consistent components.
- Iconography can easily expand scope, so it should stay post-MVP unless a
  specific icon is needed to solve a clear usability problem.
- A navigation redesign may affect user expectations, so it should stay
  post-MVP.
- Theme changes can accidentally reduce dark-mode readability if not checked
  screen by screen.
- Dense screens such as the editor and history view need polish without losing
  efficiency.

## Non-Goals

The MVP visual overhaul should not:

- Change scoring behavior.
- Change import/export behavior.
- Change database schema.
- Change test session behavior.
- Add new study features.
- Redesign navigation from scratch.
- Add a marketing-style landing page.
- Replace CustomTkinter with another UI framework.
