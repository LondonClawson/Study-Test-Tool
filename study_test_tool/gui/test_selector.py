"""Home screen — test selector with import, create, and test list."""

import json
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

import customtkinter as ctk

from config.user_preferences import TEXT_SIZE_OPTIONS
from gui.components.collapsible_group import CollapsibleGroup
from gui.components.import_preview_dialog import ImportPreviewDialog
from gui.components.mix_test_dialog import MixTestDialog
from gui.components.mode_dialog import ModeSelectionDialog
from gui.mix_test_display import build_mix_test_display
from gui.styles import (
    FONT_METADATA,
    RADIUS_CARD,
    RADIUS_CONTROL,
    SPACE_2,
    SPACE_4,
    SPACE_8,
    SPACE_12,
    SPACE_16,
    SPACE_24,
    SPACE_32,
    get_button_style,
    get_card_style,
    get_color,
    get_header_style,
    get_text_style,
)
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
        self._deferred_group_cards: dict[str, tuple[list, bool]] = {}
        self._rendered_group_keys: set[str] = set()

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the home screen layout."""
        self.configure(fg_color=get_color("app_bg"))

        # Page header
        header_frame = ctk.CTkFrame(
            self,
            **get_header_style("page"),
        )
        header_frame.pack(fill="x", padx=SPACE_24, pady=(SPACE_24, SPACE_16))

        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=SPACE_24, pady=(SPACE_16, SPACE_8))

        ctk.CTkLabel(
            title_frame,
            text="Study Testing Tool",
            anchor="w",
            **get_text_style("page_title"),
        ).pack(fill="x")

        self._header_summary_label = ctk.CTkLabel(
            title_frame,
            text="",
            anchor="w",
            **get_text_style("page_subtitle"),
        )
        self._header_summary_label.pack(fill="x", pady=(SPACE_4, 0))

        action_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        action_frame.pack(fill="x", padx=SPACE_24, pady=(0, SPACE_16))

        primary_actions = ctk.CTkFrame(action_frame, fg_color="transparent")
        primary_actions.pack(fill="x")

        navigation_actions = ctk.CTkFrame(action_frame, fg_color="transparent")
        navigation_actions.pack(fill="x", pady=(SPACE_8, 0))

        ctk.CTkButton(
            primary_actions,
            text="Import",
            command=self._on_import,
            width=120,
            **get_button_style("secondary"),
        ).pack(side="left", padx=(0, SPACE_8))

        ctk.CTkButton(
            primary_actions,
            text="New Test",
            command=self._on_new_test,
            width=120,
            **get_button_style("primary"),
        ).pack(side="left", padx=(0, SPACE_8))

        ctk.CTkButton(
            primary_actions,
            text="Mix Test",
            command=self._on_mix_test,
            width=120,
            **get_button_style("special"),
        ).pack(side="left")

        text_size_frame = ctk.CTkFrame(primary_actions, fg_color="transparent")
        text_size_frame.pack(side="right")

        ctk.CTkLabel(
            text_size_frame,
            text="Text Size",
            **get_text_style("metadata"),
        ).pack(side="left", padx=(0, SPACE_8))

        self._text_size_menu = ctk.CTkOptionMenu(
            text_size_frame,
            values=TEXT_SIZE_OPTIONS,
            width=132,
            height=34,
            font=FONT_METADATA,
            fg_color=get_color("surface_subtle"),
            button_color=get_color("surface_muted"),
            button_hover_color=get_color("divider"),
            text_color=get_color("text_primary"),
            dropdown_fg_color=get_color("surface"),
            dropdown_hover_color=get_color("surface_subtle"),
            dropdown_text_color=get_color("text_primary"),
            command=self._on_text_size_changed,
        )
        self._text_size_menu.set(self.controller.get_text_size())
        self._text_size_menu.pack(side="left")

        ctk.CTkButton(
            navigation_actions,
            text="Review Missed",
            command=self._on_review_missed,
            width=120,
            **get_button_style("warning"),
        ).pack(side="left", padx=(0, SPACE_8))

        ctk.CTkButton(
            navigation_actions,
            text="View History",
            command=self._on_view_history,
            width=120,
            **get_button_style("secondary"),
        ).pack(side="left", padx=(0, SPACE_8))

        ctk.CTkButton(
            navigation_actions,
            text="Analytics",
            command=self._on_analytics,
            width=120,
            **get_button_style("secondary"),
        ).pack(side="left")

        # Sort toolbar
        sort_frame = ctk.CTkFrame(
            self,
            fg_color=get_color("surface"),
            border_color=get_color("border"),
            border_width=1,
            corner_radius=RADIUS_CARD,
        )
        sort_frame.pack(fill="x", padx=SPACE_24, pady=(0, SPACE_12))

        ctk.CTkLabel(
            sort_frame,
            text="Sort by:",
            **get_text_style("metadata"),
        ).pack(side="left", padx=(SPACE_16, SPACE_8), pady=SPACE_12)

        self._sort_menu = ctk.CTkOptionMenu(
            sort_frame,
            values=[
                "Last Updated",
                "Name (A-Z)",
                "Name (Z-A)",
                "Date Created",
            ],
            width=160,
            height=34,
            font=FONT_METADATA,
            fg_color=get_color("surface_subtle"),
            button_color=get_color("surface_muted"),
            button_hover_color=get_color("divider"),
            text_color=get_color("text_primary"),
            dropdown_fg_color=get_color("surface"),
            dropdown_hover_color=get_color("surface_subtle"),
            dropdown_text_color=get_color("text_primary"),
            command=self._on_sort_changed,
        )
        self._sort_menu.set(self._sort_by)
        self._sort_menu.pack(side="left", pady=SPACE_12)

        self._collapse_all_btn = ctk.CTkButton(
            sort_frame,
            text="Collapse All",
            width=110,
            height=34,
            command=self._on_collapse_all_toggle,
            **get_button_style("tertiary"),
        )
        self._collapse_all_btn.pack(side="left", padx=(SPACE_12, 0), pady=SPACE_12)

        # Scrollable test list
        self.test_list_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=get_color("surface_subtle"),
            border_color=get_color("border"),
            border_width=1,
            corner_radius=RADIUS_CARD,
            scrollbar_button_color=get_color("secondary"),
            scrollbar_button_hover_color=get_color("secondary_hover"),
        )
        self.test_list_frame.pack(
            fill="both",
            expand=True,
            padx=SPACE_24,
            pady=(0, SPACE_24),
        )

        self.empty_state_frame = self._build_empty_state()

    def _build_empty_state(self) -> ctk.CTkFrame:
        """Create the no-tests state surface."""
        empty_frame = ctk.CTkFrame(self.test_list_frame, **get_card_style("default"))

        ctk.CTkLabel(
            empty_frame,
            text="Start your study library",
            anchor="center",
            **get_text_style("section_title"),
        ).pack(fill="x", padx=SPACE_24, pady=(SPACE_24, SPACE_8))

        ctk.CTkLabel(
            empty_frame,
            text="Import an existing test or create a new one to begin.",
            anchor="center",
            **get_text_style("metadata"),
        ).pack(fill="x", padx=SPACE_24)

        action_frame = ctk.CTkFrame(empty_frame, fg_color="transparent")
        action_frame.pack(pady=(SPACE_16, SPACE_24))

        ctk.CTkButton(
            action_frame,
            text="Import",
            width=120,
            command=self._on_import,
            **get_button_style("secondary"),
        ).pack(side="left", padx=(0, SPACE_8))

        ctk.CTkButton(
            action_frame,
            text="New Test",
            width=120,
            command=self._on_new_test,
            **get_button_style("primary"),
        ).pack(side="left")

        return empty_frame

    def on_show(self, **kwargs) -> None:
        """Refresh the test list when this screen is shown."""
        self._text_size_menu.set(self.controller.get_text_size())
        self._refresh_test_list()

    def _on_text_size_changed(self, value: str) -> None:
        """Apply the selected app text size."""
        self.controller.set_text_size(value)

    def _update_header_summary(self, active_count: int, archived_count: int) -> None:
        """Update the page header metadata from the current test list."""
        if active_count == 0 and archived_count == 0:
            summary = "No tests yet"
        else:
            active_text = (
                f"{active_count} active test{'s' if active_count != 1 else ''}"
            )
            if archived_count:
                archived_text = (
                    f"{archived_count} archived test"
                    f"{'s' if archived_count != 1 else ''}"
                )
                summary = f"{active_text} | {archived_text}"
            else:
                summary = active_text
        self._header_summary_label.configure(text=summary)

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
        old_group_states = {
            name: w.is_expanded for name, w in self._group_widgets.items()
        }

        for widget in self.test_list_frame.winfo_children():
            if widget != self.empty_state_frame:
                widget.destroy()
        self._group_widgets = {}
        self._deferred_group_cards = {}
        self._rendered_group_keys = set()

        tests = self.test_service.get_all_tests()
        archived_tests = self.test_service.get_archived_tests()
        question_counts = self.test_service.get_all_question_counts()
        self._update_header_summary(len(tests), len(archived_tests))

        if not tests and not archived_tests:
            self.empty_state_frame.pack(
                fill="x",
                padx=SPACE_24,
                pady=(SPACE_32, 0),
            )
            return

        self.empty_state_frame.pack_forget()

        tests = self._sort_tests(tests)

        # Always render in groups: named groups alphabetically, "Ungrouped" last
        grouped: dict[str, list] = {}
        for test in tests:
            group = test.group_name if test.group_name else "Ungrouped"
            grouped.setdefault(group, []).append(test)

        named_groups = sorted(k for k in grouped if k != "Ungrouped")
        ordered_groups = named_groups + (
            ["Ungrouped"] if "Ungrouped" in grouped else []
        )

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
                on_expand=lambda key=group: self._render_group_cards(key),
            )
            group_widget.pack(fill="x", pady=(0, SPACE_8))
            self._group_widgets[group] = group_widget
            self._deferred_group_cards[group] = (
                [(test, question_counts.get(test.id, 0)) for test in group_tests],
                False,
            )
            if was_expanded:
                self._render_group_cards(group)

        if archived_tests:
            archived_widget = CollapsibleGroup(
                self.test_list_frame,
                group_name="Archived Tests",
                test_count=len(archived_tests),
                expanded=old_group_states.get("__archived__", False),
                on_expand=lambda: self._render_group_cards("__archived__"),
            )
            archived_widget.pack(fill="x", pady=(SPACE_8, 0))
            self._group_widgets["__archived__"] = archived_widget
            self._deferred_group_cards["__archived__"] = (
                [(test, question_counts.get(test.id, 0)) for test in archived_tests],
                True,
            )
            if archived_widget.is_expanded:
                self._render_group_cards("__archived__")

    def _render_group_cards(self, group_key: str) -> None:
        """Create a group's cards the first time its content is displayed."""
        if group_key in self._rendered_group_keys:
            return

        group_widget = self._group_widgets.get(group_key)
        card_data = self._deferred_group_cards.get(group_key)
        if group_widget is None or card_data is None:
            return

        cards, archived = card_data
        for test, question_count in cards:
            if archived:
                self._create_archived_test_card(
                    test,
                    question_count,
                    parent=group_widget.content_frame,
                )
            else:
                self._create_test_card(
                    test,
                    question_count,
                    parent=group_widget.content_frame,
                )
        self._rendered_group_keys.add(group_key)

    def _create_test_card(
        self, test, q_count: int, parent: ctk.CTkFrame = None
    ) -> None:
        """Create a card widget for a single test."""
        if parent is None:
            parent = self.test_list_frame
        card = ctk.CTkFrame(parent, **get_card_style("default"))
        card.pack(fill="x", pady=SPACE_4, padx=SPACE_4)

        card_body = ctk.CTkFrame(card, fg_color="transparent")
        card_body.pack(fill="x", padx=SPACE_16, pady=SPACE_16)
        card_body.grid_columnconfigure(0, weight=1)

        # Info section
        info_frame = ctk.CTkFrame(card_body, fg_color="transparent")
        info_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, SPACE_16),
        )

        ctk.CTkLabel(
            info_frame,
            text=test.name,
            anchor="w",
            **get_text_style("card_title"),
        ).pack(fill="x")

        desc_text = test.description if test.description else "No description"
        ctk.CTkLabel(
            info_frame,
            text=desc_text,
            anchor="w",
            **get_text_style("card_description"),
        ).pack(fill="x", pady=(SPACE_4, SPACE_8))

        self._build_card_metadata(info_frame, test, q_count)

        # Action buttons
        btn_frame = ctk.CTkFrame(card_body, fg_color="transparent")
        btn_frame.grid(row=0, column=1, sticky="ne")
        btn_frame.grid_columnconfigure((0, 1), weight=1, uniform="card_actions")

        take_btn = ctk.CTkButton(
            btn_frame,
            text="Take Test",
            width=184,
            height=34,
            command=lambda t=test: self._on_take_test(t),
            **get_button_style("primary"),
        )
        take_btn.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=SPACE_2,
            pady=(0, SPACE_8),
        )
        if q_count == 0:
            self._configure_disabled_take_test(take_btn)

        ctk.CTkButton(
            btn_frame,
            text="Edit",
            width=88,
            height=32,
            command=lambda t=test: self._on_edit_test(t),
            **get_button_style("tertiary"),
        ).grid(row=1, column=0, sticky="ew", padx=SPACE_2, pady=(0, SPACE_4))

        ctk.CTkButton(
            btn_frame,
            text="Export",
            width=88,
            height=32,
            command=lambda t=test: self._on_export_test(t),
            **get_button_style("tertiary"),
        ).grid(row=1, column=1, sticky="ew", padx=SPACE_2, pady=(0, SPACE_4))

        ctk.CTkButton(
            btn_frame,
            text="Archive",
            width=88,
            height=32,
            command=lambda t=test: self._on_archive_test(t),
            **get_button_style("secondary"),
        ).grid(row=2, column=0, sticky="ew", padx=SPACE_2)

        ctk.CTkButton(
            btn_frame,
            text="Delete",
            width=88,
            height=32,
            command=lambda t=test: self._on_delete_test(t),
            **get_button_style("danger"),
        ).grid(row=2, column=1, sticky="ew", padx=SPACE_2)

    def _create_archived_test_card(
        self, test, q_count: int, parent: ctk.CTkFrame = None
    ) -> None:
        """Create a dimmed card widget for an archived test."""
        if parent is None:
            parent = self.test_list_frame
        card = ctk.CTkFrame(parent, **get_card_style("muted"))
        card.pack(fill="x", pady=SPACE_4, padx=SPACE_4)

        card_body = ctk.CTkFrame(card, fg_color="transparent")
        card_body.pack(fill="x", padx=SPACE_16, pady=SPACE_16)
        card_body.grid_columnconfigure(0, weight=1)

        info_frame = ctk.CTkFrame(card_body, fg_color="transparent")
        info_frame.grid(row=0, column=0, sticky="nsew", padx=(0, SPACE_16))

        title_row = ctk.CTkFrame(info_frame, fg_color="transparent")
        title_row.pack(fill="x")

        ctk.CTkLabel(
            title_row,
            text=test.name,
            anchor="w",
            **get_text_style("card_title_muted"),
        ).pack(side="left", fill="x", expand=True)

        self._build_metadata_chip(
            title_row,
            "Archived",
            muted=True,
            compact=True,
        ).pack(side="right", padx=(SPACE_8, 0))

        desc_text = test.description if test.description else "No description"
        ctk.CTkLabel(
            info_frame,
            text=desc_text,
            anchor="w",
            **get_text_style("card_metadata_muted"),
        ).pack(fill="x", pady=(SPACE_4, SPACE_8))

        self._build_card_metadata(info_frame, test, q_count, muted=True)

        btn_frame = ctk.CTkFrame(card_body, fg_color="transparent")
        btn_frame.grid(row=0, column=1, sticky="ne")
        btn_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            btn_frame,
            text="Unarchive",
            width=128,
            height=34,
            command=lambda t=test: self._on_unarchive_test(t),
            **get_button_style("secondary"),
        ).grid(row=0, column=0, sticky="ew", padx=SPACE_2, pady=(0, SPACE_8))

        ctk.CTkButton(
            btn_frame,
            text="Delete",
            width=128,
            height=32,
            command=lambda t=test: self._on_delete_test(t),
            **get_button_style("danger"),
        ).grid(row=1, column=0, sticky="ew", padx=SPACE_2)

    def _build_card_metadata(
        self,
        parent: ctk.CTkFrame,
        test,
        q_count: int,
        muted: bool = False,
    ) -> None:
        """Build compact card metadata chips."""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x")

        count_text = f"{q_count} question{'s' if q_count != 1 else ''}"
        self._build_metadata_chip(
            row,
            count_text,
            muted=muted or q_count == 0,
        ).pack(side="left", padx=(0, SPACE_8))

        if test.group_name:
            self._build_metadata_chip(
                row,
                test.group_name,
                muted=muted,
            ).pack(side="left", padx=(0, SPACE_8))

    def _build_metadata_chip(
        self,
        parent: ctk.CTkFrame,
        text: str,
        muted: bool = False,
        compact: bool = False,
    ) -> ctk.CTkLabel:
        """Create a compact metadata chip for a Home card."""
        style = get_text_style("metadata")
        if muted:
            style["text_color"] = get_color("text_muted")

        return ctk.CTkLabel(
            parent,
            text=text,
            height=22 if compact else 24,
            fg_color=get_color("surface_subtle" if muted else "surface_muted"),
            corner_radius=RADIUS_CONTROL,
            anchor="center",
            **style,
        )

    def _configure_disabled_take_test(self, button: ctk.CTkButton) -> None:
        """Style disabled Take Test without changing the disabled behavior."""
        button.configure(
            state="disabled",
            fg_color=get_color("surface_muted"),
            hover_color=get_color("surface_muted"),
            text_color=get_color("text_disabled"),
            text_color_disabled=get_color("text_disabled"),
            border_color=get_color("border"),
            border_width=1,
        )

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

        lines = [
            f"Processed: {len(results)}",
            f"Succeeded: {len(succeeded)}",
            f"Skipped: {len(skipped)}",
            "",
        ]
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
        question_counts = self.test_service.get_all_question_counts()
        tests_with_counts = []
        for test in tests:
            q_count = question_counts.get(test.id, 0)
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
