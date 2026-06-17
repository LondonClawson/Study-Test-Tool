"""Mix test dialog — select tests and question count for a mixed test."""

from typing import Dict, List, Optional, Tuple

import customtkinter as ctk

from gui.styles import (
    RADIUS_CARD,
    RADIUS_ROW,
    SPACE_12,
    SPACE_16,
    SPACE_24,
    SPACE_4,
    SPACE_8,
    get_button_style,
    get_card_style,
    get_color,
    get_text_style,
)
from gui.mix_test_display import group_tests_by_name
from models.test import Test


class MixTestDialog(ctk.CTkToplevel):
    """Modal dialog for selecting tests and question count for a mix test."""

    DIALOG_WIDTH = 540
    DIALOG_HEIGHT = 640

    def __init__(
        self,
        parent,
        tests_with_counts: List[Tuple[Test, int]],
    ) -> None:
        super().__init__(parent)
        self.title("Mix Test")
        self.geometry(f"{self.DIALOG_WIDTH}x{self.DIALOG_HEIGHT}")
        self.resizable(False, False)
        self.configure(fg_color=get_color("app_bg"))

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
        x = parent.winfo_rootx() + (parent.winfo_width() - self.DIALOG_WIDTH) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.DIALOG_HEIGHT) // 2
        self.geometry(f"+{x}+{y}")

    def _build_ui(self) -> None:
        """Build the dialog layout."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=SPACE_16, pady=SPACE_16)

        shell = ctk.CTkFrame(container, **get_card_style("default"))
        shell.pack(fill="both", expand=True)

        ctk.CTkLabel(
            shell,
            text="Build a Mixed Test",
            **get_text_style("section_title"),
        ).pack(pady=(SPACE_16, SPACE_4))

        ctk.CTkLabel(
            shell,
            text="Choose source tests, then set how many questions to include.",
            wraplength=430,
            justify="center",
            **get_text_style("card_description"),
        ).pack(padx=SPACE_24, pady=(0, SPACE_12))

        utility_frame = ctk.CTkFrame(shell, fg_color="transparent")
        utility_frame.pack(fill="x", padx=SPACE_24, pady=(0, SPACE_8))

        ctk.CTkButton(
            utility_frame,
            text="Select All",
            width=90,
            height=28,
            command=self._select_all,
            **get_button_style("tertiary"),
        ).pack(side="left", padx=(0, SPACE_8))

        ctk.CTkButton(
            utility_frame,
            text="Deselect All",
            width=90,
            height=28,
            command=self._deselect_all,
            **get_button_style("tertiary"),
        ).pack(side="left")

        scroll = ctk.CTkScrollableFrame(
            shell,
            height=250,
            fg_color=get_color("surface_subtle"),
            corner_radius=RADIUS_CARD,
            scrollbar_button_color=get_color("surface_muted"),
            scrollbar_button_hover_color=get_color("border"),
        )
        scroll.pack(fill="both", expand=True, padx=SPACE_24, pady=(0, SPACE_12))

        grouped = group_tests_by_name(self._tests_with_counts)
        test_index = 0

        for group_name, group_tests in grouped:
            test_index = self._add_group_section(
                scroll,
                group_name,
                group_tests,
                test_index,
            )

        setup_frame = ctk.CTkFrame(shell, fg_color="transparent")
        setup_frame.pack(fill="x", padx=SPACE_24, pady=(0, SPACE_12))
        setup_frame.grid_columnconfigure(0, weight=1)
        setup_frame.grid_columnconfigure(1, weight=0)

        total_card = ctk.CTkFrame(
            setup_frame,
            fg_color=get_color("surface_subtle"),
            corner_radius=RADIUS_CARD,
        )
        total_card.grid(row=0, column=0, sticky="ew", padx=(0, SPACE_12))

        ctk.CTkLabel(
            total_card,
            text="Selected pool",
            anchor="w",
            **get_text_style("card_metadata"),
        ).pack(fill="x", padx=SPACE_12, pady=(SPACE_8, 0))

        self._total_label = ctk.CTkLabel(
            total_card,
            text="Total available: 0",
            anchor="w",
            **get_text_style("body_bold"),
        )
        self._total_label.pack(fill="x", padx=SPACE_12, pady=(0, SPACE_8))

        count_card = ctk.CTkFrame(
            setup_frame,
            fg_color=get_color("surface_subtle"),
            corner_radius=RADIUS_CARD,
        )
        count_card.grid(row=0, column=1, sticky="e")

        ctk.CTkLabel(
            count_card,
            text="Questions",
            anchor="w",
            **get_text_style("card_metadata"),
        ).pack(fill="x", padx=SPACE_12, pady=(SPACE_8, 0))

        self._count_entry = ctk.CTkEntry(
            count_card,
            width=96,
            height=34,
            justify="center",
            fg_color=get_color("surface"),
            border_color=get_color("border"),
            text_color=get_color("text_primary"),
        )
        self._count_entry.insert(0, "10")
        self._count_entry.pack(padx=SPACE_12, pady=(0, SPACE_8))

        btn_frame = ctk.CTkFrame(shell, fg_color="transparent")
        btn_frame.pack(fill="x", padx=SPACE_24, pady=(0, SPACE_16))
        btn_frame.grid_columnconfigure((0, 1), weight=1, uniform="mix_actions")

        ctk.CTkButton(
            btn_frame,
            text="Start Mix Test",
            height=36,
            command=self._on_ok,
            **get_button_style("primary"),
        ).grid(row=0, column=0, sticky="ew", padx=(0, SPACE_8))

        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            height=36,
            command=self.destroy,
            **get_button_style("secondary"),
        ).grid(row=0, column=1, sticky="ew", padx=(SPACE_8, 0))

    def _add_group_section(
        self,
        parent,
        group_name: str,
        group_tests: List[Tuple[Test, int]],
        test_index: int,
    ) -> int:
        """Add a grouped checkbox section and return the next test index."""
        group_var = ctk.BooleanVar(value=False)
        self._group_vars[group_name] = group_var
        self._group_to_test_indices[group_name] = []

        group_card = ctk.CTkFrame(parent, **get_card_style("default"))
        group_card.pack(fill="x", padx=SPACE_4, pady=(SPACE_4, SPACE_8))

        group_header = ctk.CTkFrame(group_card, fg_color="transparent")
        group_header.pack(fill="x", padx=SPACE_12, pady=(SPACE_12, SPACE_8))

        group_cb = ctk.CTkCheckBox(
            group_header,
            text=group_name,
            variable=group_var,
            command=lambda gn=group_name: self._on_group_toggled(gn),
            **self._checkbox_style("body_bold"),
        )
        group_cb.pack(side="left", fill="x", expand=True)

        group_total = sum(q_count for _, q_count in group_tests)
        ctk.CTkLabel(
            group_header,
            text=f"{len(group_tests)} test(s) / {group_total} questions",
            anchor="e",
            **get_text_style("card_metadata"),
        ).pack(side="right", padx=(SPACE_8, 0))

        for test, q_count in group_tests:
            test_index = self._add_test_row(
                group_card,
                group_name,
                test,
                q_count,
                test_index,
            )

        return test_index

    def _add_test_row(
        self,
        parent,
        group_name: str,
        test: Test,
        q_count: int,
        test_index: int,
    ) -> int:
        """Add one test checkbox row and return the next test index."""
        var = ctk.BooleanVar(value=False)
        self._check_vars.append(var)

        row = ctk.CTkFrame(
            parent,
            fg_color=get_color("surface_subtle"),
            corner_radius=RADIUS_ROW,
        )
        row.pack(fill="x", padx=SPACE_12, pady=(0, SPACE_8))

        cb = ctk.CTkCheckBox(
            row,
            text=f"{test.name}  ({q_count} questions)",
            variable=var,
            command=lambda gn=group_name: self._on_test_checkbox_changed(gn),
            **self._checkbox_style("body"),
        )
        cb.pack(anchor="w", fill="x", padx=SPACE_12, pady=SPACE_8)

        self._checkboxes.append((cb, test.id))
        self._group_to_test_indices[group_name].append(test_index)
        return test_index + 1

    @staticmethod
    def _checkbox_style(text_role: str) -> dict:
        """Return shared checkbox styling for grouped test selection."""
        style = get_text_style(text_role)
        style.update(
            {
                "fg_color": get_color("primary"),
                "hover_color": get_color("primary_hover"),
                "border_color": get_color("border"),
                "checkmark_color": get_color("text_inverse"),
            }
        )
        return style

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
