# GEMINI.md - Project Context for Gemini CLI

This document provides a comprehensive overview of the "Study Testing Tool" project, derived from `projectGoal.md` and `technicalArchitecture.md`, and `test.txt` to serve as instructional context for future interactions with the Gemini CLI.

## Project Overview

The "Study Testing Tool" is a desktop application written in Python 3.9+ with a GUI built using CustomTkinter (or Tkinter). Its primary purpose is to allow users to import, take, and manage various types of tests (multiple-choice, essay), track their progress, and improve their learning through features like practice modes, performance analytics, and spaced repetition. The application is designed to run on macOS, offering a user-friendly interface for managing questions, taking tests with a timer, and reviewing results.

**Key Features (MVP):**
*   **Test Management:** Create, edit, and delete tests and questions.
*   **Test Taking:** Take multiple-choice and essay questions, with randomization of questions and answers. Includes a timer and question flagging.
*   **Results & History:** View immediate test scores, detailed question feedback, and historical performance trends.
*   **Data Storage:** Uses SQLite3 for persistent local storage, and JSON for test import/export.

**Technology Stack:**
*   **Language:** Python 3.9+
*   **GUI Framework:** CustomTkinter (or Tkinter)
*   **Database:** SQLite3
*   **Data Serialization:** JSON
*   **Platform:** macOS (cross-platform compatible)

## Project Structure

The project follows a modular structure to separate concerns and facilitate development.

```
study_test_tool/
│
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation
│
├── config/
│   ├── __init__.py
│   ├── settings.py                  # App configuration (colors, fonts, paths)
│   └── database.py                  # Database connection handler
│
├── models/
│   ├── __init__.py
│   ├── test.py                      # Test model
│   ├── question.py                  # Question model
│   ├── test_result.py               # Test result/attempt model
│   ├── user_settings.py             # User preferences model
│   └── achievement.py               # Achievement/badge model (Phase 2)
│
├── database/
│   ├── __init__.py
│   ├── db_manager.py                # Database operations manager
│   ├── schema.sql                   # Database schema
│   └── migrations/                  # Future schema updates
│
├── gui/
│   ├── __init__.py
│   ├── main_window.py               # Main application window
│   ├── test_selector.py             # Test selection screen
│   ├── test_editor.py               # Add/edit questions interface
│   ├── test_taking.py               # Active test interface
│   ├── results_view.py              # Test results display
│   ├── history_view.py              # Score history/analytics
│   ├── practice_mode.py             # Practice mode interface (Phase 1)
│   ├── review_mode.py               # Missed questions review (Phase 1)
│   └── components/
│       ├── question_widget.py       # Reusable question display
│       ├── timer_widget.py          # Timer display
│       ├── progress_bar.py          # Progress indicator
│       └── graph_widget.py          # Chart/graph components (Phase 1)
│
├── services/
│   ├── __init__.py
│   ├── test_service.py              # Business logic for tests
│   ├── question_service.py          # Question management
│   ├── scoring_service.py           # Score calculation
│   ├── import_service.py            # Import tests from files
│   ├── export_service.py            # Export tests/results
│   ├── randomizer_service.py        # Question/answer shuffling
│   ├── analytics_service.py         # Performance analytics (Phase 1)
│   ├── spaced_repetition.py         # Spaced repetition algorithm (Phase 3)
│   └── notification_service.py      # Reminders (Nice-to-have)
│
├── utils/
│   ├── __init__.py
│   ├── timer.py                     # Timer utility
│   ├── validators.py                # Input validation
│   ├── formatters.py                # Data formatting helpers
│   └── constants.py                 # App-wide constants
│
├── data/
│   ├── tests/                       # Imported test JSON files
│   ├── database/
│   │   └── study_tool.db            # SQLite database
│   └── backups/                     # Database backups
│
└── assets/
    ├── icons/                       # App icons
    └── themes/                      # Color themes (dark mode, etc.)
```

## Building and Running

### Initial Setup
To set up and run the application, follow these steps:

1.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    ```
2.  **Activate the virtual environment:**
    ```bash
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    The project uses a `requirements.txt` file to manage Python dependencies.
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application
Once the setup is complete, you can run the application using:

```bash
python main.py
```

### First Run Considerations
Upon the first run, the application will:
1.  Create the `data/database/study_tool.db` file.
2.  Initialize the database schema based on `schema.sql`.
3.  Set up default user settings.
4.  Display a welcome screen with instructions on how to import tests.

## Development Conventions

### Coding Style
*   The project uses Python, and adherence to PEP 8 guidelines is expected.
*   Consider using a linter (e.g., `pylint`) and a formatter (e.g., `black`) to maintain code quality and consistency.

### Testing
*   **Unit Tests:** Services and core logic should have independent unit tests, mocking database interactions.
*   **Integration Tests:** GUI interactions, database operations, and import/export functionality should be covered by integration tests.
*   **User Testing:** Crucial for validating UI/UX on macOS and testing performance with various datasets.
*   Recommended testing libraries include `pytest` and `pytest-cov`.

### Database Design
*   The database schema is defined in `database/schema.sql`.
*   Tables are designed for tests, questions, options, test attempts, and question responses.
*   Indexes should be used on frequently queried columns (`test_id`, `question_id`, `completed_at`) for performance.

### Modularity
*   The project is divided into `config`, `models`, `database`, `gui`, `services`, `utils`, `data`, and `assets` directories, each with specific responsibilities. This structure should be maintained for new features.

## Key Files and Their Contents

*   **`projectGoal.md`**: Outlines the overall vision, MVP features, and future phases (Phase 1, 2, 3, and Nice-to-Haves) of the Study Testing Tool.
*   **`technicalArchitecture.md`**: Provides a detailed technical blueprint, covering the technology stack, project structure, core systems (database, GUI, test management, scoring, import/export, timer), data models, and a comprehensive development roadmap. It also includes database schemas and API-like definitions for key services.
*   **`test.txt`**: Contains example multiple-choice questions with designated correct answers, demonstrating the format of test data the application is expected to handle. This file serves as an example of test content that can be imported into the application.
*   **`main.py` (Planned):** The entry point for the application, responsible for initializing the GUI and connecting the various services.
*   **`requirements.txt` (Planned):** Lists all necessary Python packages and their versions for the project.

This `GEMINI.md` file will serve as a foundational document for any future development or analysis tasks related to the "Study Testing Tool."
