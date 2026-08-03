"""Collapsible group widget for grouping test cards with expand/collapse."""

from typing import Callable, Optional

import customtkinter as ctk

from gui.styles import (
    FONT_METADATA,
    FONT_SECTION_TITLE,
    SPACE_4,
    SPACE_8,
    SPACE_12,
    SPACE_16,
    get_button_style,
    get_card_style,
    get_color,
)


class CollapsibleGroup(ctk.CTkFrame):
    """A collapsible container with a header showing group name and test count."""

    def __init__(
        self,
        parent,
        group_name: str,
        test_count: int,
        expanded: bool = False,
        archive_callback: Optional[Callable] = None,
        on_expand: Optional[Callable[[], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(parent, fg_color="transparent", **kwargs)
        self._is_expanded = expanded
        self._group_name = group_name
        self._test_count = test_count
        self._archive_callback = archive_callback
        self._on_expand = on_expand

        self._build_header()
        self._content_frame = ctk.CTkFrame(self, fg_color="transparent")
        if self._is_expanded:
            self._content_frame.pack(fill="x", padx=SPACE_12, pady=(0, SPACE_8))

    def _build_header(self) -> None:
        """Build the header row with toggle button, name, and count badge."""
        header = ctk.CTkFrame(self, **get_card_style("default"))
        header.pack(fill="x", padx=SPACE_4, pady=(SPACE_8, SPACE_4))

        arrow = "▼" if self._is_expanded else "▶"
        label = self._make_label(arrow)
        self._toggle_btn = ctk.CTkButton(
            header,
            text=label,
            anchor="w",
            fg_color="transparent",
            hover_color=get_color("surface_subtle"),
            text_color=get_color("primary"),
            font=FONT_SECTION_TITLE,
            command=self.toggle,
            height=42,
        )
        self._toggle_btn.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(SPACE_8, SPACE_4),
            pady=SPACE_8,
        )

        if self._archive_callback is not None:
            ctk.CTkButton(
                header,
                text="Archive Group",
                width=112,
                height=32,
                font=FONT_METADATA,
                command=self._archive_callback,
                **get_button_style("secondary"),
            ).pack(side="right", padx=(SPACE_4, SPACE_12))

    def _make_label(self, arrow: str) -> str:
        """Return the formatted button label string."""
        count = self._test_count
        noun = "test" if count == 1 else "tests"
        return f"{arrow}  {self._group_name}  ({count} {noun})"

    def toggle(self) -> None:
        """Toggle the expanded/collapsed state."""
        self._is_expanded = not self._is_expanded
        arrow = "▼" if self._is_expanded else "▶"
        self._toggle_btn.configure(text=self._make_label(arrow))
        if self._is_expanded:
            if self._on_expand is not None:
                self._on_expand()
            self._content_frame.pack(fill="x", padx=SPACE_12, pady=(0, SPACE_8))
        else:
            self._content_frame.pack_forget()

    @property
    def is_expanded(self) -> bool:
        """Return the current expanded state."""
        return self._is_expanded

    @property
    def content_frame(self) -> ctk.CTkFrame:
        """Return the inner frame where test cards should be placed."""
        return self._content_frame
