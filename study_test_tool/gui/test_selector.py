"""Home screen — test selector with import, create, and test list."""

import json
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

import customtkinter as ctk

from config.settings import (
    FONT_FAMILY,
    FONT_SIZE_BODY,
    FONT_SIZE_HEADING,
    FONT_SIZE_SMALL,
    FONT_SIZE_TITLE,
)
from gui.components.collapsible_group import CollapsibleGroup
from gui.components.import_preview_dialog import ImportPreviewDialog
from gui.components.mix_test_dialog import MixTestDialog
from gui.components.mode_dialog import ModeSelectionDialog
from gui.mix_test_display import build_mix_test_display
from gui.styles import get_button_style
from services.export_service import ExportService
from services.import_preview_service import ImportPreview
from services.import_service import ImportService
from services.pdf_import_service import ConversionError, strip_role_suffix
from services.mix_service import MixService
from services.question_service import QuestionService
from services.test_service import TestService
from utils.constants import (
    EXPORT_FILE_TYPES,
    IMPORT_FILE_TYPES,
    SCREEN_ANALYTICS,
    SCREEN_EDITOR,
    SCREEN_HISTORY,
    SCREEN_REVIEW,
    SCREEN_TEST_TAKING,
)


class TestSelectorFrame(ctk.CTkFrame):
    """Home screen displaying available tests with actions."""

    def __init__(self, parent: ctk.CTkFrame, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.test_service = TestService()
        self.question_service = QuestionService()
        self.import_service = ImportService()
        self.export_service = ExportService()
        self.mix_service = MixService()

        self._sort_by = "Last Updated"
        self._group_widgets: dict[str, CollapsibleGroup] = {}

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the home screen layout."""
        # Title
        title = ctk.CTkLabel(
            self,
            text="Study Testing Tool",
            font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
        )
        title.pack(pady=(20, 10))

        # Button bar
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=(0, 15))

        ctk.CTkButton(
            btn_frame,
            text="Import",
            command=self._on_import,
            width=120,
            **get_button_style("secondary"),
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="New Test",
            command=self._on_new_test,
            width=120,
            **get_button_style("primary"),
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Mix Test",
            command=self._on_mix_test,
            width=120,
            **get_button_style("special"),
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Analytics",
            command=self._on_analytics,
            width=120,
            **get_button_style("secondary"),
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="View History",
            command=self._on_view_history,
            width=120,
            **get_button_style("secondary"),
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Review Missed",
            command=self._on_review_missed,
            width=120,
            **get_button_style("warning"),
        ).pack(side="right", padx=5)

        # Sort toolbar
        sort_frame = ctk.CTkFrame(self, fg_color="transparent")
        sort_frame.pack(fill="x", padx=30, pady=(0, 5))

        ctk.CTkLabel(
            sort_frame,
            text="Sort by:",
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
        ).pack(side="left", padx=(0, 5))

        self._sort_menu = ctk.CTkOptionMenu(
            sort_frame,
            values=[
                "Last Updated",
                "Name (A-Z)",
                "Name (Z-A)",
                "Date Created",
            ],
            width=150,
            command=self._on_sort_changed,
        )
        self._sort_menu.set(self._sort_by)
        self._sort_menu.pack(side="left")

        self._collapse_all_btn = ctk.CTkButton(
            sort_frame,
            text="Collapse All",
            width=110,
            command=self._on_collapse_all_toggle,
            **get_button_style("tertiary"),
        )
        self._collapse_all_btn.pack(side="left", padx=(10, 0))

        # Scrollable test list
        self.test_list_frame = ctk.CTkScrollableFrame(self)
        self.test_list_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        # Empty state label (shown when no tests)
        self.empty_label = ctk.CTkLabel(
            self.test_list_frame,
            text="No tests available. Import or create one!",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
            text_color="gray",
        )

    def on_show(self, **kwargs) -> None:
        """Refresh the test list when this screen is shown."""
        self._refresh_test_list()

    def _on_sort_changed(self, value: str) -> None:
        """Handle sort dropdown change."""
        self._sort_by = value
        self._refresh_test_list()

    def _on_collapse_all_toggle(self) -> None:
        """Collapse all groups if any are expanded; otherwise expand all."""
        if not self._group_widgets:
            return
        any_expanded = any(w.is_expanded for w in self._group_widgets.values())
        for w in self._group_widgets.values():
            if any_expanded and w.is_expanded:
                w.toggle()
            elif not any_expanded and not w.is_expanded:
                w.toggle()
        self._collapse_all_btn.configure(
            text="Expand All" if any_expanded else "Collapse All"
        )

    def _sort_tests(self, tests):
        """Sort the test list based on current sort selection (within each group)."""
        if self._sort_by == "Name (A-Z)":
            return sorted(tests, key=lambda t: t.name.lower())
        if self._sort_by == "Name (Z-A)":
            return sorted(tests, key=lambda t: t.name.lower(), reverse=True)
        if self._sort_by == "Date Created":
            return sorted(tests, key=lambda t: t.created_at or "", reverse=True)
        # Default: "Last Updated" — already sorted by DB query
        return tests

    def _refresh_test_list(self) -> None:
        """Reload and display all tests."""
        # Preserve expanded/collapsed state before destroying widgets
        old_group_states = {name: w.is_expanded for name, w in self._group_widgets.items()}

        for widget in self.test_list_frame.winfo_children():
            if widget != self.empty_label:
                widget.destroy()
        self._group_widgets = {}

        tests = self.test_service.get_all_tests()
        archived_tests = self.test_service.get_archived_tests()

        if not tests and not archived_tests:
            self.empty_label.pack(pady=40)
            return

        self.empty_label.pack_forget()

        tests = self._sort_tests(tests)

        # Always render in groups: named groups alphabetically, "Ungrouped" last
        grouped: dict[str, list] = {}
        for test in tests:
            group = test.group_name if test.group_name else "Ungrouped"
            grouped.setdefault(group, []).append(test)

        named_groups = sorted(k for k in grouped if k != "Ungrouped")
        ordered_groups = named_groups + (["Ungrouped"] if "Ungrouped" in grouped else [])

        for group in ordered_groups:
            group_tests = grouped[group]
            was_expanded = old_group_states.get(group, False)
            archive_cb = (
                (lambda g=group: self._on_archive_group(g))
                if group != "Ungrouped"
                else None
            )
            group_widget = CollapsibleGroup(
                self.test_list_frame,
                group_name=group,
                test_count=len(group_tests),
                expanded=was_expanded,
                archive_callback=archive_cb,
            )
            group_widget.pack(fill="x")
            self._group_widgets[group] = group_widget
            for test in group_tests:
                self._create_test_card(test, parent=group_widget.content_frame)

        if archived_tests:
            archived_widget = CollapsibleGroup(
                self.test_list_frame,
                group_name="Archived Tests",
                test_count=len(archived_tests),
                expanded=old_group_states.get("__archived__", False),
            )
            archived_widget.pack(fill="x", pady=(10, 0))
            self._group_widgets["__archived__"] = archived_widget
            for test in archived_tests:
                self._create_archived_test_card(
                    test, parent=archived_widget.content_frame
                )

    def _create_test_card(self, test, parent: ctk.CTkFrame = None) -> None:
        """Create a card widget for a single test."""
        if parent is None:
            parent = self.test_list_frame
        card = ctk.CTkFrame(parent, corner_radius=8)
        card.pack(fill="x", pady=5, padx=5)

        # Info section
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)

        ctk.CTkLabel(
            info_frame,
            text=test.name,
            font=(FONT_FAMILY, FONT_SIZE_HEADING, "bold"),
            anchor="w",
        ).pack(fill="x")

        desc_text = test.description if test.description else "No description"
        ctk.CTkLabel(
            info_frame,
            text=desc_text,
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            text_color="gray",
            anchor="w",
        ).pack(fill="x")

        # Question count and group
        q_count = self.test_service.get_question_count(test.id)
        detail_parts = [f"{q_count} question{'s' if q_count != 1 else ''}"]
        if test.group_name:
            detail_parts.append(test.group_name)
        ctk.CTkLabel(
            info_frame,
            text="  |  ".join(detail_parts),
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            text_color="gray",
            anchor="w",
        ).pack(fill="x")

        # Action buttons
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(side="right", padx=15, pady=10)

        take_btn = ctk.CTkButton(
            btn_frame,
            text="Take Test",
            width=90,
            command=lambda t=test: self._on_take_test(t),
            **get_button_style("primary"),
        )
        take_btn.pack(side="left", padx=3)
        if q_count == 0:
            take_btn.configure(state="disabled")

        ctk.CTkButton(
            btn_frame,
            text="Edit",
            width=70,
            command=lambda t=test: self._on_edit_test(t),
            **get_button_style("tertiary"),
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            btn_frame,
            text="Export",
            width=70,
            command=lambda t=test: self._on_export_test(t),
            **get_button_style("tertiary"),
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            btn_frame,
            text="Archive",
            width=70,
            command=lambda t=test: self._on_archive_test(t),
            **get_button_style("secondary"),
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            btn_frame,
            text="Delete",
            width=70,
            command=lambda t=test: self._on_delete_test(t),
            **get_button_style("danger"),
        ).pack(side="left", padx=3)

    def _create_archived_test_card(
        self, test, parent: ctk.CTkFrame = None
    ) -> None:
        """Create a dimmed card widget for an archived test."""
        if parent is None:
            parent = self.test_list_frame
        card = ctk.CTkFrame(
            parent, corner_radius=8, fg_color=("#d0d0d0", "#2a2a2a")
        )
        card.pack(fill="x", pady=5, padx=5)

        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)

        ctk.CTkLabel(
            info_frame,
            text=test.name,
            font=(FONT_FAMILY, FONT_SIZE_HEADING, "bold"),
            text_color="gray",
            anchor="w",
        ).pack(fill="x")

        desc_text = test.description if test.description else "No description"
        ctk.CTkLabel(
            info_frame,
            text=desc_text,
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            text_color="gray",
            anchor="w",
        ).pack(fill="x")

        q_count = self.test_service.get_question_count(test.id)
        detail_parts = [f"{q_count} question{'s' if q_count != 1 else ''}"]
        if test.group_name:
            detail_parts.append(test.group_name)
        ctk.CTkLabel(
            info_frame,
            text="  |  ".join(detail_parts),
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            text_color="gray",
            anchor="w",
        ).pack(fill="x")

        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(side="right", padx=15, pady=10)

        ctk.CTkButton(
            btn_frame,
            text="Unarchive",
            width=90,
            command=lambda t=test: self._on_unarchive_test(t),
            **get_button_style("secondary"),
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            btn_frame,
            text="Delete",
            width=70,
            command=lambda t=test: self._on_delete_test(t),
            **get_button_style("danger"),
        ).pack(side="left", padx=3)

    def _on_import(self) -> None:
        """Handle Import button click — auto-detects file type."""
        file_path = filedialog.askopenfilename(
            title="Import",
            filetypes=IMPORT_FILE_TYPES,
        )
        if not file_path:
            return

        try:
            if file_path.lower().endswith((".pdf", ".docx")):
                imported = self._import_pdf(file_path)
            elif file_path.endswith(".json"):
                preview = self.import_service.preview_from_json(file_path)
                imported = self._confirm_and_commit_import([preview])
            else:
                preview = self.import_service.preview_from_text(file_path)
                imported = self._confirm_and_commit_import([preview])
            if imported:
                self._refresh_test_list()
        except ConversionError as e:
            messagebox.showerror("PDF Import Error", str(e))
        except (ValueError, FileNotFoundError, json.JSONDecodeError) as e:
            messagebox.showerror("Import Error", str(e))
        except Exception as e:
            messagebox.showerror("Import Error", f"Unexpected error: {e}")

    def _confirm_and_commit_import(
        self,
        previews: list[ImportPreview],
        create_backup: bool = False,
    ) -> list[int]:
        """Show the preview dialog and commit confirmed importable previews."""
        dialog = ImportPreviewDialog(self, previews)
        result = dialog.get_result()
        if not result:
            return []

        confirmed, group_name = result
        if not confirmed:
            return []

        group_override = group_name if group_name else None
        test_ids = self.import_service.commit_previews(
            previews,
            group_name_override=group_override,
            create_backup=create_backup,
        )
        messagebox.showinfo(
            "Success",
            f"Imported {len(test_ids)} test(s) successfully.",
        )
        return test_ids

    def _import_pdf(self, pdf_path: str) -> list[int]:
        """Import a PDF, auto-detecting partner and offering folder batch.

        Resolves the Questions/Answers partner for the picked PDF. If the
        containing folder holds more than one valid pair, prompts the user
        to choose between importing just this pair or batch-importing all
        pairs in the folder. Raises ConversionError on failure.
        """
        from pathlib import Path

        from services import pdf_import_service
        from services.pdf_import_service import find_partner_pdf

        picked = Path(pdf_path)

        # Figure out which half the user picked.
        try:
            _, role = strip_role_suffix(picked.stem)
        except ConversionError as exc:
            raise ConversionError(
                f"{exc} Rename the file so it ends with 'Questions' or 'Answers'."
            ) from exc

        # Try auto-detect; fall back to asking for the partner.
        try:
            partner = find_partner_pdf(picked)
        except ConversionError:
            want = "Answers" if role == "questions" else "Questions"
            partner_path = filedialog.askopenfilename(
                title=f"Select the matching {want} file",
                filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx")],
                initialdir=str(picked.parent),
            )
            if not partner_path:
                return
            partner = Path(partner_path)
            # Sanity check: must be the correct role and same pairing key.
            try:
                _, partner_role = strip_role_suffix(partner.stem)
            except ConversionError as exc:
                raise ConversionError(
                    f"{exc} Rename the file so it ends with 'Questions' or 'Answers'."
                ) from exc
            if partner_role == role:
                raise ConversionError(
                    f"Selected file is also a '{role.capitalize()}' PDF — "
                    f"need a {want} PDF."
                )

        # If the containing folder has more than one valid pair, offer batch.
        try:
            all_pairs = pdf_import_service.discover_pairs(picked.parent)
        except ConversionError:
            all_pairs = []

        if len(all_pairs) > 1:
            # Yes = import all pairs, No = just this one, Cancel = abort.
            choice = messagebox.askyesnocancel(
                "Multiple PDF pairs found",
                f"Found {len(all_pairs)} Questions/Answers PDF pairs in this folder.\n\n"
                "Yes — Import all pairs in the folder\n"
                "No — Import only the selected pair\n"
                "Cancel — Abort",
                default=messagebox.NO,
            )
            if choice is None:
                return []
            if choice:
                previews = self.import_service.preview_from_pdf_folder(
                    str(picked.parent)
                )
                test_ids = self._confirm_and_commit_import(
                    previews,
                    create_backup=True,
                )
                if not test_ids:
                    return []
                results = self._build_pdf_folder_report(previews, test_ids)
                self._show_pdf_folder_report(results)
                return test_ids

        if role == "questions":
            questions_pdf, answers_pdf = picked, partner
        else:
            questions_pdf, answers_pdf = partner, picked

        preview = self.import_service.preview_from_pdf_pair(
            str(questions_pdf), str(answers_pdf)
        )
        return self._confirm_and_commit_import([preview])

    @staticmethod
    def _build_pdf_folder_report(previews, test_ids) -> list[dict]:
        """Build a folder report from previews and committed ids."""
        id_iter = iter(test_ids)
        results = []
        for preview in previews:
            if preview.errors:
                results.append(
                    {
                        "pair": preview.test_name,
                        "status": "skipped",
                        "error": "; ".join(preview.errors),
                    }
                )
            else:
                results.append(
                    {
                        "pair": preview.test_name,
                        "status": "success",
                        "test_id": next(id_iter, None),
                        "question_count": preview.question_count,
                    }
                )
        return results

    def _show_pdf_folder_report(self, results) -> None:
        """Render the success/skip report for a folder PDF batch import."""
        succeeded = [r for r in results if r["status"] == "success"]
        skipped = [r for r in results if r["status"] == "skipped"]

        lines = [f"Processed: {len(results)}",
                 f"Succeeded: {len(succeeded)}",
                 f"Skipped: {len(skipped)}", ""]
        for r in succeeded:
            lines.append(f"[OK] {r['pair']} ({r['question_count']} questions)")
        for r in skipped:
            lines.append(f"[SKIP] {r['pair']} — {r['error']}")

        if skipped:
            messagebox.showwarning("PDF Import Report", "\n".join(lines))
        else:
            messagebox.showinfo("PDF Import Report", "\n".join(lines))

    def _on_new_test(self) -> None:
        """Navigate to editor for a new test."""
        self.controller.show_frame(SCREEN_EDITOR, test_id=None)

    def _on_view_history(self) -> None:
        """Navigate to history view."""
        self.controller.show_frame(SCREEN_HISTORY)

    def _on_review_missed(self) -> None:
        """Navigate to missed questions review."""
        self.controller.show_frame(SCREEN_REVIEW)

    def _on_analytics(self) -> None:
        """Navigate to analytics view."""
        self.controller.show_frame(SCREEN_ANALYTICS)

    def _on_mix_test(self) -> None:
        """Open mix test dialog, then start a mixed test."""
        tests = self.test_service.get_all_tests()
        tests_with_counts = []
        for test in tests:
            q_count = self.test_service.get_question_count(test.id)
            if q_count > 0:
                tests_with_counts.append((test, q_count))

        if not tests_with_counts:
            messagebox.showinfo(
                "No Tests",
                "No tests with questions available for mixing.",
            )
            return

        dialog = MixTestDialog(self.winfo_toplevel(), tests_with_counts)
        result = dialog.get_result()
        if result is None:
            return

        test_ids, count = result

        # Show mode selection
        mode_dialog = ModeSelectionDialog(self.winfo_toplevel())
        mode = mode_dialog.get_mode()
        if mode is None:
            return

        questions = self.mix_service.select_questions(test_ids, count)
        if not questions:
            messagebox.showwarning(
                "No Questions", "Could not load questions from selected tests."
            )
            return

        selected_tests = [t for t, _ in tests_with_counts if t.id in test_ids]
        mix_display = build_mix_test_display(
            selected_tests,
            tests_with_counts,
            len(questions),
        )

        self.controller.show_frame(
            SCREEN_TEST_TAKING,
            mode=mode,
            questions=questions,
            mix_test_name=mix_display.title,
            mix_test_subtitle=mix_display.subtitle,
        )

    def _on_take_test(self, test) -> None:
        """Show mode dialog, then navigate to test-taking."""
        # Check for questions with no correct answer set
        questions = self.question_service.get_questions_for_test(test.id)
        missing = [q for q in questions if not q.correct_answer]
        if missing:
            proceed = messagebox.askyesno(
                "Missing Answers",
                f"{len(missing)} question(s) have no correct answer set. "
                "Scoring may not work correctly for those questions.\n\n"
                "Do you want to continue anyway?",
            )
            if not proceed:
                return

        dialog = ModeSelectionDialog(self.winfo_toplevel())
        mode = dialog.get_mode()
        if mode is None:
            return
        self.controller.show_frame(SCREEN_TEST_TAKING, test_id=test.id, mode=mode)

    def _on_edit_test(self, test) -> None:
        """Navigate to editor for an existing test."""
        self.controller.show_frame(SCREEN_EDITOR, test_id=test.id)

    def _on_export_test(self, test) -> None:
        """Validate and export a test to a JSON file."""
        try:
            warnings = self.export_service.validate_test(test.id)
        except ValueError as e:
            messagebox.showerror("Export Error", str(e))
            return

        if warnings:
            msg = "The following issues were found:\n\n"
            msg += "\n".join(f"  - {w}" for w in warnings)
            msg += "\n\nDo you want to export anyway?"
            if not messagebox.askyesno("Export Warnings", msg):
                return

        file_path = filedialog.asksaveasfilename(
            title="Export Test",
            defaultextension=".json",
            filetypes=EXPORT_FILE_TYPES,
            initialfile=f"{test.name}.json",
        )
        if not file_path:
            return

        try:
            self.export_service.export_to_json(test.id, file_path)
            messagebox.showinfo("Success", "Test exported successfully!")
        except Exception as e:
            messagebox.showerror("Export Error", f"Unexpected error: {e}")

    def _on_delete_test(self, test) -> None:
        """Confirm permanent deletion of a test."""
        if messagebox.askyesno(
            "Permanently Delete",
            f'Permanently delete "{test.name}"? This cannot be undone.\n\n'
            "This will also delete all questions and attempt history.",
        ):
            self.test_service.delete_test(test.id)
            self._refresh_test_list()

    def _on_archive_test(self, test) -> None:
        """Archive a test (hide but preserve)."""
        self.test_service.archive_test(test.id)
        self._refresh_test_list()

    def _on_unarchive_test(self, test) -> None:
        """Restore an archived test to the active list."""
        self.test_service.unarchive_test(test.id)
        self._refresh_test_list()

    def _on_archive_group(self, group_name: str) -> None:
        """Archive all tests in a group after confirmation."""
        if messagebox.askyesno(
            "Archive Group",
            f'Archive all tests in "{group_name}"?\n\n'
            "They will be hidden but can be restored from the Archived section.",
        ):
            self.test_service.archive_group(group_name)
            self._refresh_test_list()
