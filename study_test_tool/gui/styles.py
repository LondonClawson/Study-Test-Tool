"""Shared visual style roles for CustomTkinter GUI code."""

from typing import Dict, Tuple, Union

from config.settings import (
    COLOR_ANSWERED,
    COLOR_CORRECT,
    COLOR_CURRENT,
    COLOR_DANGER,
    COLOR_FLAGGED,
    COLOR_INCORRECT,
    COLOR_PRIMARY,
    COLOR_SUCCESS,
    COLOR_UNANSWERED,
    COLOR_WARNING,
    FONT_FAMILY,
    FONT_SIZE_BODY,
    FONT_SIZE_HEADING,
    FONT_SIZE_SMALL,
    FONT_SIZE_TITLE,
)

ThemeColor = Union[str, Tuple[str, str]]
FontValue = Union[Tuple[str, int], Tuple[str, int, str]]
WidgetStyle = Dict[str, Union[int, ThemeColor]]

# Base surfaces
COLOR_APP_BG: ThemeColor = ("#f3f5f7", "#1f2023")
COLOR_SURFACE: ThemeColor = ("#ffffff", "#2b2d31")
COLOR_SURFACE_SUBTLE: ThemeColor = ("#f7f9fb", "#24262a")
COLOR_SURFACE_MUTED: ThemeColor = ("#e9edf1", "#34373d")
COLOR_BORDER: ThemeColor = ("#d6dde5", "#3c4148")
COLOR_DIVIDER: ThemeColor = ("#e5eaf0", "#343941")

# Text roles
COLOR_TEXT_PRIMARY: ThemeColor = ("#1f2328", "#f2f5f8")
COLOR_TEXT_SECONDARY: ThemeColor = ("#4f5b67", "#c4ccd4")
COLOR_TEXT_MUTED: ThemeColor = ("#697684", "#8f98a3")
COLOR_TEXT_DISABLED: ThemeColor = ("#9ca6b1", "#666f7a")
COLOR_TEXT_INVERSE: ThemeColor = "#ffffff"

# Action roles
COLOR_PRIMARY_HOVER: ThemeColor = "#185a8d"
COLOR_SECONDARY: ThemeColor = "#6c757d"
COLOR_SECONDARY_HOVER: ThemeColor = "#5a6268"
COLOR_DANGER_HOVER: ThemeColor = "#c9302c"
COLOR_WARNING_HOVER: ThemeColor = "#d9972d"
COLOR_SUCCESS_HOVER: ThemeColor = "#258a5e"
COLOR_SPECIAL: ThemeColor = "#7b2d8e"
COLOR_SPECIAL_HOVER: ThemeColor = "#5e2270"

# Status roles
COLOR_STATUS_CORRECT: ThemeColor = COLOR_CORRECT
COLOR_STATUS_INCORRECT: ThemeColor = COLOR_INCORRECT
COLOR_STATUS_WARNING: ThemeColor = COLOR_WARNING
COLOR_STATUS_ANSWERED: ThemeColor = COLOR_ANSWERED
COLOR_STATUS_CURRENT: ThemeColor = COLOR_CURRENT
COLOR_STATUS_UNANSWERED: ThemeColor = COLOR_UNANSWERED
COLOR_STATUS_NEUTRAL: ThemeColor = COLOR_UNANSWERED
COLOR_STATUS_FLAGGED: ThemeColor = COLOR_FLAGGED

# Radius roles
RADIUS_ROW = 4
RADIUS_CONTROL = 6
RADIUS_CARD = 8

# Spacing roles
SPACE_2 = 2
SPACE_4 = 4
SPACE_8 = 8
SPACE_12 = 12
SPACE_16 = 16
SPACE_24 = 24
SPACE_32 = 32

# Typography roles
FONT_PAGE_TITLE: FontValue = (FONT_FAMILY, FONT_SIZE_TITLE, "bold")
FONT_SECTION_TITLE: FontValue = (FONT_FAMILY, FONT_SIZE_HEADING, "bold")
FONT_CARD_TITLE: FontValue = (FONT_FAMILY, 16, "bold")
FONT_BODY: FontValue = (FONT_FAMILY, FONT_SIZE_BODY)
FONT_BODY_BOLD: FontValue = (FONT_FAMILY, FONT_SIZE_BODY, "bold")
FONT_METADATA: FontValue = (FONT_FAMILY, FONT_SIZE_SMALL)
FONT_COMPACT: FontValue = (FONT_FAMILY, 11)
FONT_COMPACT_BOLD: FontValue = (FONT_FAMILY, 11, "bold")

COLOR_ROLES: Dict[str, ThemeColor] = {
    "app_bg": COLOR_APP_BG,
    "surface": COLOR_SURFACE,
    "surface_subtle": COLOR_SURFACE_SUBTLE,
    "surface_muted": COLOR_SURFACE_MUTED,
    "border": COLOR_BORDER,
    "divider": COLOR_DIVIDER,
    "text_primary": COLOR_TEXT_PRIMARY,
    "text_secondary": COLOR_TEXT_SECONDARY,
    "text_muted": COLOR_TEXT_MUTED,
    "text_disabled": COLOR_TEXT_DISABLED,
    "text_inverse": COLOR_TEXT_INVERSE,
    "primary": COLOR_PRIMARY,
    "primary_hover": COLOR_PRIMARY_HOVER,
    "secondary": COLOR_SECONDARY,
    "secondary_hover": COLOR_SECONDARY_HOVER,
    "danger": COLOR_DANGER,
    "danger_hover": COLOR_DANGER_HOVER,
    "warning": COLOR_WARNING,
    "warning_hover": COLOR_WARNING_HOVER,
    "success": COLOR_SUCCESS,
    "success_hover": COLOR_SUCCESS_HOVER,
    "special": COLOR_SPECIAL,
    "special_hover": COLOR_SPECIAL_HOVER,
    "status_correct": COLOR_STATUS_CORRECT,
    "status_incorrect": COLOR_STATUS_INCORRECT,
    "status_warning": COLOR_STATUS_WARNING,
    "status_answered": COLOR_STATUS_ANSWERED,
    "status_current": COLOR_STATUS_CURRENT,
    "status_unanswered": COLOR_STATUS_UNANSWERED,
    "status_neutral": COLOR_STATUS_NEUTRAL,
    "status_flagged": COLOR_STATUS_FLAGGED,
}

PROGRESS_STATUS_COLORS: Dict[str, ThemeColor] = {
    "current": COLOR_STATUS_CURRENT,
    "flagged": COLOR_STATUS_FLAGGED,
    "answered": COLOR_STATUS_ANSWERED,
    "unanswered": COLOR_STATUS_UNANSWERED,
}

BUTTON_ROLES: Dict[str, WidgetStyle] = {
    "primary": {
        "fg_color": COLOR_PRIMARY,
        "hover_color": COLOR_PRIMARY_HOVER,
        "text_color": COLOR_TEXT_INVERSE,
    },
    "secondary": {
        "fg_color": COLOR_SECONDARY,
        "hover_color": COLOR_SECONDARY_HOVER,
        "text_color": COLOR_TEXT_INVERSE,
    },
    "danger": {
        "fg_color": COLOR_DANGER,
        "hover_color": COLOR_DANGER_HOVER,
        "text_color": COLOR_TEXT_INVERSE,
    },
    "warning": {
        "fg_color": COLOR_WARNING,
        "hover_color": COLOR_WARNING_HOVER,
        "text_color": COLOR_TEXT_INVERSE,
    },
    "success": {
        "fg_color": COLOR_SUCCESS,
        "hover_color": COLOR_SUCCESS_HOVER,
        "text_color": COLOR_TEXT_INVERSE,
    },
    "special": {
        "fg_color": COLOR_SPECIAL,
        "hover_color": COLOR_SPECIAL_HOVER,
        "text_color": COLOR_TEXT_INVERSE,
    },
    "tertiary": {
        "fg_color": "transparent",
        "hover_color": COLOR_SURFACE_SUBTLE,
        "text_color": COLOR_TEXT_SECONDARY,
        "border_color": COLOR_BORDER,
        "border_width": 1,
    },
}


def get_color(role: str) -> ThemeColor:
    """Return a semantic color role for GUI widgets."""
    return COLOR_ROLES[role]


def get_button_style(role: str) -> WidgetStyle:
    """Return CustomTkinter keyword values for a semantic button role."""
    return BUTTON_ROLES[role].copy()
