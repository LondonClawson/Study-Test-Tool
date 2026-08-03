"""Read-only formatted text widget for markdown-lite study content."""

import tkinter as tk
from tkinter import font as tkfont
from typing import Optional

import customtkinter as ctk

from gui.styles import ThemeColor, get_color, get_text_style
from utils.markdown_lite import TextSegment, parse_markdown_lite


class FormattedText(ctk.CTkFrame):
    """Render markdown-lite text using Tk text tags."""

    def __init__(
        self,
        parent,
        text: str = "",
        text_role: str = "body",
        text_color: Optional[ThemeColor] = None,
        background_color: Optional[ThemeColor] = None,
        cursor: str = "arrow",
        max_lines: Optional[int] = None,
        **kwargs,
    ) -> None:
        kwargs.setdefault("fg_color", "transparent")
        super().__init__(parent, **kwargs)
        style = get_text_style(text_role)
        self._base_font_value = style["font"]
        self._text_color = text_color or style["text_color"]
        self._background_color = background_color or get_color("surface")
        self._max_lines = max_lines
        self._resize_callback = None
        self._rendered_height = None

        self._text = tk.Text(
            self,
            wrap="word",
            height=1,
            borderwidth=0,
            highlightthickness=0,
            padx=0,
            pady=0,
            spacing1=0,
            spacing2=0,
            spacing3=0,
            takefocus=0,
            cursor=cursor,
            exportselection=False,
        )
        self._text.pack(fill="x", expand=True)
        self._text.bind("<Configure>", self._schedule_resize)
        self._configure_colors()
        self.set_text(text)

    def set_text(self, text: str) -> None:
        """Replace the rendered markdown-lite text."""
        self._text.configure(state="normal")
        self._text.delete("1.0", "end")
        for segment in parse_markdown_lite(text or ""):
            self._insert_segment(segment)
        self._text.configure(state="disabled")
        self._schedule_resize()

    def configure_text_color(self, text_color: ThemeColor) -> None:
        """Update the foreground color for all formatted spans."""
        self._text_color = text_color
        self._configure_colors()

    def configure_background_color(self, background_color: ThemeColor) -> None:
        """Update the widget background color."""
        self._background_color = background_color
        self._configure_colors()

    def configure_colors(
        self,
        text_color: Optional[ThemeColor] = None,
        background_color: Optional[ThemeColor] = None,
    ) -> None:
        """Update foreground and/or background colors."""
        if text_color is not None:
            self._text_color = text_color
        if background_color is not None:
            self._background_color = background_color
        self._configure_colors()

    def bind_click(self, callback) -> None:
        """Bind a click callback to the frame and its inner text widget."""
        self.bind("<Button-1>", callback)
        self._text.bind("<Button-1>", callback)

    def unbind_click(self) -> None:
        """Remove click bindings from the frame and its inner text widget."""
        self.unbind("<Button-1>")
        self._text.unbind("<Button-1>")

    def configure_cursor(self, cursor: str) -> None:
        """Set the cursor used by the inner text widget."""
        self.configure(cursor=cursor)
        self._text.configure(cursor=cursor)

    def _insert_segment(self, segment: TextSegment) -> None:
        tag = self._tag_for_segment(segment)
        self._text.insert("end", segment.text, tag)

    def _tag_for_segment(self, segment: TextSegment) -> str:
        tag = (
            "bold" if segment.bold else "regular",
            "italic" if segment.italic else "roman",
            "underline" if segment.underline else "plain",
        )
        tag_name = "_".join(tag)
        if tag_name not in self._text.tag_names():
            font = _font_from_value(
                self._base_font_value,
                bold=segment.bold,
                italic=segment.italic,
                underline=segment.underline,
            )
            self._text.tag_configure(tag_name, font=font)
        return tag_name

    def _configure_colors(self) -> None:
        fg = _resolve_color(self._text_color)
        bg = _resolve_color(self._background_color)
        self._text.configure(foreground=fg, background=bg, insertbackground=fg)
        for tag in self._text.tag_names():
            if tag == "sel":
                continue
            self._text.tag_configure(tag, foreground=fg, background=bg)

    def _schedule_resize(self, _event=None) -> None:
        """Schedule one content-height measurement for the current idle cycle."""
        if self._resize_callback is None:
            self._resize_callback = self.after_idle(self._resize_to_content)

    def _resize_to_content(self) -> None:
        """Resize only when the displayed line count changes."""
        self._resize_callback = None
        try:
            count = self._text.count("1.0", "end-1c", "displaylines")
        except tk.TclError:
            return
        lines = count[0] if count else 1
        if self._max_lines is not None:
            lines = min(lines, self._max_lines)
        height = max(lines, 1)
        if height != self._rendered_height:
            self._text.configure(height=height)
            self._rendered_height = height

    def destroy(self) -> None:
        """Cancel a queued resize before destroying this widget."""
        if self._resize_callback is not None:
            try:
                self.after_cancel(self._resize_callback)
            except tk.TclError:
                pass
            self._resize_callback = None
        super().destroy()


def _resolve_color(color: ThemeColor) -> str:
    if isinstance(color, tuple):
        return color[1] if ctk.get_appearance_mode() == "Dark" else color[0]
    return color


def _font_from_value(
    font_value,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
) -> tkfont.Font:
    family = font_value[0]
    size = font_value[1]
    style = font_value[2] if len(font_value) > 2 else ""
    style_parts = set(str(style).split())
    return tkfont.Font(
        family=family,
        size=size,
        weight="bold" if bold or "bold" in style_parts else "normal",
        slant="italic" if italic or "italic" in style_parts else "roman",
        underline=1 if underline or "underline" in style_parts else 0,
    )
