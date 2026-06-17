#!/usr/bin/env python3
"""Capture visual-overhaul baseline screenshots with seeded app data.

This is a development-only harness. It creates an isolated SQLite database,
drives the CustomTkinter app through its frame controller, and captures named
screenshots for the visual overhaul audit. It does not touch the user's normal
application database.
"""

from __future__ import annotations

import argparse
import colorsys
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = REPO_ROOT / "study_test_tool"
DEFAULT_OUTPUT_DIR = (
    REPO_ROOT / "visual_overhaul_project" / "01_context" / "screenshots" / "baseline"
)
GROUPS = (
    "all",
    "home",
    "dialogs",
    "editor",
    "test-taking",
    "results",
    "data",
    "empty",
)

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

try:
    from PIL import Image, ImageStat
except ImportError as exc:  # pragma: no cover - environment guard
    missing = exc.name or "required dependency"
    raise SystemExit(f"Missing {missing}. Install app requirements first.") from exc

try:
    import customtkinter as ctk
except ImportError:  # pragma: no cover - validate-only can run without GUI deps
    ctk = None

try:
    import Quartz
except ImportError:  # pragma: no cover - validate-only can run without Quartz
    Quartz = None

import config.database as database_config
import config.settings as settings
from config.database import initialize_database
from database.db_manager import DatabaseManager
from models.question import Question, QuestionOption
from models.test_result import QuestionResponse, TestAttempt
from services.scoring_service import ScoringService
from services.test_session import TestSession
from utils.constants import (
    MODE_PRACTICE,
    MODE_TEST,
    SCREEN_ANALYTICS,
    SCREEN_EDITOR,
    SCREEN_HISTORY,
    SCREEN_HOME,
    SCREEN_RESULTS,
    SCREEN_REVIEW,
    SCREEN_TEST_TAKING,
)

App = None
MixTestDialog = None
build_mix_test_display = None
ModeSelectionDialog = None


def ensure_gui_modules() -> None:
    """Load GUI modules only when capture mode needs them."""
    global App, MixTestDialog, build_mix_test_display, ModeSelectionDialog

    if ctk is None:
        raise RuntimeError("customtkinter is required for capture.")
    if App is not None:
        return

    from gui.components.mix_test_dialog import MixTestDialog as ImportedMixTestDialog
    from gui.components.mode_dialog import (
        ModeSelectionDialog as ImportedModeSelectionDialog,
    )
    from gui.main_window import App as ImportedApp
    from gui.mix_test_display import (
        build_mix_test_display as imported_build_mix_test_display,
    )

    App = ImportedApp
    MixTestDialog = ImportedMixTestDialog
    build_mix_test_display = imported_build_mix_test_display
    ModeSelectionDialog = ImportedModeSelectionDialog


@dataclass
class SeedData:
    """IDs and objects needed to drive screenshot states."""

    db_path: Path
    active_test_id: int
    second_test_id: int
    essay_test_id: int
    archived_test_id: int
    empty_attempt_id: int
    partial_attempt_id: int
    high_attempt_id: int
    questions_by_test: Dict[int, List[Question]]


@dataclass(frozen=True)
class CaptureState:
    """A named visual state the harness can capture."""

    name: str
    group: str
    source: str
    action: Callable[
        ["App", Optional[SeedData], "ScreenshotHarness"],
        Optional[Callable[[], None]],
    ]


@dataclass
class ValidationResult:
    """Validation outcome for one screenshot."""

    path: Path
    ok: bool
    reason: str = ""


class ScreenshotHarness:
    """Drive app states and capture screenshots."""

    def __init__(self, app: App, output_dir: Path, mode: str) -> None:
        self.app = app
        self.output_dir = output_dir
        self.mode = mode

    def capture(self, name: str) -> None:
        """Capture the current app window."""
        self._settle()
        self._bring_app_to_front()
        try:
            target = self.output_dir / self.mode / f"{self.mode}_{name}.png"
            target.parent.mkdir(parents=True, exist_ok=True)
            bounds = self._find_app_bounds()
            if bounds is None:
                raise RuntimeError("Could not find the Study Testing Tool window.")
            rect = self._screencapture_rect(bounds)
            subprocess.run(
                [
                    "screencapture",
                    "-x",
                    "-R",
                    f"{rect[0]},{rect[1]},{rect[2]},{rect[3]}",
                    str(target),
                ],
                check=True,
            )
            try:
                display_target = target.relative_to(REPO_ROOT)
            except ValueError:
                display_target = target
            print(f"captured {display_target}")
        finally:
            self._release_app_front()

    def show_frame(self, screen_name: str, **kwargs) -> None:
        """Raise an app frame and wait for Tk to render it."""
        self.app.show_frame(screen_name, **kwargs)
        self._settle()

    def use_default_geometry(self) -> None:
        """Reset the app to the default capture geometry."""
        self.app.geometry(f"{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}+80+80")
        self._settle()

    def use_minimum_geometry(self) -> None:
        """Resize the app to the documented minimum supported geometry."""
        self.app.geometry(
            f"{settings.MIN_WINDOW_WIDTH}x{settings.MIN_WINDOW_HEIGHT}+80+80"
        )
        self._settle()

    def show_history_sync(self) -> None:
        """Raise history and load table data without its background thread."""
        self.app._current_screen = SCREEN_HISTORY
        frame = self.app.frames[SCREEN_HISTORY]
        frame.tkraise()
        frame._show_loading_state()
        attempts = frame.scoring_service.get_all_attempts()
        tests = frame.test_service.get_all_tests()
        frame._on_data_loaded(attempts, tests)
        self._settle()

    def _settle(self) -> None:
        """Let Tk and the macOS compositor catch up before capture."""
        self.app.update_idletasks()
        self.app.update()
        time.sleep(0.25)
        self.app.update_idletasks()
        self.app.update()

    def _bring_app_to_front(self) -> None:
        """Keep the app unobscured while screencapture reads its screen region."""
        try:
            self.app.lift()
            self.app.focus_force()
            self.app.attributes("-topmost", True)
            self.app.update_idletasks()
            self.app.update()
            time.sleep(0.1)
        except Exception:
            pass

    def _release_app_front(self) -> None:
        """Return the app to normal stacking after capture."""
        try:
            self.app.attributes("-topmost", False)
            self.app.update_idletasks()
            self.app.update()
        except Exception:
            pass

    def _find_app_bounds(self) -> Optional[Dict[str, int]]:
        """Return CoreGraphics bounds for the main app window."""
        if Quartz is None:
            raise RuntimeError(
                "PyObjC Quartz is required for capture. Install "
                "pyobjc-framework-Quartz."
            )
        windows = Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListOptionOnScreenOnly,
            Quartz.kCGNullWindowID,
        )
        if not windows:
            return None

        candidates = []
        for window in windows:
            owner = window.get("kCGWindowOwnerName")
            bounds = window.get("kCGWindowBounds") or {}
            if owner != "Python":
                continue
            if bounds.get("Width", 0) < 700 or bounds.get("Height", 0) < 500:
                continue
            candidates.append(bounds)

        if not candidates:
            return None
        return max(candidates, key=lambda b: b.get("Width", 0) * b.get("Height", 0))

    def _screencapture_rect(self, bounds: Dict[str, int]) -> tuple[int, int, int, int]:
        """Convert CoreGraphics point bounds into screencapture pixels."""
        scale = self._display_scale(bounds)
        x = int(bounds["X"] * scale)
        y = int(bounds["Y"] * scale)
        width = int(bounds["Width"] * scale)
        height = int(bounds["Height"] * scale)
        return x, y, width, height

    def _display_scale(self, bounds: Dict[str, int]) -> float:
        """Find the backing scale for the display containing the window."""
        displays = Quartz.CGGetActiveDisplayList(16, None, None)[1]
        center_x = bounds["X"] + bounds["Width"] / 2
        center_y = bounds["Y"] + bounds["Height"] / 2

        for display_id in displays:
            display_bounds = Quartz.CGDisplayBounds(display_id)
            if (
                display_bounds.origin.x
                <= center_x
                <= display_bounds.origin.x + display_bounds.size.width
                and display_bounds.origin.y
                <= center_y
                <= display_bounds.origin.y + display_bounds.size.height
            ):
                pixel_width = Quartz.CGDisplayPixelsWide(display_id)
                return pixel_width / display_bounds.size.width
        return 1.0


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Capture seeded baseline screenshots for the visual overhaul."
    )
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Appearance mode to capture.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Screenshot output root.",
    )
    parser.add_argument(
        "--keep-db",
        action="store_true",
        help="Keep the temporary seeded database for debugging.",
    )
    parser.add_argument(
        "--states",
        nargs="*",
        help="Optional list of state names to capture. Takes precedence over --group.",
    )
    parser.add_argument(
        "--group",
        choices=GROUPS,
        default="all",
        help="Capture a named group of states.",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate expected screenshots without launching the GUI.",
    )
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip post-capture screenshot validation.",
    )
    return parser.parse_args()


def configure_database(db_path: Path) -> None:
    """Point app services at an isolated database."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    initialize_database(str(db_path))
    settings.DB_PATH = db_path
    database_config.DB_PATH = db_path


def add_question(
    db: DatabaseManager,
    test_id: int,
    text: str,
    correct_answer: str,
    category: str,
    options: Optional[List[str]] = None,
) -> int:
    """Insert a multiple-choice or essay question."""
    if options is None:
        question = Question(
            test_id=test_id,
            text=text,
            type=settings.QUESTION_TYPE_ESSAY,
            correct_answer=correct_answer,
            category=category,
        )
    else:
        question = Question(
            test_id=test_id,
            text=text,
            type=settings.QUESTION_TYPE_MC,
            correct_answer=correct_answer,
            category=category,
            options=[
                QuestionOption(text=option, is_correct=option == correct_answer)
                for option in options
            ],
        )
    return db.add_question(question)


def save_attempt(
    db: DatabaseManager,
    test_id: int,
    responses: Iterable[QuestionResponse],
    score: int,
    total_questions: int,
    percentage: float,
    mode: str = MODE_TEST,
    time_taken: int = 420,
) -> int:
    """Insert an attempt and its responses."""
    attempt_id = db.save_attempt(
        TestAttempt(
            test_id=test_id,
            score=score,
            total_questions=total_questions,
            percentage=percentage,
            time_taken=time_taken,
            mode=mode,
        )
    )
    for response in responses:
        response.attempt_id = attempt_id
        db.save_response(response)
    return attempt_id


def seed_database(db_path: Path) -> SeedData:
    """Create representative app data for visual capture."""
    db_path.unlink(missing_ok=True)
    configure_database(db_path)
    db = DatabaseManager(str(db_path))

    active_test_id = db.create_test(
        settings_test(
            "Cardiology Board Review",
            "High-yield practice set with categories and mixed question types.",
            "Clinical Medicine",
        )
    )
    second_test_id = db.create_test(
        settings_test(
            "Pharmacology Quick Drill",
            "Medication mechanism and safety review.",
            "Clinical Medicine",
        )
    )
    essay_test_id = db.create_test(
        settings_test(
            "Pathophysiology Essays",
            "Short-answer prompts for explaining mechanisms.",
            "",
        )
    )
    archived_test_id = db.create_test(
        settings_test(
            "Archived Anatomy Final",
            "Older final exam prep set retained for reference.",
            "Archived Courses",
        )
    )

    active_questions = [
        add_question(
            db,
            active_test_id,
            "Which finding most strongly supports acute decompensated heart failure?",
            "Bilateral pulmonary crackles with elevated BNP",
            "Cardiology",
            [
                "Normal jugular venous pressure",
                "Bilateral pulmonary crackles with elevated BNP",
                "Isolated wheezing after exercise",
                "Low serum creatinine",
            ],
        ),
        add_question(
            db,
            active_test_id,
            "A patient with atrial fibrillation needs stroke-risk counseling. Which score is commonly used?",
            "CHA2DS2-VASc",
            "Cardiology",
            ["CURB-65", "Wells", "CHA2DS2-VASc", "APACHE II"],
        ),
        add_question(
            db,
            active_test_id,
            "Explain why loop diuretics can cause hypokalemia.",
            "Increased distal sodium delivery promotes potassium secretion.",
            "Renal",
            None,
        ),
    ]
    second_questions = [
        add_question(
            db,
            second_test_id,
            "Which medication class is first-line for anaphylaxis?",
            "Epinephrine",
            "Emergency",
            ["Diphenhydramine", "Epinephrine", "Albuterol", "Prednisone"],
        ),
        add_question(
            db,
            second_test_id,
            "Which adverse effect is most associated with aminoglycosides?",
            "Ototoxicity",
            "Pharmacology",
            ["Ototoxicity", "Hyperkalemia", "Photosensitivity", "Sedation"],
        ),
    ]
    essay_questions = [
        add_question(
            db,
            essay_test_id,
            "Compare preload and afterload in one concise paragraph.",
            "Preload reflects ventricular filling; afterload reflects ejection resistance.",
            "Physiology",
            None,
        )
    ]
    archived_questions = [
        add_question(
            db,
            archived_test_id,
            "Which structure passes through the foramen magnum?",
            "Medulla oblongata",
            "Anatomy",
            ["Optic nerve", "Medulla oblongata", "Facial nerve", "Carotid artery"],
        )
    ]
    db.archive_test(archived_test_id)

    partial_attempt_id = save_attempt(
        db,
        active_test_id,
        [
            QuestionResponse(
                active_questions[0], "Normal jugular venous pressure", False, True, 65
            ),
            QuestionResponse(active_questions[1], "CHA2DS2-VASc", True, False, 44),
            QuestionResponse(
                active_questions[2],
                "Loop diuretics increase sodium delivery downstream.",
                None,
                False,
                120,
            ),
        ],
        score=1,
        total_questions=3,
        percentage=50.0,
        mode=MODE_TEST,
    )
    high_attempt_id = save_attempt(
        db,
        second_test_id,
        [
            QuestionResponse(second_questions[0], "Epinephrine", True, False, 35),
            QuestionResponse(second_questions[1], "Ototoxicity", True, False, 42),
        ],
        score=2,
        total_questions=2,
        percentage=100.0,
        mode=MODE_PRACTICE,
    )
    empty_attempt_id = save_attempt(
        db,
        essay_test_id,
        [
            QuestionResponse(
                essay_questions[0],
                "Preload is filling; afterload is resistance.",
                None,
                False,
                95,
            )
        ],
        score=0,
        total_questions=1,
        percentage=0.0,
        mode=MODE_TEST,
    )

    return SeedData(
        db_path=db_path,
        active_test_id=active_test_id,
        second_test_id=second_test_id,
        essay_test_id=essay_test_id,
        archived_test_id=archived_test_id,
        empty_attempt_id=empty_attempt_id,
        partial_attempt_id=partial_attempt_id,
        high_attempt_id=high_attempt_id,
        questions_by_test={
            active_test_id: DatabaseManager(str(db_path)).get_questions_for_test(
                active_test_id
            ),
            second_test_id: DatabaseManager(str(db_path)).get_questions_for_test(
                second_test_id
            ),
            essay_test_id: DatabaseManager(str(db_path)).get_questions_for_test(
                essay_test_id
            ),
            archived_test_id: DatabaseManager(str(db_path)).get_questions_for_test(
                archived_test_id
            ),
        },
    )


def settings_test(name: str, description: str, group_name: str):
    """Create a Test model without importing it at module top for readability."""
    from models.test import Test

    return Test(name=name, description=description, group_name=group_name)


def create_results_session(seed: SeedData) -> tuple[TestSession, dict]:
    """Create an unsaved session with flagged, incorrect, and essay responses."""
    questions = seed.questions_by_test[seed.active_test_id]
    session = TestSession(seed.active_test_id, questions, mode=MODE_TEST)
    session.start()
    session.save_response(questions[0].id, "Normal jugular venous pressure")
    session.save_response(questions[1].id, "CHA2DS2-VASc")
    session.save_response(questions[2].id, "Increased distal sodium delivery.")
    session.flag_question(questions[0].id)
    score_data = ScoringService(str(seed.db_path)).score_test(session)
    score_data["time_taken"] = 540
    return session, score_data


def create_all_correct_results_session(seed: SeedData) -> tuple[TestSession, dict]:
    """Create an unsaved all-correct multiple-choice results session."""
    questions = seed.questions_by_test[seed.second_test_id]
    session = TestSession(seed.second_test_id, questions, mode=MODE_TEST)
    session.start()
    for question in questions:
        session.save_response(question.id, question.correct_answer)
    score_data = ScoringService(str(seed.db_path)).score_test(session)
    score_data["time_taken"] = 126
    return session, score_data


def create_missing_answer_results_session(seed: SeedData) -> tuple[TestSession, dict]:
    """Create an unsaved results session with a missing multiple-choice answer."""
    questions = seed.questions_by_test[seed.active_test_id]
    session = TestSession(seed.active_test_id, questions, mode=MODE_TEST)
    session.start()
    session.save_response(questions[1].id, questions[1].correct_answer)
    session.save_response(questions[2].id, "Loop diuretics increase distal sodium.")
    score_data = ScoringService(str(seed.db_path)).score_test(session)
    score_data["time_taken"] = 390
    return session, score_data


def create_mix_results_session(seed: SeedData) -> tuple[TestSession, dict]:
    """Create an unsaved mixed-test results session with source breakdown."""
    questions = create_mix_questions(seed)
    session = TestSession(
        None,
        questions,
        mode=MODE_TEST,
        mix_name="Mixed Clinical Drill",
        mix_subtitle="4 questions from 2 tests",
    )
    session.start()
    for index, question in enumerate(questions):
        if index == 1 and question.options:
            wrong = next(
                option.text
                for option in question.options
                if option.text != question.correct_answer
            )
            session.save_response(question.id, wrong)
        else:
            session.save_response(question.id, question.correct_answer)
    session.flag_question(questions[1].id)
    score_data = ScoringService(str(seed.db_path)).score_test(session)
    score_data["time_taken"] = 480
    return session, score_data


def create_mix_questions(seed: SeedData) -> List[Question]:
    """Return questions from one group for mix-test screenshots."""
    return (
        seed.questions_by_test[seed.active_test_id][:2]
        + seed.questions_by_test[seed.second_test_id][:2]
    )


def create_partial_group_mix_questions(seed: SeedData) -> List[Question]:
    """Return questions from part of one group for mix-test screenshots."""
    return seed.questions_by_test[seed.active_test_id][:2]


def create_multi_group_mix_questions(seed: SeedData) -> List[Question]:
    """Return questions from three group buckets for mix-test screenshots."""
    return (
        seed.questions_by_test[seed.active_test_id][:1]
        + seed.questions_by_test[seed.essay_test_id][:1]
        + seed.questions_by_test[seed.archived_test_id][:1]
    )


def capture_dialog(
    app: App,
    harness: ScreenshotHarness,
    factory: Callable[[], ctk.CTkToplevel],
) -> Callable[[], None]:
    """Open a CTk dialog and return a cleanup callback."""
    dialog = factory()
    app.update_idletasks()
    app.update()

    def cleanup() -> None:
        dialog.destroy()
        app.update_idletasks()
        app.update()

    return cleanup


def show_home(app: App, seed: Optional[SeedData], harness: ScreenshotHarness) -> None:
    """Show the populated home screen."""
    harness.show_frame(SCREEN_HOME)


def ensure_zero_question_home_test(seed: Optional[SeedData]) -> None:
    """Add the STORY-005-only zero-question test fixture if missing."""
    if seed is None:
        return
    db = DatabaseManager(str(seed.db_path))
    if any(test.name == "Empty Intake Template" for test in db.get_all_tests()):
        return
    db.create_test(
        settings_test(
            "Empty Intake Template",
            "Newly created test with no questions yet.",
            "Clinical Medicine",
        )
    )


def ensure_no_missed_review_test(seed: Optional[SeedData]) -> Optional[int]:
    """Add a review fixture with active questions and no missed responses."""
    if seed is None:
        return None
    db = DatabaseManager(str(seed.db_path))
    for test in db.get_all_tests():
        if test.name == "Clean Review Check":
            return test.id
    test_id = db.create_test(
        settings_test(
            "Clean Review Check",
            "Active test with questions but no missed attempts.",
            "Clinical Medicine",
        )
    )
    add_question(
        db,
        test_id,
        "Which review scope should stay empty when no attempts are missed?",
        "Clean review scope",
        "Review",
        ["Clean review scope", "Archived review scope", "Mixed review scope"],
    )
    return test_id


def clear_question_categories(seed: Optional[SeedData]) -> None:
    """Remove question category tags from a seeded database."""
    if seed is None:
        return
    conn = database_config.get_connection(str(seed.db_path))
    try:
        conn.execute("UPDATE questions SET category = ''")
        conn.commit()
    finally:
        conn.close()


def show_home_expanded_cards(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show expanded Home groups with active card actions visible."""
    ensure_zero_question_home_test(seed)
    harness.show_frame(SCREEN_HOME)
    frame = app.frames[SCREEN_HOME]
    for group_widget in frame._group_widgets.values():
        if not group_widget.is_expanded:
            group_widget.toggle()
    frame._collapse_all_btn.configure(text="Collapse All")
    harness._settle()


def show_home_expanded_archived_cards(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show expanded Home groups scrolled to archived card actions."""
    show_home_expanded_cards(app, seed, harness)
    frame = app.frames[SCREEN_HOME]
    frame.test_list_frame._parent_canvas.yview_moveto(1.0)
    harness._settle()


def show_mode_dialog(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> Callable[[], None]:
    """Show the mode selection dialog."""
    harness.show_frame(SCREEN_HOME)
    return capture_dialog(app, harness, lambda: ModeSelectionDialog(app))


def mix_dialog_tests_with_counts(seed: SeedData) -> list:
    """Return seeded test/count tuples for Mix Test dialog captures."""
    tests_with_counts = [
        (DatabaseManager(str(seed.db_path)).get_test_by_id(seed.active_test_id), 3),
        (DatabaseManager(str(seed.db_path)).get_test_by_id(seed.second_test_id), 2),
        (DatabaseManager(str(seed.db_path)).get_test_by_id(seed.essay_test_id), 1),
    ]
    return tests_with_counts


def capture_mix_dialog_state(
    app: App,
    seed: Optional[SeedData],
    harness: ScreenshotHarness,
    configure: Optional[Callable] = None,
) -> Callable[[], None]:
    """Open the Mix Test dialog and apply an optional capture-state action."""
    if seed is None:
        raise RuntimeError("Mix Test dialog captures require seeded data.")
    harness.show_frame(SCREEN_HOME)
    dialog = MixTestDialog(app, mix_dialog_tests_with_counts(seed))
    if configure is not None:
        configure(dialog)
    app.update_idletasks()
    app.update()

    def cleanup() -> None:
        dialog.destroy()
        app.update_idletasks()
        app.update()

    return cleanup


def show_mix_dialog(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> Callable[[], None]:
    """Show the mix-test dialog with no selected tests."""
    return capture_mix_dialog_state(app, seed, harness)


def show_mix_dialog_select_all(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> Callable[[], None]:
    """Show the mix-test dialog after Select All."""
    return capture_mix_dialog_state(
        app,
        seed,
        harness,
        lambda dialog: dialog._select_all(),
    )


def show_mix_dialog_group_selected(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> Callable[[], None]:
    """Show the mix-test dialog with one source group selected."""

    def configure(dialog) -> None:
        group_name = next(iter(dialog._group_vars))
        dialog._group_vars[group_name].set(True)
        dialog._on_group_toggled(group_name)

    return capture_mix_dialog_state(app, seed, harness, configure)


def show_mix_dialog_deselected(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> Callable[[], None]:
    """Show the mix-test dialog after Select All then Deselect All."""

    def configure(dialog) -> None:
        dialog._select_all()
        dialog._deselect_all()

    return capture_mix_dialog_state(app, seed, harness, configure)


def show_editor_new(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show the new-test editor state."""
    harness.show_frame(SCREEN_EDITOR, test_id=None)


def show_editor_existing(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show the existing-test editor state."""
    harness.show_frame(SCREEN_EDITOR, test_id=seed.active_test_id)


def get_or_create_empty_editor_test_id(seed: SeedData) -> int:
    """Return a saved test with no questions for editor empty-state capture."""
    db = DatabaseManager(str(seed.db_path))
    for test in db.get_all_tests():
        if test.name == "Saved Empty Editor Test":
            return test.id
    return db.create_test(
        settings_test(
            "Saved Empty Editor Test",
            "Saved metadata with no questions yet.",
            "Clinical Medicine",
        )
    )


def show_editor_saved_empty(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show a saved editor test with no questions."""
    test_id = get_or_create_empty_editor_test_id(seed)
    harness.show_frame(SCREEN_EDITOR, test_id=test_id)


def show_editor_mc_add_form(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show the editor multiple-choice add form."""
    harness.show_frame(SCREEN_EDITOR, test_id=seed.active_test_id)
    frame = app.frames[SCREEN_EDITOR]
    frame.form_scroll._parent_canvas.yview_moveto(0.45)
    harness._settle()


def show_editor_essay_add_form(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show the editor essay add form."""
    harness.show_frame(SCREEN_EDITOR, test_id=seed.active_test_id)
    frame = app.frames[SCREEN_EDITOR]
    frame.type_selector.set("Essay")
    frame._on_type_change("Essay")
    frame.form_scroll._parent_canvas.yview_moveto(0.55)
    harness._settle()


def show_editor_edit_question(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show editor edit-question mode."""
    harness.show_frame(SCREEN_EDITOR, test_id=seed.active_test_id)
    frame = app.frames[SCREEN_EDITOR]
    question = seed.questions_by_test[seed.active_test_id][0]
    frame._on_edit_question(question)
    frame.form_scroll._parent_canvas.yview_moveto(1.0)
    harness._settle()


def show_editor_group_autocomplete(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> Callable[[], None]:
    """Show the editor group autocomplete dropdown."""
    harness.show_frame(SCREEN_EDITOR, test_id=seed.active_test_id)
    frame = app.frames[SCREEN_EDITOR]
    frame.group_entry.delete(0, "end")
    frame.group_entry._entry.focus_force()
    frame.group_entry._show_dropdown()
    harness._settle()

    def cleanup() -> None:
        frame.group_entry._close_dropdown()
        harness._settle()

    return cleanup


def show_editor_minimum_existing(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show the editor at the documented minimum window size."""
    harness.use_minimum_geometry()
    harness.show_frame(SCREEN_EDITOR, test_id=seed.active_test_id)


def show_test_unanswered(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show an unanswered test-taking question."""
    harness.show_frame(SCREEN_TEST_TAKING, test_id=seed.active_test_id, mode=MODE_TEST)


def go_to_first_question_type(frame, question_type: str) -> Question:
    """Move the active session to the first question of the requested type."""
    for index, question in enumerate(frame._session.questions):
        if question.type == question_type:
            frame._session.go_to_question(index)
            frame._display_question()
            return question
    raise RuntimeError(f"No {question_type} question available in seeded test.")


def option_answer(question: Question, correct: bool) -> str:
    """Return a correct or incorrect option text for a multiple-choice question."""
    if correct:
        return question.correct_answer
    for option in question.options:
        if option.text != question.correct_answer:
            return option.text
    return ""


def show_test_answered_flagged(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show an answered and flagged test-taking question."""
    harness.show_frame(SCREEN_TEST_TAKING, test_id=seed.active_test_id, mode=MODE_TEST)
    frame = app.frames[SCREEN_TEST_TAKING]
    question = go_to_first_question_type(frame, settings.QUESTION_TYPE_MC)
    frame._question_widget.set_answer(option_answer(question, correct=True))
    frame._save_current_answer()
    frame._session.flag_question(question.id)
    frame._display_question()


def show_test_selected_answer(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show a selected but unchecked multiple-choice answer row."""
    harness.show_frame(SCREEN_TEST_TAKING, test_id=seed.active_test_id, mode=MODE_TEST)
    frame = app.frames[SCREEN_TEST_TAKING]
    question = go_to_first_question_type(frame, settings.QUESTION_TYPE_MC)
    frame._question_widget.set_answer(option_answer(question, correct=True))


def show_test_middle_question(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show a middle test-taking question with both nav buttons enabled."""
    harness.show_frame(SCREEN_TEST_TAKING, test_id=seed.active_test_id, mode=MODE_TEST)
    frame = app.frames[SCREEN_TEST_TAKING]
    frame._session.go_to_question(1)
    frame._display_question()


def show_test_last_question(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show the final test-taking question with Next disabled."""
    harness.show_frame(SCREEN_TEST_TAKING, test_id=seed.active_test_id, mode=MODE_TEST)
    frame = app.frames[SCREEN_TEST_TAKING]
    frame._session.go_to_question(frame._session.total_questions - 1)
    frame._display_question()


def show_test_review_session(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show the test-taking shell for a review session."""
    question_ids = [
        question.id for question in seed.questions_by_test[seed.active_test_id][:2]
    ]
    harness.show_frame(
        SCREEN_TEST_TAKING,
        test_id=seed.active_test_id,
        mode=MODE_TEST,
        review_question_ids=question_ids,
    )


def show_test_minimum_unanswered(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show the normal test-taking shell at minimum window size."""
    harness.use_minimum_geometry()
    harness.show_frame(SCREEN_TEST_TAKING, test_id=seed.active_test_id, mode=MODE_TEST)


def show_practice_feedback(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show practice-mode incorrect feedback."""
    harness.show_frame(
        SCREEN_TEST_TAKING, test_id=seed.active_test_id, mode=MODE_PRACTICE
    )
    frame = app.frames[SCREEN_TEST_TAKING]
    question = go_to_first_question_type(frame, settings.QUESTION_TYPE_MC)
    frame._question_widget.set_answer(option_answer(question, correct=False))
    frame._on_check_answer()


def show_practice_correct_feedback(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show practice-mode correct feedback."""
    harness.show_frame(
        SCREEN_TEST_TAKING, test_id=seed.active_test_id, mode=MODE_PRACTICE
    )
    frame = app.frames[SCREEN_TEST_TAKING]
    question = go_to_first_question_type(frame, settings.QUESTION_TYPE_MC)
    frame._question_widget.set_answer(option_answer(question, correct=True))
    frame._on_check_answer()


def show_practice_checked_return(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show a checked answer after navigating away and back."""
    harness.show_frame(
        SCREEN_TEST_TAKING, test_id=seed.active_test_id, mode=MODE_PRACTICE
    )
    frame = app.frames[SCREEN_TEST_TAKING]
    question = go_to_first_question_type(frame, settings.QUESTION_TYPE_MC)
    frame._question_widget.set_answer(option_answer(question, correct=False))
    frame._on_check_answer()
    frame._on_next()
    frame._on_previous()
    frame.question_area._parent_canvas.yview_moveto(0.0)
    harness._settle()


def show_essay_question(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show an essay question in the test-taking screen."""
    harness.show_frame(SCREEN_TEST_TAKING, test_id=seed.active_test_id, mode=MODE_TEST)
    frame = app.frames[SCREEN_TEST_TAKING]
    essay_index = next(
        index
        for index, question in enumerate(frame._session.questions)
        if question.type == settings.QUESTION_TYPE_ESSAY
    )
    frame._session.go_to_question(essay_index)
    frame._display_question()


def show_essay_input(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show a typed essay answer in the test-taking screen."""
    harness.show_frame(SCREEN_TEST_TAKING, test_id=seed.active_test_id, mode=MODE_TEST)
    frame = app.frames[SCREEN_TEST_TAKING]
    go_to_first_question_type(frame, settings.QUESTION_TYPE_ESSAY)
    frame._question_widget.set_answer(
        "Loop diuretics increase distal sodium delivery and potassium secretion."
    )


def show_essay_feedback(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show practice-mode expected-answer feedback for an essay question."""
    harness.show_frame(
        SCREEN_TEST_TAKING, test_id=seed.essay_test_id, mode=MODE_PRACTICE
    )
    frame = app.frames[SCREEN_TEST_TAKING]
    go_to_first_question_type(frame, settings.QUESTION_TYPE_ESSAY)
    frame._question_widget.set_answer(
        "Preload is ventricular filling and afterload is resistance to ejection."
    )
    frame._on_check_answer()


def show_mix_session(
    seed: SeedData,
    harness: ScreenshotHarness,
    test_ids: List[int],
    questions: List[Question],
) -> None:
    """Show a mixed test-taking session with generated display metadata."""
    db = DatabaseManager(str(seed.db_path))
    selected_tests = [db.get_test_by_id(test_id) for test_id in test_ids]
    selected_tests = [test for test in selected_tests if test is not None]
    available_test_ids = [
        seed.active_test_id,
        seed.second_test_id,
        seed.essay_test_id,
        seed.archived_test_id,
    ]
    available_tests = [db.get_test_by_id(test_id) for test_id in available_test_ids]
    all_tests_with_counts = [
        (test, db.get_question_count(test.id))
        for test in available_tests
        if test is not None
    ]
    mix_display = build_mix_test_display(
        selected_tests,
        all_tests_with_counts,
        len(questions),
    )
    harness.show_frame(
        SCREEN_TEST_TAKING,
        mode=MODE_TEST,
        questions=questions,
        mix_test_name=mix_display.title,
        mix_test_subtitle=mix_display.subtitle,
    )


def show_mix_test(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show a mixed test-taking session from one complete group."""
    show_mix_session(
        seed,
        harness,
        [seed.active_test_id, seed.second_test_id],
        create_mix_questions(seed),
    )


def show_mix_partial_group(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show a mixed test-taking session from part of one group."""
    show_mix_session(
        seed,
        harness,
        [seed.active_test_id],
        create_partial_group_mix_questions(seed),
    )


def show_mix_multi_group(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show a mixed test-taking session from three group buckets."""
    show_mix_session(
        seed,
        harness,
        [seed.active_test_id, seed.essay_test_id, seed.archived_test_id],
        create_multi_group_mix_questions(seed),
    )


def show_results_session(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show just-completed results with partial score, essay, and flag data."""
    session, score_data = create_results_session(seed)
    harness.show_frame(SCREEN_RESULTS, session=session, score_data=score_data)


def show_results_all_correct(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show all-correct multiple-choice results."""
    session, score_data = create_all_correct_results_session(seed)
    harness.show_frame(SCREEN_RESULTS, session=session, score_data=score_data)


def show_results_essay_review(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show the essay review card in a partial results session."""
    session, score_data = create_results_session(seed)
    harness.show_frame(SCREEN_RESULTS, session=session, score_data=score_data)
    frame = app.frames[SCREEN_RESULTS]
    frame.review_frame._parent_canvas.yview_moveto(1.0)
    harness._settle()


def show_results_missing_answer(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show results with an unanswered multiple-choice question."""
    session, score_data = create_missing_answer_results_session(seed)
    harness.show_frame(SCREEN_RESULTS, session=session, score_data=score_data)


def show_results_mix_breakdown(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show live mixed-test results with source breakdown."""
    session, score_data = create_mix_results_session(seed)
    harness.show_frame(SCREEN_RESULTS, session=session, score_data=score_data)
    frame = app.frames[SCREEN_RESULTS]
    frame.review_frame._parent_canvas.yview_moveto(1.0)
    harness._settle()


def show_results_history(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show results loaded from persisted history."""
    harness.show_frame(SCREEN_RESULTS, attempt_id=seed.partial_attempt_id)


def show_history(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show history with data loaded synchronously."""
    harness.show_history_sync()
    frame = app.frames[SCREEN_HISTORY]
    frame.filter_var.set("All Tests")
    frame.mode_filter_var.set("All Modes")
    frame._apply_filters()
    harness._settle()


def show_history_filtered(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show history filtered to one practice-mode test."""
    harness.show_history_sync()
    frame = app.frames[SCREEN_HISTORY]
    frame.filter_var.set("Pharmacology Quick Drill")
    frame.mode_filter_var.set("Practice")
    frame._apply_filters()
    harness._settle()


def show_history_loading(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show the designed history loading state."""
    app._current_screen = SCREEN_HISTORY
    frame = app.frames[SCREEN_HISTORY]
    frame.tkraise()
    frame.filter_var.set("All Tests")
    frame.mode_filter_var.set("All Modes")
    frame._show_loading_state()
    harness._settle()


def show_history_minimum_populated(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show populated History at the documented minimum window size."""
    harness.use_minimum_geometry()
    harness.show_history_sync()
    frame = app.frames[SCREEN_HISTORY]
    frame.filter_var.set("All Tests")
    frame.mode_filter_var.set("All Modes")
    frame._apply_filters()
    harness._settle()


def show_analytics(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show analytics with populated data."""
    harness.show_frame(SCREEN_ANALYTICS)


def show_analytics_test_comparison(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show Analytics Test Comparison chart tab."""
    harness.show_frame(SCREEN_ANALYTICS)
    frame = app.frames[SCREEN_ANALYTICS]
    frame.tab_var.set("Test Comparison")
    frame._render_current_tab()
    harness._settle()


def show_analytics_study_activity(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show Analytics Study Activity chart tab."""
    harness.show_frame(SCREEN_ANALYTICS)
    frame = app.frames[SCREEN_ANALYTICS]
    frame.tab_var.set("Study Activity")
    frame._render_current_tab()
    harness._settle()


def show_analytics_minimum_score_trends(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show Analytics Score Trends at the documented minimum window size."""
    harness.use_minimum_geometry()
    harness.show_frame(SCREEN_ANALYTICS)


def show_analytics_weak_topics_group(
    app: App,
    harness: ScreenshotHarness,
    group_by: str,
) -> None:
    """Show Analytics Weak Topics for one grouping mode."""
    harness.show_frame(SCREEN_ANALYTICS)
    frame = app.frames[SCREEN_ANALYTICS]
    frame.tab_var.set("Weak Topics")
    frame.group_by_var.set(group_by)
    frame._render_current_tab()
    harness._settle()


def show_analytics_weak_topics_test(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show Analytics Weak Topics grouped by Test."""
    show_analytics_weak_topics_group(app, harness, "Test")


def show_analytics_weak_topics_grouped(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show Analytics Weak Topics grouped by Group."""
    show_analytics_weak_topics_group(app, harness, "Group")


def show_analytics_weak_topics_category(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show Analytics Weak Topics grouped by Category."""
    show_analytics_weak_topics_group(app, harness, "Category")


def show_analytics_weak_topics_no_category(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show Analytics Weak Topics category grouping with no tagged categories."""
    show_analytics_weak_topics_group(app, harness, "Category")


def show_analytics_weak_topics_minimum(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show Analytics Weak Topics at the documented minimum window size."""
    harness.use_minimum_geometry()
    show_analytics_weak_topics_group(app, harness, "Test")


def show_review(app: App, seed: Optional[SeedData], harness: ScreenshotHarness) -> None:
    """Show missed-question review."""
    harness.show_frame(SCREEN_REVIEW)


def set_review_scope(frame, selected_test_ids: Sequence[int]) -> None:
    """Select a specific test scope in the Review screen."""
    selected = set(selected_test_ids)
    for test_id, var in frame._test_scope_vars.items():
        var.set(test_id in selected)
    for group_name, test_ids in frame._group_to_test_ids.items():
        frame._group_scope_vars[group_name].set(
            bool(test_ids) and all(test_id in selected for test_id in test_ids)
        )
    frame._load_questions()


def show_review_selected_scope(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show Review scoped to one selected test."""
    harness.show_frame(SCREEN_REVIEW)
    frame = app.frames[SCREEN_REVIEW]
    selected_id = (
        seed.active_test_id if seed else next(iter(frame._test_scope_vars), None)
    )
    if selected_id is not None:
        set_review_scope(frame, [selected_id])
    harness._settle()


def show_review_selected_questions(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show Review with one missed question selected."""
    harness.show_frame(SCREEN_REVIEW)
    frame = app.frames[SCREEN_REVIEW]
    if frame._checkboxes:
        first_var = next(iter(frame._checkboxes.values()))
        first_var.set(True)
        frame._update_selected_count()
    harness._settle()


def show_review_no_selected_tests(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show Review with every scope checkbox cleared."""
    harness.show_frame(SCREEN_REVIEW)
    frame = app.frames[SCREEN_REVIEW]
    frame._deselect_all_scope()
    harness._settle()


def show_review_no_missed_questions(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show Review scoped to an active test with no missed questions."""
    clean_test_id = ensure_no_missed_review_test(seed)
    harness.show_frame(SCREEN_REVIEW)
    frame = app.frames[SCREEN_REVIEW]
    if clean_test_id is not None:
        set_review_scope(frame, [clean_test_id])
    harness._settle()


def show_review_minimum_missed_questions(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show Review missed questions at the documented minimum window size."""
    harness.use_minimum_geometry()
    harness.show_frame(SCREEN_REVIEW)


def show_empty_home(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show the empty home state."""
    harness.show_frame(SCREEN_HOME)


def show_home_minimum_populated(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show populated Home at the documented minimum window size."""
    harness.use_minimum_geometry()
    harness.show_frame(SCREEN_HOME)
    frame = app.frames[SCREEN_HOME]
    frame.test_list_frame._parent_canvas.yview_moveto(0.0)
    harness._settle()


def show_home_minimum_empty(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show empty Home at the documented minimum window size."""
    harness.use_minimum_geometry()
    harness.show_frame(SCREEN_HOME)


def show_empty_history(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show the empty history state."""
    harness.show_history_sync()


def show_empty_analytics(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show the analytics no-data state."""
    harness.show_frame(SCREEN_ANALYTICS)


def show_empty_analytics_weak_topics(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show the analytics Weak Topics no-data state."""
    show_analytics_weak_topics_group(app, harness, "Test")


def show_empty_review(
    app: App, seed: Optional[SeedData], harness: ScreenshotHarness
) -> None:
    """Show the empty review state."""
    harness.show_frame(SCREEN_REVIEW)


CAPTURE_STATES = [
    CaptureState("home_populated_grouped", "home", "seeded", show_home),
    CaptureState("home_expanded_cards", "home", "seeded", show_home_expanded_cards),
    CaptureState(
        "home_expanded_archived_cards",
        "home",
        "seeded",
        show_home_expanded_archived_cards,
    ),
    CaptureState(
        "home_minimum_populated",
        "home",
        "seeded",
        show_home_minimum_populated,
    ),
    CaptureState("mode_selection_dialog", "dialogs", "seeded", show_mode_dialog),
    CaptureState("mix_test_dialog", "dialogs", "seeded", show_mix_dialog),
    CaptureState(
        "mix_test_dialog_select_all",
        "dialogs",
        "seeded",
        show_mix_dialog_select_all,
    ),
    CaptureState(
        "mix_test_dialog_group_selected",
        "dialogs",
        "seeded",
        show_mix_dialog_group_selected,
    ),
    CaptureState(
        "mix_test_dialog_deselected",
        "dialogs",
        "seeded",
        show_mix_dialog_deselected,
    ),
    CaptureState("editor_new_test", "editor", "seeded", show_editor_new),
    CaptureState(
        "editor_existing_test_with_questions",
        "editor",
        "seeded",
        show_editor_existing,
    ),
    CaptureState(
        "editor_saved_empty_test",
        "editor",
        "seeded",
        show_editor_saved_empty,
    ),
    CaptureState(
        "editor_mc_add_form",
        "editor",
        "seeded",
        show_editor_mc_add_form,
    ),
    CaptureState(
        "editor_essay_add_form",
        "editor",
        "seeded",
        show_editor_essay_add_form,
    ),
    CaptureState(
        "editor_edit_question",
        "editor",
        "seeded",
        show_editor_edit_question,
    ),
    CaptureState(
        "editor_group_autocomplete",
        "editor",
        "seeded",
        show_editor_group_autocomplete,
    ),
    CaptureState(
        "editor_minimum_existing",
        "editor",
        "seeded",
        show_editor_minimum_existing,
    ),
    CaptureState(
        "test_taking_unanswered", "test-taking", "seeded", show_test_unanswered
    ),
    CaptureState(
        "test_taking_answered_flagged",
        "test-taking",
        "seeded",
        show_test_answered_flagged,
    ),
    CaptureState(
        "test_taking_selected_answer",
        "test-taking",
        "seeded",
        show_test_selected_answer,
    ),
    CaptureState(
        "test_taking_middle_question",
        "test-taking",
        "seeded",
        show_test_middle_question,
    ),
    CaptureState(
        "test_taking_last_question",
        "test-taking",
        "seeded",
        show_test_last_question,
    ),
    CaptureState(
        "test_taking_review_session",
        "test-taking",
        "seeded",
        show_test_review_session,
    ),
    CaptureState(
        "test_taking_minimum_unanswered",
        "test-taking",
        "seeded",
        show_test_minimum_unanswered,
    ),
    CaptureState(
        "test_taking_practice_incorrect_feedback",
        "test-taking",
        "seeded",
        show_practice_feedback,
    ),
    CaptureState(
        "test_taking_practice_correct_feedback",
        "test-taking",
        "seeded",
        show_practice_correct_feedback,
    ),
    CaptureState(
        "test_taking_practice_checked_return",
        "test-taking",
        "seeded",
        show_practice_checked_return,
    ),
    CaptureState(
        "test_taking_essay_question", "test-taking", "seeded", show_essay_question
    ),
    CaptureState("test_taking_essay_input", "test-taking", "seeded", show_essay_input),
    CaptureState(
        "test_taking_essay_feedback",
        "test-taking",
        "seeded",
        show_essay_feedback,
    ),
    CaptureState("test_taking_mix_test", "test-taking", "seeded", show_mix_test),
    CaptureState(
        "test_taking_mix_partial_group",
        "test-taking",
        "seeded",
        show_mix_partial_group,
    ),
    CaptureState(
        "test_taking_mix_multi_group",
        "test-taking",
        "seeded",
        show_mix_multi_group,
    ),
    CaptureState(
        "results_partial_score_essay_flagged",
        "results",
        "seeded",
        show_results_session,
    ),
    CaptureState(
        "results_all_correct",
        "results",
        "seeded",
        show_results_all_correct,
    ),
    CaptureState(
        "results_essay_review",
        "results",
        "seeded",
        show_results_essay_review,
    ),
    CaptureState(
        "results_missing_answer",
        "results",
        "seeded",
        show_results_missing_answer,
    ),
    CaptureState(
        "results_mix_breakdown",
        "results",
        "seeded",
        show_results_mix_breakdown,
    ),
    CaptureState(
        "results_loaded_from_history", "results", "seeded", show_results_history
    ),
    CaptureState("history_populated", "data", "seeded", show_history),
    CaptureState("history_filtered", "data", "seeded", show_history_filtered),
    CaptureState("history_loading_state", "data", "seeded", show_history_loading),
    CaptureState(
        "history_minimum_populated",
        "data",
        "seeded",
        show_history_minimum_populated,
    ),
    CaptureState("analytics_populated", "data", "seeded", show_analytics),
    CaptureState(
        "analytics_test_comparison",
        "data",
        "seeded",
        show_analytics_test_comparison,
    ),
    CaptureState(
        "analytics_study_activity",
        "data",
        "seeded",
        show_analytics_study_activity,
    ),
    CaptureState(
        "analytics_minimum_score_trends",
        "data",
        "seeded",
        show_analytics_minimum_score_trends,
    ),
    CaptureState(
        "analytics_weak_topics_test",
        "data",
        "seeded",
        show_analytics_weak_topics_test,
    ),
    CaptureState(
        "analytics_weak_topics_group",
        "data",
        "seeded",
        show_analytics_weak_topics_grouped,
    ),
    CaptureState(
        "analytics_weak_topics_category",
        "data",
        "seeded",
        show_analytics_weak_topics_category,
    ),
    CaptureState(
        "analytics_weak_topics_minimum",
        "data",
        "seeded",
        show_analytics_weak_topics_minimum,
    ),
    CaptureState(
        "analytics_weak_topics_no_category",
        "data",
        "no_category",
        show_analytics_weak_topics_no_category,
    ),
    CaptureState("review_missed_questions", "data", "seeded", show_review),
    CaptureState(
        "review_selected_scope",
        "data",
        "seeded",
        show_review_selected_scope,
    ),
    CaptureState(
        "review_selected_questions",
        "data",
        "seeded",
        show_review_selected_questions,
    ),
    CaptureState(
        "review_no_selected_tests",
        "data",
        "seeded",
        show_review_no_selected_tests,
    ),
    CaptureState(
        "review_no_missed_questions",
        "data",
        "seeded",
        show_review_no_missed_questions,
    ),
    CaptureState(
        "review_minimum_missed_questions",
        "data",
        "seeded",
        show_review_minimum_missed_questions,
    ),
    CaptureState("home_empty_state", "empty", "empty", show_empty_home),
    CaptureState(
        "home_minimum_empty",
        "empty",
        "empty",
        show_home_minimum_empty,
    ),
    CaptureState("history_empty_state", "empty", "empty", show_empty_history),
    CaptureState("analytics_no_data", "empty", "empty", show_empty_analytics),
    CaptureState(
        "analytics_weak_topics_no_data",
        "empty",
        "empty",
        show_empty_analytics_weak_topics,
    ),
    CaptureState("review_empty_state", "empty", "empty", show_empty_review),
]


def selected_capture_states(args: argparse.Namespace) -> List[CaptureState]:
    """Return states selected by --states or --group."""
    if args.states:
        known = {state.name: state for state in CAPTURE_STATES}
        missing = sorted(set(args.states) - set(known))
        if missing:
            raise SystemExit(f"Unknown capture state(s): {', '.join(missing)}")
        return [known[name] for name in args.states]
    if args.group == "all":
        return list(CAPTURE_STATES)
    return [state for state in CAPTURE_STATES if state.group == args.group]


def capture_state_group(
    app: App,
    seed: Optional[SeedData],
    harness: ScreenshotHarness,
    states: Sequence[CaptureState],
) -> None:
    """Capture states for one database source."""
    for state in states:
        harness.use_default_geometry()
        cleanup = state.action(app, seed, harness)
        try:
            harness.capture(state.name)
        finally:
            if cleanup is not None:
                cleanup()


def create_app(mode: str) -> App:
    """Create the app and force the requested appearance mode."""
    if ctk is None:
        raise RuntimeError("customtkinter is required for capture.")
    app = App()
    ctk.set_appearance_mode(mode)
    app.geometry(f"{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}+80+80")
    app.update_idletasks()
    app.update()
    return app


def selected_modes(mode: str) -> List[str]:
    """Expand a mode argument into concrete appearance modes."""
    return ["light", "dark"] if mode == "both" else [mode]


def expected_screenshot_paths(
    output_dir: Path,
    modes: Sequence[str],
    states: Sequence[CaptureState],
) -> List[Path]:
    """Return expected screenshot paths for modes and states."""
    return [
        output_dir / mode / f"{mode}_{state.name}.png"
        for mode in modes
        for state in states
    ]


def validate_screenshot(path: Path) -> ValidationResult:
    """Validate one screenshot file."""
    if not path.exists():
        return ValidationResult(path, False, "missing")

    try:
        with Image.open(path) as image:
            image = image.convert("RGB")
            width, height = image.size
            if width < 760 or height < 560:
                return ValidationResult(path, False, f"too small: {width}x{height}")

            stat = ImageStat.Stat(image)
            if max(stat.stddev) < 2.0:
                return ValidationResult(path, False, "near-uniform image")

            if looks_desktop_only(image):
                return ValidationResult(path, False, "looks like desktop-only capture")
    except Exception as exc:
        return ValidationResult(path, False, f"unreadable: {exc}")

    return ValidationResult(path, True)


def looks_desktop_only(image: Image.Image) -> bool:
    """Heuristically detect wallpaper-only captures."""
    sample = image.resize((80, 80))
    if hasattr(sample, "get_flattened_data"):
        pixels = list(sample.get_flattened_data())
    else:
        pixels = list(sample.getdata())
    saturated_purple_blue = 0
    neutral = 0

    for red, green, blue in pixels:
        hue, saturation, value = colorsys.rgb_to_hsv(
            red / 255,
            green / 255,
            blue / 255,
        )
        hue_degrees = hue * 360
        if 220 <= hue_degrees <= 320 and saturation > 0.45 and value > 0.2:
            saturated_purple_blue += 1
        if saturation < 0.18 and value > 0.08:
            neutral += 1

    total = len(pixels)
    return saturated_purple_blue / total > 0.55 and neutral / total < 0.12


def validate_screenshots(paths: Sequence[Path]) -> bool:
    """Validate screenshot files and print a concise summary."""
    results = [validate_screenshot(path) for path in paths]
    failures = [result for result in results if not result.ok]

    if failures:
        print(f"validation failed: {len(failures)} of {len(results)} file(s)")
        for failure in failures:
            try:
                rel_path = failure.path.relative_to(REPO_ROOT)
            except ValueError:
                rel_path = failure.path
            print(f"- {rel_path}: {failure.reason}")
        return False

    print(f"validation passed: {len(results)} screenshot(s)")
    return True


def run_capture(args: argparse.Namespace) -> None:
    """Seed data, launch the app, and capture requested states."""
    tmp_dir = Path(tempfile.mkdtemp(prefix="study-test-tool-visual-"))
    db_path = tmp_dir / "visual_seed.db"
    modes = selected_modes(args.mode)
    states = selected_capture_states(args)
    seeded_states = [state for state in states if state.source == "seeded"]
    no_category_states = [state for state in states if state.source == "no_category"]
    empty_states = [state for state in states if state.source == "empty"]
    expected_paths = expected_screenshot_paths(args.output, modes, states)

    if args.validate_only:
        if not validate_screenshots(expected_paths):
            raise SystemExit(1)
        return

    ensure_gui_modules()

    app = None
    try:
        for mode in modes:
            if seeded_states:
                seed = seed_database(db_path)
                app = create_app(mode)
                harness = ScreenshotHarness(app, args.output, mode)
                capture_state_group(app, seed, harness, seeded_states)
                app.destroy()
                app = None

            if no_category_states:
                no_category_db_path = tmp_dir / f"visual_no_category_{mode}.db"
                seed = seed_database(no_category_db_path)
                clear_question_categories(seed)
                app = create_app(mode)
                harness = ScreenshotHarness(app, args.output, mode)
                capture_state_group(app, seed, harness, no_category_states)
                app.destroy()
                app = None

            if empty_states:
                empty_db_path = tmp_dir / f"visual_empty_{mode}.db"
                configure_database(empty_db_path)
                app = create_app(mode)
                harness = ScreenshotHarness(app, args.output, mode)
                capture_state_group(app, None, harness, empty_states)
                app.destroy()
                app = None
    finally:
        if app is not None:
            app.destroy()
        if args.keep_db:
            print(f"kept seeded database: {db_path}")
        else:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    if not args.no_validate and not validate_screenshots(expected_paths):
        raise SystemExit(1)


def main() -> None:
    """CLI entrypoint."""
    args = parse_args()
    run_capture(args)


if __name__ == "__main__":
    main()
