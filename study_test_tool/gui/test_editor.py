"""Test editor screen — create and edit tests with questions."""

import tkinter.messagebox as messagebox

import customtkinter as ctk

from gui.components.autocomplete_entry import AutocompleteEntry
from config.settings import (
    FONT_FAMILY,
    QUESTION_TYPE_ESSAY,
    QUESTION_TYPE_MC,
)
from gui.styles import (
    FONT_CARD_TITLE,
    RADIUS_CARD,
    RADIUS_CONTROL,
    SPACE_4,
    SPACE_8,
    SPACE_12,
    SPACE_16,
    SPACE_24,
    get_button_style,
    get_card_style,
    get_color,
    get_header_style,
    get_text_style,
)
from models.question import Question, QuestionOption
from models.test import Test
from services.question_service import QuestionService
from services.test_service import TestService
from utils.constants import SCREEN_HOME


class TestEditorFrame(ctk.CTkFrame):
    """Screen for creating and editing tests with their questions."""

    def __init__(self, parent: ctk.CTkFrame, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.test_service = TestService()
        self.question_service = QuestionService()

        self._test_id = None
        self._editing_question_id = None
        self._clean_snapshot = None

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the editor layout."""
        self.configure(fg_color=get_color("app_bg"))

        # Page header and metadata
        header_frame = ctk.CTkFrame(self, **get_header_style("page"))
        header_frame.pack(fill="x", padx=SPACE_24, pady=(SPACE_24, SPACE_12))
        header_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            header_frame,
            text="< Back",
            width=86,
            command=self._on_back,
            **get_button_style("secondary"),
        ).grid(row=0, column=0, padx=SPACE_16, pady=(SPACE_16, SPACE_8), sticky="w")

        self.title_label = ctk.CTkLabel(
            header_frame,
            text="New Test",
            anchor="w",
            **get_text_style("page_title"),
        )
        self.title_label.grid(
            row=0,
            column=1,
            padx=(0, SPACE_16),
            pady=(SPACE_16, SPACE_8),
            sticky="ew",
        )

        self.save_test_btn = ctk.CTkButton(
            header_frame,
            text="Save Test",
            width=120,
            command=self._on_save_test,
            **get_button_style("primary"),
        )
        self.save_test_btn.grid(
            row=0,
            column=2,
            padx=(0, SPACE_16),
            pady=(SPACE_16, SPACE_8),
            sticky="e",
        )

        meta_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        meta_frame.grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=SPACE_16,
            pady=(0, SPACE_16),
        )
        meta_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            meta_frame,
            text="Test Name",
            anchor="w",
            **get_text_style("metadata"),
        ).grid(row=0, column=0, sticky="w", pady=(0, SPACE_4))

        self.name_entry = ctk.CTkEntry(
            meta_frame,
            border_color=get_color("border"),
            fg_color=get_color("surface_subtle"),
        )
        self.name_entry.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(SPACE_12, 0),
            pady=(0, SPACE_4),
        )

        ctk.CTkLabel(
            meta_frame,
            text="Description",
            anchor="w",
            **get_text_style("metadata"),
        ).grid(row=1, column=0, sticky="w", pady=(0, SPACE_4))

        self.desc_entry = ctk.CTkEntry(
            meta_frame,
            border_color=get_color("border"),
            fg_color=get_color("surface_subtle"),
        )
        self.desc_entry.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(SPACE_12, 0),
            pady=(0, SPACE_4),
        )

        ctk.CTkLabel(
            meta_frame,
            text="Group (optional)",
            anchor="w",
            **get_text_style("metadata"),
        ).grid(row=2, column=0, sticky="w")

        self.group_entry = AutocompleteEntry(
            meta_frame,
            placeholder_text="e.g. Week 1, Cert Prep",
        )
        self.group_entry.grid(row=2, column=1, sticky="ew", padx=(SPACE_12, 0))

        # Main content: left = question list, right = question form
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=SPACE_24, pady=(0, SPACE_24))
        content_frame.grid_columnconfigure(0, weight=1, uniform="editor_columns")
        content_frame.grid_columnconfigure(1, weight=1, uniform="editor_columns")
        content_frame.grid_rowconfigure(0, weight=1)

        # Left: existing questions
        left_frame = ctk.CTkFrame(content_frame, **get_card_style("default"))
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, SPACE_8))
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        left_header = ctk.CTkFrame(left_frame, fg_color="transparent")
        left_header.grid(row=0, column=0, sticky="ew", padx=SPACE_16, pady=SPACE_16)
        left_header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            left_header,
            text="Questions",
            anchor="w",
            **get_text_style("section_title"),
        ).grid(row=0, column=0, sticky="ew")

        self.question_count_label = ctk.CTkLabel(
            left_header,
            text="",
            anchor="e",
            **get_text_style("metadata"),
        )
        self.question_count_label.grid(row=0, column=1, sticky="e")

        self.question_list = ctk.CTkScrollableFrame(
            left_frame,
            fg_color=get_color("surface_subtle"),
            border_color=get_color("divider"),
            border_width=1,
            corner_radius=RADIUS_CONTROL,
            scrollbar_button_color=get_color("secondary"),
            scrollbar_button_hover_color=get_color("secondary_hover"),
        )
        self.question_list.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=SPACE_16,
            pady=(0, SPACE_16),
        )

        self.no_questions_label = ctk.CTkLabel(
            self.question_list,
            text="No questions yet.",
            **get_text_style("metadata"),
        )

        # Right: add/edit question form
        right_frame = ctk.CTkFrame(content_frame, **get_card_style("default"))
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(SPACE_8, 0))
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        form_header = ctk.CTkFrame(right_frame, fg_color="transparent")
        form_header.grid(row=0, column=0, sticky="ew", padx=SPACE_16, pady=SPACE_16)
        form_header.grid_columnconfigure(0, weight=1)

        self.form_title = ctk.CTkLabel(
            form_header,
            text="Add Question",
            anchor="w",
            **get_text_style("section_title"),
        )
        self.form_title.grid(row=0, column=0, sticky="ew")

        self.form_mode_badge = ctk.CTkLabel(
            form_header,
            text="New",
            fg_color=get_color("surface_subtle"),
            corner_radius=RADIUS_CONTROL,
            **get_text_style("metadata"),
        )
        self.form_mode_badge.grid(row=0, column=1, sticky="e", ipadx=SPACE_8)

        self.form_scroll = ctk.CTkScrollableFrame(
            right_frame,
            fg_color=get_color("surface_subtle"),
            border_color=get_color("divider"),
            border_width=1,
            corner_radius=RADIUS_CONTROL,
            scrollbar_button_color=get_color("secondary"),
            scrollbar_button_hover_color=get_color("secondary_hover"),
        )
        self.form_scroll.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=SPACE_16,
            pady=(0, SPACE_16),
        )

        prompt_section = self._create_form_section(self.form_scroll, "Prompt")
        self._add_field_label(prompt_section, "Question Text")

        self.question_text = ctk.CTkTextbox(
            prompt_section,
            height=92,
            border_color=get_color("border"),
            border_width=1,
            fg_color=get_color("surface"),
        )
        self.question_text.pack(fill="x", pady=(0, SPACE_8))

        details_section = self._create_form_section(
            self.form_scroll, "Question Details"
        )
        self._add_field_label(details_section, "Type")

        self.type_var = ctk.StringVar(value=QUESTION_TYPE_MC)
        self.type_selector = ctk.CTkSegmentedButton(
            details_section,
            values=["Multiple Choice", "Essay"],
            command=self._on_type_change,
            selected_color=get_color("surface_muted"),
            selected_hover_color=get_color("divider"),
            unselected_color=get_color("surface"),
            unselected_hover_color=get_color("surface_muted"),
            fg_color=get_color("border"),
            text_color=get_color("text_primary"),
        )
        self.type_selector.set("Multiple Choice")
        self.type_selector.pack(fill="x", pady=(0, SPACE_8))

        self._add_field_label(details_section, "Category (optional)")

        self.category_entry = ctk.CTkEntry(
            details_section,
            border_color=get_color("border"),
            fg_color=get_color("surface"),
        )
        self.category_entry.pack(fill="x", pady=(0, SPACE_4))

        answer_section = self._create_form_section(self.form_scroll, "Answer Data")

        # MC Options frame
        self.options_frame = ctk.CTkFrame(answer_section, fg_color="transparent")
        self.options_frame.pack(fill="x")

        self._add_field_label(self.options_frame, "Options (select the correct one)")

        self.correct_var = ctk.IntVar(value=0)
        self.option_entries: list = []
        self._option_rows: list = []
        self._option_radios: list = []
        self._option_remove_btns: list = []

        self.options_container = ctk.CTkFrame(
            self.options_frame, fg_color="transparent"
        )
        self.options_container.pack(fill="x", pady=(0, SPACE_4))

        self.add_option_btn = ctk.CTkButton(
            self.options_frame,
            text="+ Add Option",
            width=120,
            height=26,
            command=self._on_add_option,
            **get_button_style("tertiary"),
        )
        self.add_option_btn.pack(anchor="w")

        self._rebuild_option_rows(["", "", "", ""], correct_idx=0)

        # Essay answer frame
        self.essay_frame = ctk.CTkFrame(answer_section, fg_color="transparent")

        self._add_field_label(self.essay_frame, "Expected Answer")

        self.essay_answer = ctk.CTkTextbox(
            self.essay_frame,
            height=92,
            border_color=get_color("border"),
            border_width=1,
            fg_color=get_color("surface"),
        )
        self.essay_answer.pack(fill="x")

        explanation_section = self._create_form_section(self.form_scroll, "Explanation")
        self._add_field_label(explanation_section, "Explanation (optional)")

        self.explanation_text = ctk.CTkTextbox(
            explanation_section,
            height=84,
            border_color=get_color("border"),
            border_width=1,
            fg_color=get_color("surface"),
        )
        self.explanation_text.pack(fill="x")

        # Add/Update actions
        self.action_frame = ctk.CTkFrame(self.form_scroll, fg_color="transparent")
        self.action_frame.pack(fill="x", padx=SPACE_12, pady=(0, SPACE_16))
        self.add_btn = ctk.CTkButton(
            self.action_frame,
            text="Add Question",
            command=self._on_add_question,
            **get_button_style("primary"),
        )
        self.add_btn.pack(side="left")

        self.cancel_edit_btn = ctk.CTkButton(
            self.action_frame,
            text="Cancel Edit",
            command=self._cancel_edit,
            **get_button_style("secondary"),
        )

    def _create_form_section(self, parent, title: str) -> ctk.CTkFrame:
        """Create a compact form section with a local title."""
        section = ctk.CTkFrame(
            parent, fg_color=get_color("surface"), corner_radius=RADIUS_CARD
        )
        section.pack(fill="x", padx=SPACE_12, pady=(SPACE_12, 0))
        ctk.CTkLabel(
            section,
            text=title,
            anchor="w",
            font=FONT_CARD_TITLE,
            text_color=get_color("text_primary"),
        ).pack(fill="x", padx=SPACE_12, pady=(SPACE_12, SPACE_8))
        return section

    def _add_field_label(self, parent, text: str) -> None:
        """Add a metadata-styled label above an input."""
        ctk.CTkLabel(
            parent,
            text=text,
            anchor="w",
            **get_text_style("metadata"),
        ).pack(fill="x", padx=SPACE_12, pady=(0, SPACE_4))

    def on_show(self, test_id=None, **kwargs) -> None:
        """Initialize the editor for creating or editing a test."""
        self._test_id = test_id
        self._editing_question_id = None
        self._reset_form()

        self.group_entry.set_values(self.test_service.get_group_names())

        if test_id is not None:
            test = self.test_service.get_test_by_id(test_id)
            if test:
                self.title_label.configure(text="Edit Test")
                self.name_entry.delete(0, "end")
                self.name_entry.insert(0, test.name)
                self.desc_entry.delete(0, "end")
                self.desc_entry.insert(0, test.description or "")
                self.group_entry.delete(0, "end")
                self.group_entry.insert(0, test.group_name or "")
        else:
            self.title_label.configure(text="New Test")
            self.name_entry.delete(0, "end")
            self.desc_entry.delete(0, "end")
            self.group_entry.delete(0, "end")

        self._refresh_question_list()

    def _refresh_question_list(self) -> None:
        """Reload and display questions for the current test."""
        for widget in self.question_list.winfo_children():
            if widget != self.no_questions_label:
                widget.destroy()

        if self._test_id is None:
            self.question_count_label.configure(text="Not saved")
            self.no_questions_label.pack(pady=SPACE_24)
            return

        questions = self.question_service.get_questions_for_test(self._test_id)
        question_count = len(questions)
        self.question_count_label.configure(
            text=f"{question_count} question{'s' if question_count != 1 else ''}"
        )

        if not questions:
            self.no_questions_label.pack(pady=SPACE_24)
            return

        self.no_questions_label.pack_forget()

        for i, question in enumerate(questions, 1):
            self._create_question_card(i, question)

    def _create_question_card(self, num: int, question: Question) -> None:
        """Create a card for a question in the list."""
        card = ctk.CTkFrame(self.question_list, **get_card_style("default"))
        card.pack(fill="x", pady=(0, SPACE_8))
        card.grid_columnconfigure(1, weight=1)

        q_badge = ctk.CTkLabel(
            card,
            text=f"Q{num}",
            fg_color=get_color("surface_subtle"),
            corner_radius=RADIUS_CONTROL,
            **get_text_style("metadata"),
        )
        q_badge.grid(row=0, column=0, sticky="nw", padx=SPACE_12, pady=SPACE_12)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.grid(row=0, column=1, sticky="nsew", pady=SPACE_12)

        ctk.CTkLabel(
            info,
            text=question.text,
            anchor="w",
            wraplength=165,
            justify="left",
            **get_text_style("body"),
        ).pack(fill="x")

        type_label = "MC" if question.type == QUESTION_TYPE_MC else "Essay"
        metadata_row = ctk.CTkFrame(info, fg_color="transparent")
        metadata_row.pack(fill="x", pady=(SPACE_4, 0))

        self._build_badge(
            metadata_row,
            type_label,
            get_color("status_neutral"),
        ).pack(side="left")

        if question.category:
            ctk.CTkLabel(
                metadata_row,
                text=question.category,
                anchor="w",
                **get_text_style("metadata"),
            ).pack(side="left", padx=(SPACE_8, 0))

        if not question.correct_answer:
            self._build_badge(
                metadata_row,
                "No answer set",
                get_color("status_warning"),
            ).pack(side="left", padx=(SPACE_8, 0))

        btns = ctk.CTkFrame(card, fg_color="transparent")
        btns.grid(row=0, column=2, sticky="ne", padx=SPACE_12, pady=SPACE_12)

        ctk.CTkButton(
            btns,
            text="Edit",
            width=54,
            height=26,
            command=lambda q=question: self._on_edit_question(q),
            **get_button_style("tertiary"),
        ).pack(fill="x", pady=(0, SPACE_4))

        ctk.CTkButton(
            btns,
            text="Del",
            width=54,
            height=26,
            command=lambda q=question: self._on_delete_question(q),
            **get_button_style("danger"),
        ).pack(fill="x")

    def _build_badge(self, parent, text: str, color) -> ctk.CTkLabel:
        """Build a compact badge for question metadata."""
        return ctk.CTkLabel(
            parent,
            text=text,
            fg_color=color,
            corner_radius=RADIUS_CONTROL,
            text_color=get_color("text_inverse"),
            font=(FONT_FAMILY, 11, "bold"),
        )

    def _on_type_change(self, value: str) -> None:
        """Toggle between MC options and essay answer field."""
        if value == "Multiple Choice":
            self.type_var.set(QUESTION_TYPE_MC)
            self.essay_frame.pack_forget()
            self.options_frame.pack(fill="x")
        else:
            self.type_var.set(QUESTION_TYPE_ESSAY)
            self.options_frame.pack_forget()
            self.essay_frame.pack(fill="x")

    def _rebuild_option_rows(self, option_texts: list, correct_idx: int = 0) -> None:
        """Destroy current option rows and build one row per ``option_texts``.

        Keeps the radio-button ``value`` in lockstep with each row's index in
        ``self.option_entries`` so callers can read ``correct_var`` directly.
        """
        for row in self._option_rows:
            row.destroy()
        self.option_entries = []
        self._option_rows = []
        self._option_radios = []
        self._option_remove_btns = []

        for i, text in enumerate(option_texts):
            row = ctk.CTkFrame(
                self.options_container,
                fg_color=get_color("surface_subtle"),
                border_color=get_color("divider"),
                border_width=1,
                corner_radius=RADIUS_CONTROL,
            )
            row.pack(fill="x", pady=(0, SPACE_4))

            rb = ctk.CTkRadioButton(
                row,
                text="",
                variable=self.correct_var,
                value=i,
                width=20,
                fg_color=get_color("primary"),
                hover_color=get_color("primary_hover"),
                border_color=get_color("border"),
            )
            rb.pack(side="left", padx=(SPACE_8, SPACE_4), pady=SPACE_8)

            entry = ctk.CTkEntry(
                row,
                placeholder_text=f"Option {chr(65 + i)}",
                border_color=get_color("border"),
                fg_color=get_color("surface"),
            )
            entry.pack(side="left", fill="x", expand=True, pady=SPACE_8)
            if text:
                entry.insert(0, text)

            remove_btn = ctk.CTkButton(
                row,
                text="×",
                width=26,
                height=26,
                command=lambda r=row: self._on_remove_option(r),
                **get_button_style("tertiary"),
            )
            remove_btn.pack(side="left", padx=SPACE_8, pady=SPACE_8)

            self.option_entries.append(entry)
            self._option_rows.append(row)
            self._option_radios.append(rb)
            self._option_remove_btns.append(remove_btn)

        # Clamp correct selection to the available range.
        if not self.option_entries:
            self.correct_var.set(0)
        elif correct_idx < 0 or correct_idx >= len(self.option_entries):
            self.correct_var.set(0)
        else:
            self.correct_var.set(correct_idx)

        self._update_remove_button_state()

    def _update_remove_button_state(self) -> None:
        """Disable per-row remove buttons when only 2 options remain."""
        can_remove = len(self.option_entries) > 2
        for btn in self._option_remove_btns:
            btn.configure(
                state="normal" if can_remove else "disabled",
                text_color=(
                    get_color("text_secondary")
                    if can_remove
                    else get_color("text_disabled")
                ),
            )

    def _current_option_texts(self) -> list:
        """Return the current text of every option entry, in row order."""
        return [entry.get() for entry in self.option_entries]

    def _on_add_option(self) -> None:
        """Append an empty option row."""
        texts = self._current_option_texts() + [""]
        self._rebuild_option_rows(texts, correct_idx=self.correct_var.get())

    def _on_remove_option(self, row) -> None:
        """Remove the option row matching ``row`` (the CTkFrame instance)."""
        if len(self.option_entries) <= 2:
            return
        try:
            idx = self._option_rows.index(row)
        except ValueError:
            return
        texts = self._current_option_texts()
        del texts[idx]
        current_correct = self.correct_var.get()
        if current_correct == idx:
            new_correct = 0
        elif current_correct > idx:
            new_correct = current_correct - 1
        else:
            new_correct = current_correct
        self._rebuild_option_rows(texts, correct_idx=new_correct)

    def _on_save_test(self) -> None:
        """Save or create the test metadata."""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Validation", "Test name is required.")
            return

        description = self.desc_entry.get().strip()
        group_name = self.group_entry.get().strip()

        if self._test_id is None:
            self._test_id = self.test_service.create_test(name, description, group_name)
            self.title_label.configure(text="Edit Test")
            messagebox.showinfo("Success", "Test created! Now add questions.")
        else:
            test = Test(
                id=self._test_id,
                name=name,
                description=description,
                group_name=group_name,
            )
            self.test_service.update_test(test)
            messagebox.showinfo("Success", "Test updated.")

    def _on_add_question(self) -> None:
        """Validate and add/update a question."""
        if self._test_id is None:
            messagebox.showwarning(
                "Save First", "Please save the test before adding questions."
            )
            return

        text = self.question_text.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning("Validation", "Question text is required.")
            return

        q_type = self.type_var.get()
        category = self.category_entry.get().strip()
        explanation = self.explanation_text.get("1.0", "end-1c").strip()

        if q_type == QUESTION_TYPE_MC:
            options = []
            correct_idx = self.correct_var.get()
            correct_answer = ""

            for i, entry in enumerate(self.option_entries):
                opt_text = entry.get().strip()
                if opt_text:
                    is_correct = i == correct_idx
                    options.append(QuestionOption(text=opt_text, is_correct=is_correct))
                    if is_correct:
                        correct_answer = opt_text

            non_empty = [o for o in options if o.text]
            if len(non_empty) < 2:
                messagebox.showwarning("Validation", "At least 2 options are required.")
                return

            if not correct_answer:
                messagebox.showwarning(
                    "Validation",
                    "The selected correct option must have text.",
                )
                return

            question = Question(
                test_id=self._test_id,
                text=text,
                type=QUESTION_TYPE_MC,
                correct_answer=correct_answer,
                category=category,
                explanation=explanation,
                options=options,
            )
        else:
            correct_answer = self.essay_answer.get("1.0", "end-1c").strip()
            question = Question(
                test_id=self._test_id,
                text=text,
                type=QUESTION_TYPE_ESSAY,
                correct_answer=correct_answer,
                category=category,
                explanation=explanation,
            )
            if not correct_answer:
                messagebox.showwarning(
                    "No Answer Set",
                    "This essay question has no expected answer set. "
                    "It will be saved, but scoring may not work correctly.",
                )

        if self._editing_question_id is not None:
            question.id = self._editing_question_id
            self.question_service.update_question(question)
            self._editing_question_id = None
            self.add_btn.configure(text="Add Question")
            self.cancel_edit_btn.pack_forget()
        else:
            self.question_service.add_question(question)

        self._reset_form()
        self._refresh_question_list()

    def _get_form_snapshot(self) -> tuple:
        """Return a tuple capturing the current state of all form fields."""
        question_text = self.question_text.get("1.0", "end-1c")
        q_type = self.type_var.get()
        correct_idx = self.correct_var.get()
        option_texts = [entry.get() for entry in self.option_entries]
        essay_text = self.essay_answer.get("1.0", "end-1c")
        category = self.category_entry.get()
        explanation = self.explanation_text.get("1.0", "end-1c")
        return (
            question_text,
            q_type,
            correct_idx,
            tuple(option_texts),
            essay_text,
            category,
            explanation,
        )

    def _form_is_dirty(self) -> bool:
        """Return True if the form has been modified since last clean state."""
        if self._clean_snapshot is None:
            return False
        return self._get_form_snapshot() != self._clean_snapshot

    def _on_edit_question(self, question: Question) -> None:
        """Populate the form with a question's data for editing."""
        if self._form_is_dirty():
            if not messagebox.askyesno(
                "Unsaved Changes",
                "You have unsaved changes. Discard and edit this question?",
            ):
                return
        self._editing_question_id = question.id
        self.form_title.configure(text="Edit Question")
        self.form_mode_badge.configure(
            text="Editing",
            fg_color=get_color("status_warning"),
            text_color=get_color("text_inverse"),
        )
        self.add_btn.configure(text="Update Question")
        self.cancel_edit_btn.pack(side="left", padx=(SPACE_8, 0))

        # Fill in text
        self.question_text.delete("1.0", "end")
        self.question_text.insert("1.0", question.text)

        # Set type
        if question.type == QUESTION_TYPE_MC:
            self.type_selector.set("Multiple Choice")
            self._on_type_change("Multiple Choice")

            opts = list(question.options)
            # Pad to 4 rows so new questions still get the familiar A–D layout.
            texts = [opt.text for opt in opts]
            while len(texts) < 4:
                texts.append("")
            correct_idx = next((i for i, opt in enumerate(opts) if opt.is_correct), 0)
            self._rebuild_option_rows(texts, correct_idx=correct_idx)
        else:
            self.type_selector.set("Essay")
            self._on_type_change("Essay")
            self.essay_answer.delete("1.0", "end")
            self.essay_answer.insert("1.0", question.correct_answer)

        self.category_entry.delete(0, "end")
        self.category_entry.insert(0, question.category or "")
        self.explanation_text.delete("1.0", "end")
        self.explanation_text.insert("1.0", question.explanation or "")

        self._clean_snapshot = self._get_form_snapshot()

    def _on_delete_question(self, question: Question) -> None:
        """Confirm and delete a question."""
        if messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this question?",
        ):
            self.question_service.delete_question(question.id)
            self._refresh_question_list()

    def _cancel_edit(self) -> None:
        """Cancel question editing and reset form."""
        self._editing_question_id = None
        self._reset_form()

    def _reset_form(self) -> None:
        """Clear the question form fields."""
        self.form_title.configure(text="Add Question")
        self.form_mode_badge.configure(
            text="New",
            fg_color=get_color("surface_subtle"),
            text_color=get_color("text_muted"),
        )
        self.add_btn.configure(text="Add Question")
        self.cancel_edit_btn.pack_forget()

        self.question_text.delete("1.0", "end")
        self.type_selector.set("Multiple Choice")
        self._on_type_change("Multiple Choice")
        self._rebuild_option_rows(["", "", "", ""], correct_idx=0)
        self.essay_answer.delete("1.0", "end")
        self.category_entry.delete(0, "end")
        self.explanation_text.delete("1.0", "end")
        self._editing_question_id = None
        self._clean_snapshot = self._get_form_snapshot()

    def _on_back(self) -> None:
        """Navigate back to home screen."""
        if self._form_is_dirty():
            if not messagebox.askyesno(
                "Unsaved Changes",
                "You have unsaved changes to the current question. "
                "Discard changes and go back?",
            ):
                return
        self.controller.show_frame(SCREEN_HOME)
