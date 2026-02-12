# Architecture Overview: Study Testing Tool

This document provides a high-level overview of the technical architecture for the "Study Testing Tool." The application is designed as a modular desktop application, prioritizing separation of concerns, maintainability, and extensibility.

## 1. High-Level Structure

The application is structured into distinct layers and modules, each responsible for specific functionalities:

*   **User Interface (GUI Layer):** Handles all visual elements and user interactions.
*   **Services/Business Logic Layer:** Contains the core logic for managing tests, questions, scoring, and other application functionalities.
*   **Data Models Layer:** Defines the structure of the data used throughout the application.
*   **Database Layer:** Manages persistent storage and retrieval of data.
*   **Utilities Layer:** Provides common helper functions and components.
*   **Configuration & Assets:** Stores application settings, database schema, icons, and themes.

```
study_test_tool/
│
├── main.py                          # Application entry point
│
├── config/                          # Application settings and database connection
│
├── models/                          # Data structures (Test, Question, TestAttempt, etc.)
│
├── database/                        # SQLite database management and schema
│
├── gui/                             # All graphical user interface components
│   ├── components/                  # Reusable GUI widgets
│
├── services/                        # Business logic for various features
│
├── utils/                           # General utility functions and helpers
│
├── data/                            # Runtime data storage (SQLite DB, imported tests, backups)
│
└── assets/                          # Application resources (icons, themes)
```

## 2. Key Architectural Components and Interactions

### a. **User Interface (GUI)**
*   Developed using CustomTkinter, providing a modern look and feel.
*   The `gui` directory contains modules for the main window, various screens (test selector, editor, taking, results, history), and reusable UI components.
*   Interacts with the `services` layer to perform actions based on user input and displays data retrieved from services.

### b. **Services Layer**
*   This is the heart of the application's logic. Modules like `test_service.py`, `question_service.py`, `scoring_service.py`, `import_service.py`, `randomizer_service.py`, and `analytics_service.py` encapsulate specific business rules.
*   Services interact with the `database` layer to store and retrieve data and utilize `models` to structure that data.
*   They provide clean APIs for the GUI layer to interact with, abstracting away the complexities of data management and business rules.

### c. **Data Models**
*   Defined in the `models` directory, these are Python classes (likely dataclasses) representing entities such as `Test`, `Question`, `TestAttempt`, `QuestionOption`, and `QuestionResponse`.
*   They ensure data consistency and provide a structured way to pass data between different layers of the application.

### d. **Database System**
*   Utilizes SQLite3 for local, file-based data persistence.
*   The `database` directory contains `db_manager.py` for centralizing database operations and `schema.sql` which defines the database structure.
*   Handles CRUD (Create, Read, Update, Delete) operations for all application data.

### e. **Import/Export System**
*   The `import_service.py` handles parsing JSON files to create new tests and questions within the application.
*   `export_service.py` (planned) will handle exporting data.
*   This system ensures the ability to easily add new test content and potentially share it.

### f. **Timer System**
*   A dedicated `Timer` utility in `utils/timer.py` manages time tracking during tests.
*   Integrated with a `timer_widget.py` in the GUI to provide a visual countdown/count-up.

## 3. Modularity and Extensibility

The architecture emphasizes modularity, where each component has a clear responsibility. This design choice makes the application:
*   **Easier to Understand:** Developers can focus on one part of the system at a time.
*   **Easier to Maintain:** Changes in one module are less likely to impact others.
*   **Easier to Extend:** New features (like Phase 1, 2, 3, and Nice-to-Have systems) can be added by introducing new services, GUI components, and potentially extending data models without major refactoring of existing core systems.

This high-level overview provides a foundational understanding of how the "Study Testing Tool" is structured and how its various parts work together to deliver the intended functionality.
