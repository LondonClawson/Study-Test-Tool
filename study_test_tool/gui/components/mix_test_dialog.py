"""Mix test dialog — select tests and question count for a mixed test."""

from collections import OrderedDict
from typing import Dict, List, Optional, Tuple

import customtkinter as ctk

from config.settings import (
    COLOR_PRIMARY,
    FONT_FAMILY,
    FONT_SIZE_BODY,
    FONT_SIZE_HEADING,
    FONT_SIZE_SMALL,
)
from models.test import Test

UNGROUPED_LABEL = "Ungrouped"


def group_tests_by_name(
    tests_with_counts: List[Tuple[Test, int]],
) -> List[Tuple[str, List[Tuple[Test, int]]]]:
    """Organize tests by ``group_name`` for display in the mix dialog.

    Real groups are returned in alphabetical order. Tests with no group
    fall into an "Ungrouped" bucket which is always returned last.
    """
    groups: "OrderedDict[str, List[Tuple[Test, int]]]" = OrderedDict()
    ungrouped: List[Tuple[Test, int]] = []

    for test, count in tests_with_counts:
        if test.group_name:
            groups.setdefault(test.group_name, []).append((test, count))
        else:
            ungrouped.append((test, count))

    result: List[Tuple[str, List[Tuple[Test, int]]]] = [
        (name, groups[name]) for name in sorted(groups.keys())
    ]
    if ungrouped:
        result.append((UNGROUPED_LABEL, ungrouped))
    return result


class MixTestDialog(ctk.CTkToplevel):
    """Modal dialog for selecting tests and question count for a mix test."""

    def __init__(
        self,
        parent,
        tests_with_counts: List[Tuple[Test, int]],
    ) -> None:
        super().__init__(parent)
        self.title("Mix Test")
        self.geometry("450x560")
        self.resizable(False, False)

        self._result: Optional[Tuple[List[int], int]] = None
        self._tests_with_counts = tests_with_counts
        self._checkboxes: List[Tuple[ctk.CTkCheckBox, int]] = []
        self._check_vars: List[ctk.BooleanVar] = []
        self._group_vars: Dict[str, ctk.BooleanVar] = {}
        self._group_to_test_indices: Dict[str, List[int]] = {}

        # Make modal
        self.transient(parent)
        self.grab_set()

        self._build_ui()

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - 450) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - 560) // 2
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

        # Scrollable test list, organized by group
        scroll = ctk.CTkScrollableFrame(self, height=300)
        scroll.pack(fill="both", expand=True, padx=25, pady=5)

        grouped = group_tests_by_name(self._tests_with_counts)
        test_index = 0

        for group_name, group_tests in grouped:
            group_var = ctk.BooleanVar(value=False)
            self._group_vars[group_name] = group_var
            self._group_to_test_indices[group_name] = []

            group_cb = ctk.CTkCheckBox(
                scroll,
                text=group_name,
                font=(FONT_FAMILY, FONT_SIZE_BODY, "bold"),
                variable=group_var,
                command=lambda gn=group_name: self._on_group_toggled(gn),
            )
            group_cb.pack(anchor="w", pady=(8, 2), padx=2)

            for test, q_count in group_tests:
                var = ctk.BooleanVar(value=False)
                self._check_vars.append(var)

                cb = ctk.CTkCheckBox(
                    scroll,
                    text=f"{test.name}  ({q_count} questions)",
                    font=(FONT_FAMILY, FONT_SIZE_BODY),
                    variable=var,
                    command=lambda gn=group_name: self._on_test_checkbox_changed(gn),
                )
                cb.pack(anchor="w", pady=2, padx=25)
                self._checkboxes.append((cb, test.id))
                self._group_to_test_indices[group_name].append(test_index)
                test_index += 1

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
        """Select all test checkboxes (and group headers)."""
        for var in self._check_vars:
            var.set(True)
        for var in self._group_vars.values():
            var.set(True)
        self._on_checkbox_changed()

    def _deselect_all(self) -> None:
        """Deselect all test checkboxes (and group headers)."""
        for var in self._check_vars:
            var.set(False)
        for var in self._group_vars.values():
            var.set(False)
        self._on_checkbox_changed()

    def _on_group_toggled(self, group_name: str) -> None:
        """Toggle every test in a group when its header checkbox changes."""
        is_selected = self._group_vars[group_name].get()
        for idx in self._group_to_test_indices[group_name]:
            self._check_vars[idx].set(is_selected)
        self._on_checkbox_changed()

    def _on_test_checkbox_changed(self, group_name: str) -> None:
        """Sync the group header when an individual test checkbox changes.

        The group header is checked only when every test in the group is
        selected; unchecking any test unchecks the group.
        """
        indices = self._group_to_test_indices[group_name]
        all_selected = all(self._check_vars[i].get() for i in indices)
        self._group_vars[group_name].set(all_selected)
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
