# Development Environment Setup: Study Testing Tool

This document provides instructions for setting up the development environment, installing dependencies, and running the "Study Testing Tool" application.

## 1. Initial Setup

To get the application up and running on your local machine, follow these steps:

### Prerequisites
*   **Python 3.9+:** Ensure you have Python version 3.9 or newer installed. You can download it from [python.org](https://www.python.org/downloads/) or use a package manager like Homebrew on macOS (`brew install python@3.9`).
*   **Git:** (Optional, but recommended) For cloning the repository.

### Steps

1.  **Clone the Repository (if applicable):**
    If the project is hosted in a version control system, clone it to your local machine:
    ```bash
    git clone <repository_url>
    cd study_test_tool/
    ```
    *(Note: Replace `<repository_url>` with the actual repository URL if available. Otherwise, navigate to the project directory.)*

2.  **Create a Virtual Environment:**
    It is highly recommended to use a virtual environment to manage project dependencies and avoid conflicts with other Python projects.
    ```bash
    python3 -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    *   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    *   **Windows (Command Prompt):**
        ```bash
        venv\Scripts\activate.bat
        ```
    *   **Windows (PowerShell):**
        ```bash
        venv\Scripts\Activate.ps1
        ```
    *(You should see `(venv)` prepended to your terminal prompt, indicating the virtual environment is active.)*

4.  **Install Dependencies:**
    The project uses a `requirements.txt` file to list all necessary Python packages.
    ```bash
    pip install -r requirements.txt
    ```
    *(If `requirements.txt` is not yet created, the necessary dependencies are detailed in `TECH_STACK.md` and include `customtkinter`, `Pillow`, and `python-dateutil` for MVP, with others for later phases.)*

## 2. Running the Application

Once the development environment is set up and dependencies are installed, you can run the application:

```bash
python main.py
```

## 3. First Run Considerations

Upon the very first execution of the application, it will perform initial setup tasks:

1.  **Database Creation:** A SQLite database file, `study_tool.db`, will be created in the `data/database/` directory.
2.  **Schema Initialization:** The database schema will be initialized based on the definitions in `schema.sql`.
3.  **Default Settings:** Any default user settings will be applied.
4.  **Welcome Screen:** A welcome screen with instructions on how to import tests will likely be displayed, guiding the user through their initial interaction.

## 4. Deactivating the Virtual Environment

When you are done working on the project, you can deactivate the virtual environment:

```bash
deactivate
```
This will return your terminal to its global Python environment.
