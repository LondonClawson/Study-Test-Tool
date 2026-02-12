# Technology Stack: Study Testing Tool

This document details the core technologies chosen for the development of the "Study Testing Tool," along with the rationale behind these selections.

## 1. Core Technologies

*   **Language:** Python 3.9+
    *   **Rationale:** Python is selected for its readability, extensive libraries, and strong community support, making it ideal for rapid development and maintainability.
*   **GUI Framework:** CustomTkinter (modern) or Tkinter (built-in)
    *   **Rationale:** CustomTkinter provides a modern look and feel over standard Tkinter, while Tkinter itself is built into Python, ensuring cross-platform compatibility and ease of deployment without external dependencies for the basic GUI. This choice aims for good aesthetics and user experience on macOS.
*   **Database:** SQLite3
    *   **Rationale:** SQLite3 is a lightweight, file-based, and serverless database solution, perfectly suited for single-user desktop applications. It's built into Python, simplifying development and distribution by eliminating the need for a separate database server. This ensures portability and ease of backup for user data.
*   **Data Serialization:** JSON (JavaScript Object Notation)
    *   **Rationale:** JSON is chosen for its human-readable format and ease of parsing within Python. It will be used primarily for importing and exporting test data, facilitating straightforward test file creation, sharing, and editing.
*   **Platform:** macOS (cross-platform compatible)
    *   **Rationale:** While initially targeting macOS, the choice of Python and Tkinter/CustomTkinter inherently provides cross-platform compatibility, allowing for potential future expansion to other operating systems with minimal changes.

## 2. Dependencies & Libraries

The project leverages several external Python libraries to extend its capabilities. These are managed via `requirements.txt`.

### Required (Minimum Viable Product - MVP)

These libraries are essential for the core functionality of the application:

*   **CustomTkinter (>=5.0.0):** For building the modern graphical user interface.
*   **Pillow (>=10.0.0):** An imaging library, likely used for handling icons or other graphical assets within the GUI.
*   **Python-Dateutil (>=2.8.2):** Provides powerful extensions to the standard datetime module, useful for parsing and manipulating dates and times (e.g., for test timestamps, streaks).
*   **SQLite3:** (Built-in to Python) No external `pip` installation required, but fundamental to data persistence.

### Phase 1 Additions (Core Learning)

Libraries to be introduced for analytics and graphing features:

*   **Matplotlib (>=3.7.0):** A comprehensive library for creating static, animated, and interactive visualizations in Python, essential for performance graphs.
*   **NumPy (>=1.24.0):** The fundamental package for numerical computing with Python, often used in conjunction with Matplotlib for data processing.

### Nice-to-Have Additions (Future Iterations)

Libraries considered for advanced features:

*   **ReportLab (>=4.0.0):** For generating PDF reports, such as study guides or detailed results summaries.
*   **pync (>=2.0.3):** (macOS only) For sending native macOS notifications, useful for study reminders.
*   **APScheduler (>=3.10.0):** An advanced Python scheduler for scheduling in-process background jobs, suitable for timed notifications and spaced repetition triggers.
*   **Pandas (>=2.0.0):** A powerful data manipulation and analysis library, useful for exporting test results to CSV or for more complex data analysis.

## 3. Development Tools

These tools aid in maintaining code quality and facilitating the development process:

*   **Pytest (>=7.4.0):** A robust and popular testing framework for Python, used for writing unit and integration tests.
*   **Pytest-Cov (>=4.1.0):** A plugin for pytest that provides test coverage reporting, ensuring thorough testing.
*   **Black (>=23.0.0):** An opinionated code formatter that helps maintain consistent code style across the project.
*   **Pylint (>=2.17.0):** A static code analyzer (linter) that identifies programming errors, helps enforce a coding standard, and sniffs for bad code smells.

This technology stack has been chosen to balance performance, ease of development, and maintainability, ensuring a robust and extensible application.
