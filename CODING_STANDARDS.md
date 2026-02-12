# Coding Standards and Conventions: Study Testing Tool

This document outlines the coding standards and conventions to be followed during the development of the "Study Testing Tool." Adhering to these guidelines ensures code quality, consistency, readability, and maintainability across the project.

## 1. General Principles

*   **Readability:** Code should be easy to read and understand. Prioritize clarity over cleverness.
*   **Consistency:** Maintain a consistent style throughout the codebase.
*   **Modularity:** Break down code into small, reusable functions and classes with single responsibilities.
*   **Documentation:** Add comments where necessary to explain *why* certain decisions were made or *how* complex logic works, rather than simply *what* the code does. Use docstrings for modules, classes, and functions.
*   **Error Handling:** Implement robust error handling to make the application resilient.
*   **Security:** Follow best practices to prevent vulnerabilities, especially concerning data handling and user input.

## 2. Python Specific Guidelines

The project is developed in Python, and therefore adheres to the official Python style guide, PEP 8, with additional considerations:

### a. PEP 8 Compliance

*   **Linters:** Use `pylint` to identify potential errors, enforce coding standards, and detect "code smells."
*   **Formatters:** Use `black` as an opinionated code formatter. All code should be formatted with `black` to ensure consistent style.

### b. Naming Conventions

*   **Modules:** `lowercase_with_underscores.py` (e.g., `test_service.py`, `main_window.py`).
*   **Packages:** `lowercase_with_underscores` (e.g., `services`, `gui`).
*   **Classes:** `CamelCase` (e.g., `TestService`, `MainWindow`).
*   **Functions and Methods:** `lowercase_with_underscores()` (e.g., `get_all_tests()`, `_private_helper()`).
*   **Variables:** `lowercase_with_underscores` (e.g., `total_questions`, `user_answer`).
*   **Constants:** `UPPERCASE_WITH_UNDERSCORES` (e.g., `LIGHT_THEME`, `DB_PATH`).
*   **Private/Protected Members:** Prefix with a single underscore (`_`) for internal use (e.g., `_load_config()`).

### c. Imports

*   Imports should generally be at the top of the file, one import per line if possible.
*   Group imports in the following order:
    1.  Standard library imports.
    2.  Third-party imports.
    3.  Local application-specific imports.
*   Sort imports alphabetically within each group.

### d. Docstrings and Comments

*   All public modules, classes, methods, and functions should have docstrings.
*   Use triple double-quotes (`"""Docstring content"""`) for docstrings.
*   Docstrings should briefly explain the purpose of the code, its arguments, and what it returns.
*   Comments should be used sparingly for explaining *why* something is done, not *what* is done (unless the "what" is not immediately obvious from the code).

### e. Type Hinting

*   Utilize Python's type hints (PEP 484) for function arguments and return values to improve code clarity and enable static analysis.
    ```python
    def calculate_score(correct_answers: int, total_questions: int) -> float:
        """Calculates the percentage score."""
        if total_questions == 0:
            return 0.0
        return (correct_answers / total_questions) * 100.0
    ```

## 3. Project Structure Conventions

*   Maintain the modular project structure as defined in `technicalArchitecture.md`.
*   Ensure clear separation of concerns between `gui`, `services`, `models`, `database`, and `utils` modules.
*   New features should be integrated into the appropriate existing modules or new modules that follow these conventions.

## 4. Database Conventions

*   **Schema:** Database schema changes should be documented in `database/schema.sql` and potentially through migration scripts.
*   **Naming:** Table names should be plural (e.g., `tests`, `questions`), and column names lowercase with underscores (e.g., `question_text`, `time_taken`).
*   **ORM/Wrapper:** Use a consistent approach for database interactions (e.g., a custom `db_manager.py` or an ORM if introduced later).

## 5. GUI Development Conventions

*   **CustomTkinter:** Adhere to CustomTkinter's best practices for creating widgets and managing layouts.
*   **Responsiveness:** Design GUI components to be responsive and handle various window sizes if applicable.
*   **User Experience (UX):** Prioritize intuitive and consistent user experience across the application.

By consistently applying these coding standards, we aim to build a high-quality, maintainable, and collaborative codebase for the "Study Testing Tool."
