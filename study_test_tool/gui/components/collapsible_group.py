"""Collapsible group widget for grouping test cards with expand/collapse."""

from typing import Callable, Optional

import customtkinter as ctk

from config.settings import (
    COLOR_PRIMARY,
    FONT_FAMILY,
    FONT_SIZE_HEADING,
    FONT_SIZE_SMALL,
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
        **kwargs,
    ) -> None:
        super().__init__(parent, fg_color="transparent", **kwargs)
        self._is_expanded = expanded
        self._group_name = group_name
        self._test_count = test_count
        self._archive_callback = archive_callback

        self._build_header()
        self._content_frame = ctk.CTkFrame(self, fg_color="transparent")
        if self._is_expanded:
            self._content_frame.pack(fill="x", padx=0, pady=(0, 4))

    def _build_header(self) -> None:
        """Build the header row with toggle button, name, and count badge."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=5, pady=(8, 2))

        arrow = "▼" if self._is_expanded else "▶"
        label = self._make_label(arrow)
        self._toggle_btn = ctk.CTkButton(
            header,
            text=label,
            anchor="w",
            fg_color="transparent",
            hover_color=("#e0e0e0", "#3a3a3a"),
            text_color=COLOR_PRIMARY,
            font=(FONT_FAMILY, FONT_SIZE_HEADING, "bold"),
            command=self.toggle,
            width=400,
        )
        self._toggle_btn.pack(side="left", fill="x", expand=True)

        if self._archive_callback is not None:
            ctk.CTkButton(
                header,
                text="Archive Group",
                width=120,
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                fg_color="#6c757d",
                hover_color="#5a6268",
                command=self._archive_callback,
            ).pack(side="right", padx=5)

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
            self._content_frame.pack(fill="x", padx=0, pady=(0, 4))
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
