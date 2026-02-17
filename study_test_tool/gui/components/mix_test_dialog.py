"""Mix test dialog — select tests and question count for a mixed test."""

from typing import List, Optional, Tuple

import customtkinter as ctk

from config.settings import (
    COLOR_PRIMARY,
    FONT_FAMILY,
    FONT_SIZE_BODY,
    FONT_SIZE_HEADING,
    FONT_SIZE_SMALL,
)
from models.test import Test


class MixTestDialog(ctk.CTkToplevel):
    """Modal dialog for selecting tests and question count for a mix test."""

    def __init__(
        self,
        parent,
        tests_with_counts: List[Tuple[Test, int]],
    ) -> None:
        super().__init__(parent)
        self.title("Mix Test")
        self.geometry("450x480")
        self.resizable(False, False)

        self._result: Optional[Tuple[List[int], int]] = None
        self._tests_with_counts = tests_with_counts
        self._checkboxes: List[Tuple[ctk.CTkCheckBox, int]] = []
        self._check_vars: List[ctk.BooleanVar] = []

        # Make modal
        self.transient(parent)
        self.grab_set()

        self._build_ui()

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - 450) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - 480) // 2
        self.geometry(f"+{x}+{y}")

    def _build_ui(self) -> None:
        """Build the dialog layout."""
        ctk.CTkLabel(
            self,
            text="Mix Test",
            font=(FONT_FAMILY, FONT_SIZE_HEADING, "bold"),
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            self,
            text="Select tests to draw questions from:",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
            text_color="gray",
        ).pack(pady=(0, 10))

        # Select All / Deselect All buttons
        sel_frame = ctk.CTkFrame(self, fg_color="transparent")
        sel_frame.pack(fill="x", padx=25, pady=(0, 5))

        ctk.CTkButton(
            sel_frame,
            text="Select All",
            width=90,
            height=28,
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            command=self._select_all,
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            sel_frame,
            text="Deselect All",
            width=90,
            height=28,
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            fg_color="gray",
            command=self._deselect_all,
        ).pack(side="left", padx=3)

        # Scrollable test list
        scroll = ctk.CTkScrollableFrame(self, height=220)
        scroll.pack(fill="both", expand=True, padx=25, pady=5)

        for test, q_count in self._tests_with_counts:
            var = ctk.BooleanVar(value=False)
            self._check_vars.append(var)

            cb = ctk.CTkCheckBox(
                scroll,
                text=f"{test.name}  ({q_count} questions)",
                font=(FONT_FAMILY, FONT_SIZE_BODY),
                variable=var,
                command=self._on_checkbox_changed,
            )
            cb.pack(anchor="w", pady=3, padx=5)
            self._checkboxes.append((cb, test.id))

        # Total available label
        self._total_label = ctk.CTkLabel(
            self,
            text="Total available: 0",
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            text_color="gray",
        )
        self._total_label.pack(pady=(5, 2))

        # Question count input
        count_frame = ctk.CTkFrame(self, fg_color="transparent")
        count_frame.pack(fill="x", padx=25, pady=5)

        ctk.CTkLabel(
            count_frame,
            text="Number of questions:",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
        ).pack(side="left", padx=(0, 10))

        self._count_entry = ctk.CTkEntry(count_frame, width=80)
        self._count_entry.insert(0, "10")
        self._count_entry.pack(side="left")

        # OK / Cancel buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=25, pady=(10, 15))

        ctk.CTkButton(
            btn_frame,
            text="Start Mix Test",
            width=130,
            fg_color=COLOR_PRIMARY,
            command=self._on_ok,
        ).pack(side="left", padx=5, expand=True)

        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=100,
            fg_color="gray",
            command=self.destroy,
        ).pack(side="right", padx=5, expand=True)

    def _on_checkbox_changed(self) -> None:
        """Update the total available label when checkboxes change."""
        total = self._get_total_available()
        self._total_label.configure(text=f"Total available: {total}")

    def _get_total_available(self) -> int:
        """Count total questions from selected tests."""
        total = 0
        for i, var in enumerate(self._check_vars):
            if var.get():
                total += self._tests_with_counts[i][1]
        return total

    def _select_all(self) -> None:
        """Select all test checkboxes."""
        for var in self._check_vars:
            var.set(True)
        self._on_checkbox_changed()

    def _deselect_all(self) -> None:
        """Deselect all test checkboxes."""
        for var in self._check_vars:
            var.set(False)
        self._on_checkbox_changed()

    def _on_ok(self) -> None:
        """Validate and return selected tests and count."""
        selected_ids = []
        for i, var in enumerate(self._check_vars):
            if var.get():
                selected_ids.append(self._checkboxes[i][1])

        if not selected_ids:
            return  # Nothing selected

        try:
            count = int(self._count_entry.get().strip())
        except ValueError:
            return
        if count <= 0:
            return

        self._result = (selected_ids, count)
        self.destroy()

    def get_result(self) -> Optional[Tuple[List[int], int]]:
        """Return the selection after dialog closes.

        Returns:
            Tuple of (selected_test_ids, question_count), or None if cancelled.
        """
        self.wait_window()
        return self._result
