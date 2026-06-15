"""Review view — browse and review missed questions."""

from typing import Dict, List, Optional, Set

import customtkinter as ctk

from config.settings import (
    COLOR_INCORRECT,
    FONT_FAMILY,
    FONT_SIZE_BODY,
    FONT_SIZE_HEADING,
    FONT_SIZE_SMALL,
    FONT_SIZE_TITLE,
)
from gui.mix_test_display import group_tests_by_name
from services.review_service import ReviewService
from services.test_service import TestService
from utils.constants import MODE_PRACTICE, SCREEN_HOME, SCREEN_TEST_TAKING


class ReviewViewFrame(ctk.CTkFrame):
    """Screen for browsing and reviewing missed questions."""

    def __init__(self, parent: ctk.CTkFrame, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.review_service = ReviewService()
        self.test_service = TestService()

        self._missed_data = []
        self._checkboxes = {}  # question_id -> BooleanVar
        self._scope_tests = []
        self._test_scope_vars: Dict[int, ctk.BooleanVar] = {}
        self._group_scope_vars: Dict[str, ctk.BooleanVar] = {}
        self._group_to_test_ids: Dict[str, List[int]] = {}

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the review layout."""
        # Top bar
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(20, 10))

        ctk.CTkButton(
            top_frame,
            text="< Back",
            width=80,
            fg_color="gray",
            command=lambda: self.controller.show_frame(SCREEN_HOME),
        ).pack(side="left")

        ctk.CTkLabel(
            top_frame,
            text="Missed Questions",
            font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
        ).pack(side="left", padx=20)

        # Filter row
        filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        filter_frame.pack(fill="x", padx=30, pady=(0, 10))

        ctk.CTkLabel(
            filter_frame,
            text="Scope:",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
        ).pack(side="left", padx=(0, 10))

        self.scope_summary_label = ctk.CTkLabel(
            filter_frame,
            text="All Active Tests",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
            text_color="gray",
        )
        self.scope_summary_label.pack(side="left")

        self.filter_type_var = ctk.StringVar(value="All Missed")
        self.filter_type_seg = ctk.CTkSegmentedButton(
            filter_frame,
            values=["All Missed", "Frequently Missed"],
            variable=self.filter_type_var,
            command=self._on_filter_change,
        )
        self.filter_type_seg.pack(side="left", padx=20)

        # Scope selector
        scope_frame = ctk.CTkFrame(self)
        scope_frame.pack(fill="x", padx=30, pady=(0, 10))

        scope_actions = ctk.CTkFrame(scope_frame, fg_color="transparent")
        scope_actions.pack(fill="x", padx=10, pady=(8, 2))

        ctk.CTkButton(
            scope_actions,
            text="Select All",
            width=90,
            height=28,
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            command=self._select_all_scope,
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            scope_actions,
            text="Deselect All",
            width=100,
            height=28,
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            fg_color="gray",
            command=self._deselect_all_scope,
        ).pack(side="left")

        self.scope_list = ctk.CTkScrollableFrame(scope_frame, height=130)
        self.scope_list.pack(fill="x", padx=10, pady=(0, 10))

        # Action bar
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.pack(fill="x", padx=30, pady=(0, 5))

        self.select_all_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            action_frame,
            text="Select All",
            variable=self.select_all_var,
            command=self._on_select_all,
        ).pack(side="left")

        self.start_review_btn = ctk.CTkButton(
            action_frame,
            text="Start Review",
            width=120,
            fg_color="#2fa572",
            hover_color="#258a5e",
            command=self._on_start_review,
        )
        self.start_review_btn.pack(side="right")

        self.selected_label = ctk.CTkLabel(
            action_frame,
            text="0 selected",
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            text_color="gray",
        )
        self.selected_label.pack(side="right", padx=10)

        # Scrollable question list
        self.question_list = ctk.CTkScrollableFrame(self)
        self.question_list.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        # Empty state
        self.empty_label = ctk.CTkLabel(
            self.question_list,
            text="No missed questions found.",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
            text_color="gray",
        )

    def on_show(self, **kwargs) -> None:
        """Load missed questions when shown."""
        self._refresh_scope_options()
        self.filter_type_var.set("All Missed")

        self._load_questions()

    def _on_filter_change(self, value: str) -> None:
        """Reload questions when filter changes."""
        self._load_questions()

    def _refresh_scope_options(self) -> None:
        """Load active tests into the grouped scope selector."""
        for widget in self.scope_list.winfo_children():
            widget.destroy()

        self._scope_tests = []
        self._test_scope_vars.clear()
        self._group_scope_vars.clear()
        self._group_to_test_ids.clear()

        for test in self.test_service.get_all_tests():
            q_count = self.test_service.get_question_count(test.id)
            if q_count > 0:
                self._scope_tests.append((test, q_count))

        if not self._scope_tests:
            ctk.CTkLabel(
                self.scope_list,
                text="No active tests available.",
                font=(FONT_FAMILY, FONT_SIZE_BODY),
                text_color="gray",
            ).pack(anchor="w", pady=8, padx=2)
            self._update_scope_summary()
            return

        for group_name, group_tests in group_tests_by_name(self._scope_tests):
            group_var = ctk.BooleanVar(value=True)
            self._group_scope_vars[group_name] = group_var
            self._group_to_test_ids[group_name] = []

            group_cb = ctk.CTkCheckBox(
                self.scope_list,
                text=group_name,
                font=(FONT_FAMILY, FONT_SIZE_BODY, "bold"),
                variable=group_var,
                command=lambda gn=group_name: self._on_scope_group_toggled(gn),
            )
            group_cb.pack(anchor="w", pady=(8, 2), padx=2)

            for test, q_count in group_tests:
                var = ctk.BooleanVar(value=True)
                self._test_scope_vars[test.id] = var
                self._group_to_test_ids[group_name].append(test.id)

                cb = ctk.CTkCheckBox(
                    self.scope_list,
                    text=f"{test.name}  ({q_count} questions)",
                    font=(FONT_FAMILY, FONT_SIZE_BODY),
                    variable=var,
                    command=lambda gn=group_name: self._on_scope_test_changed(
                        gn
                    ),
                )
                cb.pack(anchor="w", pady=2, padx=25)

        self._update_scope_summary()

    def _select_all_scope(self) -> None:
        """Select every active test in the review scope."""
        for var in self._test_scope_vars.values():
            var.set(True)
        for var in self._group_scope_vars.values():
            var.set(True)
        self._load_questions()

    def _deselect_all_scope(self) -> None:
        """Clear every test from the review scope."""
        for var in self._test_scope_vars.values():
            var.set(False)
        for var in self._group_scope_vars.values():
            var.set(False)
        self._load_questions()

    def _on_scope_group_toggled(self, group_name: str) -> None:
        """Toggle all tests in a group when the group checkbox changes."""
        is_selected = self._group_scope_vars[group_name].get()
        for test_id in self._group_to_test_ids[group_name]:
            self._test_scope_vars[test_id].set(is_selected)
        self._load_questions()

    def _on_scope_test_changed(self, group_name: str) -> None:
        """Sync a group checkbox after an individual test changes."""
        group_ids = self._group_to_test_ids[group_name]
        all_selected = all(
            self._test_scope_vars[test_id].get() for test_id in group_ids
        )
        self._group_scope_vars[group_name].set(all_selected)
        self._load_questions()

    def _get_selected_test_ids(self) -> Optional[List[int]]:
        """Return selected test ids, or None when all active tests are selected."""
        if not self._test_scope_vars:
            return []

        selected_ids = [
            test_id
            for test_id, var in self._test_scope_vars.items()
            if var.get()
        ]
        if len(selected_ids) == len(self._test_scope_vars):
            return None
        return selected_ids

    def _update_scope_summary(self) -> None:
        """Update the label that summarizes the selected review scope."""
        if not self._test_scope_vars:
            self.scope_summary_label.configure(text="No active tests")
            return

        selected: Set[int] = {
            test_id
            for test_id, var in self._test_scope_vars.items()
            if var.get()
        }
        if not selected:
            self.scope_summary_label.configure(text="No tests selected")
            return

        if len(selected) == len(self._test_scope_vars):
            self.scope_summary_label.configure(text="All Active Tests")
            return

        for group_name, test_ids in self._group_to_test_ids.items():
            group_set = set(test_ids)
            if selected == group_set:
                self.scope_summary_label.configure(text=f"Group: {group_name}")
                return

        if len(selected) == 1:
            test_id = next(iter(selected))
            for test, _ in self._scope_tests:
                if test.id == test_id:
                    self.scope_summary_label.configure(text=test.name)
                    return

        self.scope_summary_label.configure(text=f"{len(selected)} tests selected")

    def _load_questions(self) -> None:
        """Load missed questions based on current filters."""
        self._update_scope_summary()
        test_ids = self._get_selected_test_ids()

        filter_type = self.filter_type_var.get()
        if filter_type == "Frequently Missed":
            self._missed_data = self.review_service.get_frequently_missed(
                test_ids=test_ids
            )
        else:
            self._missed_data = self.review_service.get_missed_questions(
                test_ids=test_ids
            )

        self._display_questions()

    def _display_questions(self) -> None:
        """Render the missed question cards."""
        # Clear existing
        for widget in self.question_list.winfo_children():
            if widget != self.empty_label:
                widget.destroy()

        self._checkboxes.clear()
        self.select_all_var.set(False)

        if not self._missed_data:
            self.empty_label.pack(pady=40)
            self._update_selected_count()
            return

        self.empty_label.pack_forget()

        for item in self._missed_data:
            self._create_question_card(item)

        self._update_selected_count()

    def _create_question_card(self, item: dict) -> None:
        """Create a card for a missed question."""
        card = ctk.CTkFrame(self.question_list, corner_radius=8)
        card.pack(fill="x", pady=4, padx=5)

        # Top row: checkbox + question text
        top_row = ctk.CTkFrame(card, fg_color="transparent")
        top_row.pack(fill="x", padx=10, pady=(8, 2))

        var = ctk.BooleanVar(value=False)
        self._checkboxes[item["question_id"]] = var

        ctk.CTkCheckBox(
            top_row,
            text="",
            variable=var,
            width=24,
            command=self._update_selected_count,
        ).pack(side="left", padx=(0, 5))

        ctk.CTkLabel(
            top_row,
            text=item["question_text"],
            font=(FONT_FAMILY, FONT_SIZE_BODY),
            wraplength=550,
            justify="left",
            anchor="nw",
        ).pack(side="left", fill="x", expand=True)

        # Bottom row: metadata
        meta_row = ctk.CTkFrame(card, fg_color="transparent")
        meta_row.pack(fill="x", padx=10, pady=(2, 8))

        # Spacer to align with checkbox
        ctk.CTkFrame(meta_row, fg_color="transparent", width=29).pack(
            side="left"
        )

        ctk.CTkLabel(
            meta_row,
            text=item.get("test_name", ""),
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            text_color="gray",
        ).pack(side="left", padx=(0, 15))

        if item.get("category"):
            ctk.CTkLabel(
                meta_row,
                text=item["category"],
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                text_color="gray",
            ).pack(side="left", padx=(0, 15))

        miss_rate = (
            item["times_missed"] / item["total_attempts"] * 100
            if item["total_attempts"] > 0
            else 0
        )
        ctk.CTkLabel(
            meta_row,
            text=f"Missed {item['times_missed']}/{item['total_attempts']} ({miss_rate:.0f}%)",
            font=(FONT_FAMILY, FONT_SIZE_SMALL, "bold"),
            text_color=COLOR_INCORRECT,
        ).pack(side="left")

    def _on_select_all(self) -> None:
        """Toggle all checkboxes."""
        val = self.select_all_var.get()
        for var in self._checkboxes.values():
            var.set(val)
        self._update_selected_count()

    def _update_selected_count(self) -> None:
        """Update the selected count label."""
        count = sum(1 for v in self._checkboxes.values() if v.get())
        self.selected_label.configure(text=f"{count} selected")

    def _on_start_review(self) -> None:
        """Start a practice review with the selected questions."""
        selected_ids = [
            qid for qid, var in self._checkboxes.items() if var.get()
        ]
        if not selected_ids:
            # If none selected, use all displayed
            selected_ids = [item["question_id"] for item in self._missed_data]

        if not selected_ids:
            return

        self.controller.show_frame(
            SCREEN_TEST_TAKING,
            mode=MODE_PRACTICE,
            review_question_ids=selected_ids,
        )
