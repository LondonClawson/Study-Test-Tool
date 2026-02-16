"""Test editor screen — create and edit tests with questions."""

import tkinter.messagebox as messagebox

import customtkinter as ctk

from config.settings import (
    COLOR_DANGER,
    COLOR_SUCCESS,
    FONT_FAMILY,
    FONT_SIZE_BODY,
    FONT_SIZE_HEADING,
    FONT_SIZE_SMALL,
    FONT_SIZE_TITLE,
    QUESTION_TYPE_ESSAY,
    QUESTION_TYPE_MC,
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
        # Top bar: Back + Title
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkButton(
            top_frame,
            text="< Back",
            width=80,
            fg_color="gray",
            command=self._on_back,
        ).pack(side="left")

        self.title_label = ctk.CTkLabel(
            top_frame,
            text="New Test",
            font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
        )
        self.title_label.pack(side="left", padx=20)

        # Test metadata
        meta_frame = ctk.CTkFrame(self, fg_color="transparent")
        meta_frame.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(
            meta_frame,
            text="Test Name:",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
        ).grid(row=0, column=0, sticky="w", pady=3)

        self.name_entry = ctk.CTkEntry(meta_frame, width=400)
        self.name_entry.grid(row=0, column=1, sticky="w", padx=10, pady=3)

        ctk.CTkLabel(
            meta_frame,
            text="Description:",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
        ).grid(row=1, column=0, sticky="w", pady=3)

        self.desc_entry = ctk.CTkEntry(meta_frame, width=400)
        self.desc_entry.grid(row=1, column=1, sticky="w", padx=10, pady=3)

        ctk.CTkButton(
            meta_frame,
            text="Save Test",
            width=100,
            fg_color=COLOR_SUCCESS,
            command=self._on_save_test,
        ).grid(row=0, column=2, rowspan=2, padx=20, pady=3)

        # Divider
        ctk.CTkFrame(self, height=2, fg_color="gray").pack(
            fill="x", padx=30, pady=5
        )

        # Main content: left = question list, right = question form
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=5)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # Left: existing questions
        left_frame = ctk.CTkFrame(content_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(
            left_frame,
            text="Questions",
            font=(FONT_FAMILY, FONT_SIZE_HEADING, "bold"),
        ).pack(pady=5)

        self.question_list = ctk.CTkScrollableFrame(left_frame)
        self.question_list.pack(fill="both", expand=True, padx=5, pady=5)

        self.no_questions_label = ctk.CTkLabel(
            self.question_list,
            text="No questions yet.",
            text_color="gray",
        )

        # Right: add/edit question form
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.form_title = ctk.CTkLabel(
            right_frame,
            text="Add Question",
            font=(FONT_FAMILY, FONT_SIZE_HEADING, "bold"),
        )
        self.form_title.pack(pady=5)

        form_scroll = ctk.CTkScrollableFrame(right_frame)
        form_scroll.pack(fill="both", expand=True, padx=5, pady=5)

        # Question text
        ctk.CTkLabel(
            form_scroll,
            text="Question Text:",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
        ).pack(anchor="w", pady=(5, 2))

        self.question_text = ctk.CTkTextbox(form_scroll, height=80)
        self.question_text.pack(fill="x", pady=(0, 5))

        # Type selector
        ctk.CTkLabel(
            form_scroll,
            text="Type:",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
        ).pack(anchor="w", pady=(5, 2))

        self.type_var = ctk.StringVar(value=QUESTION_TYPE_MC)
        self.type_selector = ctk.CTkSegmentedButton(
            form_scroll,
            values=["Multiple Choice", "Essay"],
            command=self._on_type_change,
        )
        self.type_selector.set("Multiple Choice")
        self.type_selector.pack(fill="x", pady=(0, 5))

        # Category
        ctk.CTkLabel(
            form_scroll,
            text="Category (optional):",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
        ).pack(anchor="w", pady=(5, 2))

        self.category_entry = ctk.CTkEntry(form_scroll, width=300)
        self.category_entry.pack(anchor="w", pady=(0, 10))

        # MC Options frame
        self.options_frame = ctk.CTkFrame(form_scroll, fg_color="transparent")
        self.options_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            self.options_frame,
            text="Options (select the correct one):",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
        ).pack(anchor="w")

        self.correct_var = ctk.IntVar(value=0)
        self.option_entries = []
        for i in range(4):
            row = ctk.CTkFrame(self.options_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)

            rb = ctk.CTkRadioButton(
                row,
                text="",
                variable=self.correct_var,
                value=i,
                width=20,
            )
            rb.pack(side="left", padx=(0, 5))

            entry = ctk.CTkEntry(row, placeholder_text=f"Option {chr(65 + i)}")
            entry.pack(side="left", fill="x", expand=True)

            self.option_entries.append(entry)

        # Essay answer frame
        self.essay_frame = ctk.CTkFrame(form_scroll, fg_color="transparent")

        ctk.CTkLabel(
            self.essay_frame,
            text="Expected Answer:",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
        ).pack(anchor="w")

        self.essay_answer = ctk.CTkTextbox(self.essay_frame, height=80)
        self.essay_answer.pack(fill="x", pady=(2, 5))

        # Add/Update button
        self.add_btn = ctk.CTkButton(
            form_scroll,
            text="Add Question",
            command=self._on_add_question,
        )
        self.add_btn.pack(pady=10)

        self.cancel_edit_btn = ctk.CTkButton(
            form_scroll,
            text="Cancel Edit",
            fg_color="gray",
            command=self._cancel_edit,
        )

    def on_show(self, test_id=None, **kwargs) -> None:
        """Initialize the editor for creating or editing a test."""
        self._test_id = test_id
        self._editing_question_id = None
        self._reset_form()

        if test_id is not None:
            test = self.test_service.get_test_by_id(test_id)
            if test:
                self.title_label.configure(text="Edit Test")
                self.name_entry.delete(0, "end")
                self.name_entry.insert(0, test.name)
                self.desc_entry.delete(0, "end")
                self.desc_entry.insert(0, test.description or "")
        else:
            self.title_label.configure(text="New Test")
            self.name_entry.delete(0, "end")
            self.desc_entry.delete(0, "end")

        self._refresh_question_list()

    def _refresh_question_list(self) -> None:
        """Reload and display questions for the current test."""
        for widget in self.question_list.winfo_children():
            if widget != self.no_questions_label:
                widget.destroy()

        if self._test_id is None:
            self.no_questions_label.pack(pady=20)
            return

        questions = self.question_service.get_questions_for_test(self._test_id)

        if not questions:
            self.no_questions_label.pack(pady=20)
            return

        self.no_questions_label.pack_forget()

        for i, question in enumerate(questions, 1):
            self._create_question_card(i, question)

    def _create_question_card(self, num: int, question: Question) -> None:
        """Create a card for a question in the list."""
        card = ctk.CTkFrame(self.question_list, corner_radius=6)
        card.pack(fill="x", pady=3)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        # Truncate long text
        text = question.text
        if len(text) > 80:
            text = text[:77] + "..."

        ctk.CTkLabel(
            info,
            text=f"Q{num}. {text}",
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            anchor="w",
            wraplength=300,
        ).pack(fill="x")

        type_label = "MC" if question.type == QUESTION_TYPE_MC else "Essay"
        ctk.CTkLabel(
            info,
            text=f"Type: {type_label}",
            font=(FONT_FAMILY, 11),
            text_color="gray",
            anchor="w",
        ).pack(fill="x")

        if not question.correct_answer:
            ctk.CTkLabel(
                info,
                text="\u26a0 No answer set",
                font=(FONT_FAMILY, 11),
                text_color="#f0ad4e",
                anchor="w",
            ).pack(fill="x")

        btns = ctk.CTkFrame(card, fg_color="transparent")
        btns.pack(side="right", padx=5, pady=5)

        ctk.CTkButton(
            btns,
            text="Edit",
            width=50,
            height=26,
            fg_color="gray",
            command=lambda q=question: self._on_edit_question(q),
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            btns,
            text="Del",
            width=50,
            height=26,
            fg_color=COLOR_DANGER,
            hover_color="#c9302c",
            command=lambda q=question: self._on_delete_question(q),
        ).pack(side="left", padx=2)

    def _on_type_change(self, value: str) -> None:
        """Toggle between MC options and essay answer field."""
        if value == "Multiple Choice":
            self.type_var.set(QUESTION_TYPE_MC)
            self.essay_frame.pack_forget()
            self.options_frame.pack(fill="x", pady=5)
        else:
            self.type_var.set(QUESTION_TYPE_ESSAY)
            self.options_frame.pack_forget()
            self.essay_frame.pack(fill="x", pady=5)

    def _on_save_test(self) -> None:
        """Save or create the test metadata."""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Validation", "Test name is required.")
            return

        description = self.desc_entry.get().strip()

        if self._test_id is None:
            self._test_id = self.test_service.create_test(name, description)
            self.title_label.configure(text="Edit Test")
            messagebox.showinfo("Success", "Test created! Now add questions.")
        else:
            test = Test(id=self._test_id, name=name, description=description)
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

        if q_type == QUESTION_TYPE_MC:
            options = []
            correct_idx = self.correct_var.get()
            correct_answer = ""

            for i, entry in enumerate(self.option_entries):
                opt_text = entry.get().strip()
                if opt_text:
                    is_correct = i == correct_idx
                    options.append(
                        QuestionOption(text=opt_text, is_correct=is_correct)
                    )
                    if is_correct:
                        correct_answer = opt_text

            non_empty = [o for o in options if o.text]
            if len(non_empty) < 2:
                messagebox.showwarning(
                    "Validation", "At least 2 options are required."
                )
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
        return (question_text, q_type, correct_idx, tuple(option_texts),
                essay_text, category)

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
        self.add_btn.configure(text="Update Question")
        self.cancel_edit_btn.pack(pady=5)

        # Fill in text
        self.question_text.delete("1.0", "end")
        self.question_text.insert("1.0", question.text)

        # Set type
        if question.type == QUESTION_TYPE_MC:
            self.type_selector.set("Multiple Choice")
            self._on_type_change("Multiple Choice")

            for i, entry in enumerate(self.option_entries):
                entry.delete(0, "end")

            for i, opt in enumerate(question.options):
                if i < len(self.option_entries):
                    self.option_entries[i].insert(0, opt.text)
                    if opt.is_correct:
                        self.correct_var.set(i)
        else:
            self.type_selector.set("Essay")
            self._on_type_change("Essay")
            self.essay_answer.delete("1.0", "end")
            self.essay_answer.insert("1.0", question.correct_answer)

        self.category_entry.delete(0, "end")
        self.category_entry.insert(0, question.category or "")

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
        self.add_btn.configure(text="Add Question")
        self.cancel_edit_btn.pack_forget()

        self.question_text.delete("1.0", "end")
        self.type_selector.set("Multiple Choice")
        self._on_type_change("Multiple Choice")
        self.correct_var.set(0)
        for entry in self.option_entries:
            entry.delete(0, "end")
        self.essay_answer.delete("1.0", "end")
        self.category_entry.delete(0, "end")
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
