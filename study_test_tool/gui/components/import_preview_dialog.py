"""Import preview dialog with optional group assignment."""

from typing import List, Optional, Tuple

import customtkinter as ctk

from gui.styles import (
    RADIUS_CARD,
    RADIUS_CONTROL,
    SPACE_2,
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
from services.import_preview_service import ImportPreview


class ImportPreviewDialog(ctk.CTkToplevel):
    """Modal confirmation dialog shown before committing imported tests."""

    DIALOG_WIDTH = 680
    DIALOG_HEIGHT = 640

    def __init__(self, parent, previews: List[ImportPreview]) -> None:
        super().__init__(parent)
        self.title("Import Preview")
        self.geometry(f"{self.DIALOG_WIDTH}x{self.DIALOG_HEIGHT}")
        self.resizable(False, False)
        self.configure(fg_color=get_color("app_bg"))

        self._previews = previews
        self._result: Optional[Tuple[bool, str]] = None
        self._group_entry: Optional[ctk.CTkEntry] = None
        self._import_button: Optional[ctk.CTkButton] = None

        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - self.DIALOG_WIDTH) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.DIALOG_HEIGHT) // 2
        self.geometry(f"+{x}+{y}")

    def _build_ui(self) -> None:
        """Build the dialog layout."""
        importable = [preview for preview in self._previews if not preview.errors]
        skipped = [preview for preview in self._previews if preview.errors]
        warning_count = sum(1 for preview in importable if preview.warnings)
        total_questions = sum(preview.question_count for preview in importable)

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=SPACE_16, pady=SPACE_16)

        shell = ctk.CTkFrame(container, **get_card_style("default"))
        shell.pack(fill="both", expand=True)

        ctk.CTkLabel(
            shell,
            text="Import Preview",
            **get_text_style("section_title"),
        ).pack(pady=(SPACE_16, SPACE_4))

        ctk.CTkLabel(
            shell,
            text="Review detected tests before committing them to your library.",
            wraplength=500,
            justify="center",
            **get_text_style("card_description"),
        ).pack(padx=SPACE_24, pady=(0, SPACE_12))

        summary_frame = ctk.CTkFrame(shell, fg_color="transparent")
        summary_frame.pack(fill="x", padx=SPACE_24, pady=(0, SPACE_12))
        summary_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="summary")

        self._add_summary_tile(
            summary_frame, 0, "Ready", len(importable), "status_correct"
        )
        self._add_summary_tile(
            summary_frame,
            1,
            "Warnings",
            warning_count,
            "status_warning" if warning_count else "status_neutral",
        )
        self._add_summary_tile(
            summary_frame,
            2,
            "Skipped",
            len(skipped),
            "status_incorrect" if skipped else "status_neutral",
        )

        ctk.CTkLabel(
            shell,
            text=f"{total_questions} importable question(s)",
            **get_text_style("metadata"),
        ).pack(pady=(0, SPACE_8))

        group_frame = ctk.CTkFrame(
            shell,
            fg_color=get_color("surface_subtle"),
            corner_radius=RADIUS_CARD,
        )
        group_frame.pack(fill="x", padx=SPACE_24, pady=(0, SPACE_12))
        ctk.CTkLabel(
            group_frame,
            text="Group assignment",
            anchor="w",
            **get_text_style("card_metadata"),
        ).pack(fill="x", padx=SPACE_12, pady=(SPACE_8, 0))

        self._group_entry = ctk.CTkEntry(
            group_frame,
            height=34,
            fg_color=get_color("surface"),
            border_color=get_color("border"),
            text_color=get_color("text_primary"),
            placeholder_text="Optional group override",
        )
        self._group_entry.pack(fill="x", padx=SPACE_12, pady=(0, SPACE_8))

        existing_groups = sorted({p.group_name for p in importable if p.group_name})
        if len(existing_groups) == 1:
            self._group_entry.insert(0, existing_groups[0])

        scroll = ctk.CTkScrollableFrame(
            shell,
            height=220,
            fg_color=get_color("surface_subtle"),
            corner_radius=RADIUS_CARD,
            scrollbar_button_color=get_color("surface_muted"),
            scrollbar_button_hover_color=get_color("border"),
        )
        scroll.pack(fill="x", padx=SPACE_24, pady=(0, SPACE_12))

        for preview in self._previews:
            self._add_preview_row(scroll, preview)

        btn_frame = ctk.CTkFrame(shell, fg_color="transparent")
        btn_frame.pack(fill="x", padx=SPACE_24, pady=(0, SPACE_16))
        btn_frame.grid_columnconfigure((0, 1), weight=1, uniform="import_actions")

        self._import_button = ctk.CTkButton(
            btn_frame,
            text="Import",
            height=36,
            command=self._on_import,
            **get_button_style("primary"),
        )
        self._import_button.grid(row=0, column=0, sticky="ew", padx=(0, SPACE_8))
        if not importable:
            self._import_button.configure(
                state="disabled",
                fg_color=get_color("surface_muted"),
                text_color=get_color("text_disabled"),
                text_color_disabled=get_color("text_disabled"),
            )

        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            height=36,
            command=self._on_cancel,
            **get_button_style("secondary"),
        ).grid(row=0, column=1, sticky="ew", padx=(SPACE_8, 0))

    def _add_summary_tile(
        self,
        parent,
        column: int,
        label: str,
        value: int,
        color_role: str,
    ) -> None:
        """Add a compact import summary tile."""
        tile = ctk.CTkFrame(
            parent,
            fg_color=get_color("surface_subtle"),
            corner_radius=RADIUS_CARD,
        )
        tile.grid(row=0, column=column, sticky="ew", padx=SPACE_4)

        ctk.CTkLabel(
            tile,
            text=label,
            anchor="w",
            **get_text_style("card_metadata"),
        ).pack(fill="x", padx=SPACE_12, pady=(SPACE_8, 0))

        style = get_text_style("body_bold")
        style["text_color"] = get_color(color_role)
        ctk.CTkLabel(
            tile,
            text=str(value),
            anchor="w",
            **style,
        ).pack(fill="x", padx=SPACE_12, pady=(0, SPACE_8))

    def _add_preview_row(self, parent, preview: ImportPreview) -> None:
        row = ctk.CTkFrame(parent, **get_card_style("default"))
        row.pack(fill="x", pady=(SPACE_4, SPACE_8), padx=SPACE_4)

        status, color_role = self._preview_status(preview)
        color = get_color(color_role)

        header = ctk.CTkFrame(row, fg_color="transparent")
        header.pack(fill="x", padx=SPACE_12, pady=(SPACE_12, SPACE_4))

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            title_frame,
            text=preview.test_name,
            anchor="w",
            **get_text_style("body_bold"),
        ).pack(fill="x")

        metadata = f"{preview.source_name} / {preview.question_count} question(s)"
        if preview.group_name:
            metadata += f" / {preview.group_name}"

        ctk.CTkLabel(
            title_frame,
            text=metadata,
            anchor="w",
            **get_text_style("card_metadata"),
        ).pack(fill="x", pady=(SPACE_2, 0))

        pill = ctk.CTkFrame(
            header,
            height=28,
            fg_color=get_color("surface_subtle"),
            corner_radius=RADIUS_CONTROL,
        )
        pill.pack(side="right", padx=(SPACE_12, 0))

        status_style = get_text_style("metadata")
        status_style["text_color"] = color
        ctk.CTkLabel(
            pill,
            text=status,
            **status_style,
        ).pack(padx=SPACE_8, pady=SPACE_4)

        messages = preview.errors or preview.warnings
        if messages:
            text = "\n".join(f"- {message}" for message in messages[:4])
            if len(messages) > 4:
                text += f"\n- {len(messages) - 4} more message(s)"
            message_style = get_text_style("card_metadata")
            message_style["text_color"] = color
            ctk.CTkLabel(
                row,
                text=text,
                anchor="w",
                justify="left",
                wraplength=580,
                **message_style,
            ).pack(fill="x", padx=SPACE_12, pady=(SPACE_4, SPACE_12))
        else:
            ctk.CTkLabel(
                row,
                text="No warnings detected.",
                anchor="w",
                **get_text_style("card_metadata"),
            ).pack(fill="x", padx=SPACE_12, pady=(SPACE_4, SPACE_12))

    @staticmethod
    def _preview_status(preview: ImportPreview) -> tuple[str, str]:
        """Return display status and color role for a preview row."""
        if preview.errors:
            return "Skipped", "status_incorrect"
        if preview.warnings:
            return "Warnings", "status_warning"
        return "Ready", "status_correct"

    def _on_import(self) -> None:
        group_name = self._group_entry.get().strip() if self._group_entry else ""
        self._result = (True, group_name)
        self.destroy()

    def _on_cancel(self) -> None:
        self._result = (False, "")
        self.destroy()

    def get_result(self) -> Optional[Tuple[bool, str]]:
        """Return ``(confirmed, group_name)`` after the dialog closes."""
        self.wait_window()
        return self._result
