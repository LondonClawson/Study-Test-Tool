"""Inline formatting toolbar for question editor fields."""

import tkinter as tk

import customtkinter as ctk

from config.settings import FONT_FAMILY, FONT_SIZE_BODY
from gui.styles import FONT_BODY_BOLD, SPACE_4, get_button_style


class FormattingToolbar(ctk.CTkFrame):
    """Apply markdown-lite markers to the currently active editor field."""

    def __init__(self, parent, target_getter, **kwargs) -> None:
        kwargs.setdefault("fg_color", "transparent")
        super().__init__(parent, **kwargs)
        self._target_getter = target_getter
        self._build_button("B", "**", "**", FONT_BODY_BOLD)
        self._build_button("I", "*", "*", (FONT_FAMILY, FONT_SIZE_BODY, "italic"))
        self._build_button(
            "U",
            "<u>",
            "</u>",
            (FONT_FAMILY, FONT_SIZE_BODY, "underline"),
        )

    def _build_button(self, label: str, prefix: str, suffix: str, font) -> None:
        ctk.CTkButton(
            self,
            text=label,
            width=32,
            height=28,
            font=font,
            command=lambda: self._apply_markup(prefix, suffix),
            **get_button_style("tertiary"),
        ).pack(side="left", padx=(0, SPACE_4))

    def _apply_markup(self, prefix: str, suffix: str) -> None:
        widget = self._target_getter()
        if widget is None:
            return
        target = _inner_text_widget(widget)
        if isinstance(target, tk.Text):
            _apply_to_text(target, prefix, suffix)
        elif isinstance(target, tk.Entry):
            _apply_to_entry(target, prefix, suffix)
        target.focus_set()


def _inner_text_widget(widget):
    return getattr(widget, "_textbox", getattr(widget, "_entry", widget))


def _apply_to_text(widget: tk.Text, prefix: str, suffix: str) -> None:
    try:
        start = widget.index("sel.first")
        end = widget.index("sel.last")
    except tk.TclError:
        cursor = widget.index("insert")
        widget.insert(cursor, prefix + suffix)
        widget.mark_set("insert", f"{cursor}+{len(prefix)}c")
        return

    selected = widget.get(start, end)
    widget.delete(start, end)
    widget.insert(start, prefix + selected + suffix)
    widget.tag_remove("sel", "1.0", "end")


def _apply_to_entry(widget: tk.Entry, prefix: str, suffix: str) -> None:
    try:
        start = widget.index("sel.first")
        end = widget.index("sel.last")
    except tk.TclError:
        cursor = widget.index("insert")
        widget.insert(cursor, prefix + suffix)
        widget.icursor(cursor + len(prefix))
        return

    selected = widget.get()[start:end]
    widget.delete(start, end)
    widget.insert(start, prefix + selected + suffix)
    widget.selection_clear()
