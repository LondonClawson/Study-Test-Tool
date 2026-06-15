# Visual Foundation Decisions

## Metadata

- Summary ID: CTX-FOUNDATION.
- Produced by: `visual_overhaul_project/04_stories/STORY-003_visual_foundation_spec.md`.
- Created: 2026-06-02.
- Last updated: 2026-06-15.
- Status: Ready.
- Source inputs: `baseline_visual_audit.md`, `style_inventory.md`, `current_visual_state_seed.md`, and `VISUAL_OVERHAUL_PLAN.md`.

## Purpose

This file defines the accepted MVP visual foundation for implementation stories.
PM review accepted CTX-FOUNDATION as Ready on 2026-06-15.

## Design Direction

Use a refined version of the current blue macOS productivity style. The app
should feel calmer, clearer, and more intentional without changing workflows,
navigation, scoring, import/export, persistence, or test logic.

Primary goals:

- Preserve a practical desktop study-tool feel.
- Use blue as the main action identity.
- Use color for role and state, not decoration.
- Add clearer surface separation in both light and dark mode.
- Standardize repeated cards, rows, headers, buttons, and empty states before
  broad screen redesign.

## Semantic Color Roles

Use semantic names in implementation rather than screen-specific or raw color
names. CustomTkinter tuple colors should be supported wherever widgets need
light/dark-specific values.

### Base Surfaces

| Role | Light | Dark | Use |
| --- | --- | --- | --- |
| `app_bg` | `#f3f5f7` | `#1f2023` | Top-level screen background. |
| `surface` | `#ffffff` | `#2b2d31` | Primary cards, panels, dialogs. |
| `surface_subtle` | `#f7f9fb` | `#24262a` | Nested sections and quiet content areas. |
| `surface_muted` | `#e9edf1` | `#34373d` | Archived/disabled cards and low-priority blocks. |
| `border` | `#d6dde5` | `#3c4148` | Card, row, input, and dialog borders. |
| `divider` | `#e5eaf0` | `#343941` | Separators and table/header dividers. |

### Text

| Role | Light | Dark | Use |
| --- | --- | --- | --- |
| `text_primary` | `#1f2328` | `#f2f5f8` | Titles and primary content. |
| `text_secondary` | `#4f5b67` | `#c4ccd4` | Metadata and secondary labels. |
| `text_muted` | `#697684` | `#8f98a3` | Empty-state helper text, low-emphasis metadata. |
| `text_disabled` | `#9ca6b1` | `#666f7a` | Disabled controls or unavailable counts. |
| `text_inverse` | `#ffffff` | `#ffffff` | Text on filled action colors. |

### Action Colors

| Role | Base | Hover | Use |
| --- | --- | --- | --- |
| `primary` | `#1f6aa5` | `#185a8d` | Main next actions: Take Test, Save, Start Review, Retake when primary. |
| `secondary` | `#6c757d` | `#5a6268` | Navigation and neutral actions: Back, Cancel, History. |
| `tertiary` | transparent/surface | surface hover | Low-emphasis utility actions where CTk supports it. |
| `danger` | `#d9534f` | `#c9302c` | Destructive actions: Delete, irreversible removal. |
| `warning` | `#f0ad4e` | `#d9972d` | Caution/attention actions: Review Missed, flagged emphasis. |
| `success` | `#2fa572` | `#258a5e` | Positive outcomes and confirmed success states. |
| `special` | `#7b2d8e` | `#5e2270` | Compound/special workflows such as Mix Test. |

Resolved role decisions:

- Mix Test remains a special action for MVP because it is a distinct compound
  workflow on the home screen.
- Success should be reserved primarily for positive outcomes/statuses. Workflow
  starts such as Start Review should use primary unless a story has a specific
  reason to keep success.
- Finish Test should not use danger styling. It should use primary or secondary
  emphasis depending on screen hierarchy because it is normal completion, not a
  destructive action.
- Destructive actions should be visible but visually secondary to the main
  workflow until needed.

### Status Colors

| Role | Color | Use |
| --- | --- | --- |
| `status_correct` | `#2fa572` | Correct answers, strong topics, positive result badges. |
| `status_incorrect` | `#d9534f` | Incorrect answers, weak topics, error state badges. |
| `status_warning` | `#f0ad4e` | Flagged questions, moderate topics, caution badges. |
| `status_answered` | `#1f6aa5` | Answered progress state. |
| `status_current` | `#2fa572` | Current question/progress state. |
| `status_unanswered` | `#6c757d` | Unanswered progress state. |
| `status_neutral` | `#6c757d` | Essay/self-evaluation and neutral badges. |

## Typography

Continue using the system-safe `Helvetica` family for MVP. Improve hierarchy
through named font roles rather than new font dependencies.

| Role | Size | Weight | Use |
| --- | --- | --- | --- |
| `page_title` | 24 | bold | Screen titles and primary page identity. |
| `section_title` | 18 | bold | Major sections inside a screen. |
| `card_title` | 16 | bold | Test cards, question cards, results cards. |
| `body` | 14 | normal | Main copy and labels. |
| `body_bold` | 14 | bold | Inline emphasis and row headings. |
| `metadata` | 12 | normal | Counts, dates, helper text, secondary facts. |
| `compact` | 11 | normal/bold | Progress buttons, dense table labels. |

Do not scale font size with window width. Use wraplength and layout constraints
for long titles, questions, answers, and metadata.

## Spacing And Radius

Use a small spacing scale so screens stay dense enough for repeated studying:

- `space_2`: 2 px.
- `space_4`: 4 px.
- `space_8`: 8 px.
- `space_12`: 12 px.
- `space_16`: 16 px.
- `space_24`: 24 px.
- `space_32`: 32 px.

Radius rules:

- `radius_row`: 4 px for compact rows, progress buttons, and table-like items.
- `radius_control`: 6 px for inputs, small controls, and compact cards.
- `radius_card`: 8 px for primary cards, panels, dialogs, and empty states.
- Do not exceed 8 px for normal cards unless an existing CustomTkinter widget
  requires it.

## Component Patterns

### Page Header

- Use a consistent top structure: optional Back button, page title, optional
  right-side metadata/actions.
- Back buttons remain text secondary buttons for MVP. Do not introduce an icon
  system in foundation work.
- Home may keep a centered product title, but action hierarchy below it must be
  reduced.

### Buttons

- Use role helpers before broad screen adoption.
- Keep callbacks, command wiring, disabled states, and confirmation flows
  unchanged.
- Prefer one primary action per local workflow area.
- Secondary and tertiary actions should not visually compete with primary.
- Danger should be reserved for destructive actions only.

### Cards And Rows

- Cards use `surface`, `border`, `radius_card`, 12-16 px internal padding, and
  clear title/metadata separation.
- Compact rows use `surface_subtle` or transparent background, `radius_row`, and
  subtle hover/selected treatment when clickable.
- Archived tests use both `surface_muted` and muted/secondary text treatment.
- Do not extract one generic card component until a story proves it works for a
  narrow family; home cards, result cards, editor cards, and review cards have
  different behavior.

### Empty, Loading, And Error States

- Replace plain gray labels with a shared empty-state surface.
- Empty states should include a concise title, one helper sentence, and a
  context-appropriate action only when an action is already part of the current
  workflow.
- Loading states should use the same surface and text roles, not raw gray text.
- Error states may use `status_incorrect` sparingly with explanatory text.

### Badges And Status Labels

- Use compact pill-like labels or small status text with semantic colors.
- Correct, incorrect, essay/neutral, flagged, answered, unanswered, and current
  states must remain visually distinct in light and dark mode.
- Avoid using the same gray for secondary buttons, muted text, essay statuses,
  and disabled states.

### Charts

- Charts use a data-visualization palette aligned with the app but separate from
  button colors.
- Matplotlib figure and axes backgrounds must both match the active app theme.
- Proposed chart roles:
  - `chart_bg`: same as `surface`.
  - `chart_plot_bg`: same as `surface_subtle`.
  - `chart_text`: same as `text_secondary`.
  - `chart_grid`: same as `divider`.
  - `chart_series_primary`: `#2f80d1`.
  - `chart_series_secondary`: `#7b2d8e`.
  - `chart_series_success`: `#2fa572`.
  - `chart_series_warning`: `#f0ad4e`.
  - `chart_series_danger`: `#d9534f`.

## Screen Guidance

- Home: reduce top-action competition, make main study/create actions clearer,
  treat Mix Test as special, and use a designed empty state.
- Test taking: make question content dominant, turn answer options into
  selectable rows, move Finish away from danger styling, and make practice
  feedback a designed status surface.
- Results: make score summary stronger, use status badges, and structure user
  answer versus correct answer comparisons.
- Editor: keep the two-column workflow, but use clearer panel hierarchy and
  card/list treatment.
- History: make rows feel clickable and align headers/filters with shared data
  view spacing.
- Analytics: align chart backgrounds and topic status colors with the
  foundation.
- Review: reduce control-stack heaviness and align missed-question cards with
  the shared card pattern.
- Dialogs: style custom mode and mix dialogs with shared surfaces/buttons. Keep
  native messageboxes and file dialogs behavior-only for MVP.

## Implementation Constraints

- Do not change services, database access, scoring, import/export, session
  state, review scope logic, mix-test behavior, or navigation contracts.
- Preserve `App.show_frame(name, **kwargs)` and each frame's `on_show` refresh
  behavior.
- Preserve all current confirmation and validation flows unless a dedicated
  story changes them.
- Keep Python 3.9 compatibility.
- Work within CustomTkinter primitives; do not add a new design-system
  dependency.
- Prefer a small GUI style entry point over broad refactors in screen files.

## Recommended Implementation Order

1. `STORY-004_shared_style_entrypoints.md`: introduce semantic tokens and the
   smallest role helpers.
2. `STORY-005_button_hierarchy.md`: apply roles in a narrow high-traffic area.
3. `STORY-006_card_and_list_patterns.md`: define shared card/list guidance with
   a named pilot area.
4. `STORY-007_page_header_pattern.md`: align page headers after button roles
   exist.
5. Screen-specific stories: apply foundation rules in the assigned screen only.

## Open Decisions

No foundation-blocking design decisions remain. Later stories may still make
local implementation choices such as exact helper names, which screen pilots a
shared pattern, or whether a native dialog should ever be replaced by a custom
dialog after MVP.

## Refresh Triggers

Update this summary when:

- PM/reviewer changes any proposed foundation role before acceptance.
- Shared style entry points choose different names or discover an unsupported
  CustomTkinter state.
- A screen implementation finds that a role is incomplete or fails light/dark
  readability.
- The app changes its base CustomTkinter theme or appearance-mode behavior.
