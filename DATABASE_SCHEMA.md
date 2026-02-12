# Database Schema: Study Testing Tool

This document details the SQLite database schema for the "Study Testing Tool." The schema is designed to store information about tests, questions, answer options, user attempts, and responses, as well as supporting features like achievements, study streaks, and notes.

## 1. Core Database Tables (MVP)

These tables are fundamental for the Minimum Viable Product (MVP) of the application.

### `tests` Table

Stores general information about each test.

| Column Name | Type              | Constraints                               | Description                                     |
| :---------- | :---------------- | :---------------------------------------- | :---------------------------------------------- |
| `id`        | `INTEGER`         | `PRIMARY KEY AUTOINCREMENT`               | Unique identifier for the test.                 |
| `name`      | `TEXT`            | `NOT NULL`                                | Name of the test (e.g., "Math Chapter 5 Quiz"). |
| `description` | `TEXT`          |                                           | Optional, longer description of the test.       |
| `created_at` | `TIMESTAMP`      | `DEFAULT CURRENT_TIMESTAMP`               | Timestamp when the test was created.            |
| `updated_at` | `TIMESTAMP`      | `DEFAULT CURRENT_TIMESTAMP`               | Timestamp when the test was last updated.       |

```sql
CREATE TABLE tests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### `questions` Table

Stores individual questions belonging to tests.

| Column Name     | Type      | Constraints                               | Description                                                               |
| :-------------- | :-------- | :---------------------------------------- | :------------------------------------------------------------------------ |
| `id`            | `INTEGER` | `PRIMARY KEY AUTOINCREMENT`               | Unique identifier for the question.                                       |
| `test_id`       | `INTEGER` | `NOT NULL`, `FOREIGN KEY` (`tests`)       | Foreign key referencing the `tests` table.                                |
| `question_text` | `TEXT`    | `NOT NULL`                                | The full text of the question.                                            |
| `question_type` | `TEXT`    | `NOT NULL` (e.g., `'multiple_choice'`, `'essay'`) | Type of question.                                                         |
| `correct_answer` | `TEXT`   | `NOT NULL`                                | For MC: the correct option text (if not using `question_options`); for essay: expected answer. |
| `category`      | `TEXT`    |                                           | Optional category for the question (e.g., "Algebra", "Geometry").         |
| `created_at`    | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP`               | Timestamp when the question was created.                                  |
| `explanation`   | `TEXT`    | *(Phase 3 Addition)*                      | Explanation for the correct answer, if available.                         |

```sql
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    question_type TEXT NOT NULL, -- 'multiple_choice' or 'essay'
    correct_answer TEXT NOT NULL, -- For MC: the correct option; for essay: expected answer
    category TEXT, -- For weak topic identification
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (test_id) REFERENCES tests(id) ON DELETE CASCADE
);
-- Phase 3 Addition:
ALTER TABLE questions ADD COLUMN explanation TEXT;
```

### `question_options` Table

Stores answer options for multiple-choice questions.

| Column Name | Type      | Constraints                               | Description                                         |
| :---------- | :-------- | :---------------------------------------- | :-------------------------------------------------- |
| `id`        | `INTEGER` | `PRIMARY KEY AUTOINCREMENT`               | Unique identifier for the option.                   |
| `question_id` | `INTEGER` | `NOT NULL`, `FOREIGN KEY` (`questions`)   | Foreign key referencing the `questions` table.      |
| `option_text` | `TEXT`    | `NOT NULL`                                | The text of the answer option.                      |
| `is_correct` | `BOOLEAN` | `DEFAULT 0` (`0` for false, `1` for true) | Indicates if this is the correct option for the question. |

```sql
CREATE TABLE question_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    option_text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT 0,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);
```

### `test_attempts` Table

Records each instance of a user taking a test.

| Column Name       | Type      | Constraints                               | Description                                       |
| :---------------- | :-------- | :---------------------------------------- | :------------------------------------------------ |
| `id`              | `INTEGER` | `PRIMARY KEY AUTOINCREMENT`               | Unique identifier for the test attempt.           |
| `test_id`         | `INTEGER` | `NOT NULL`, `FOREIGN KEY` (`tests`)       | Foreign key referencing the `tests` table.        |
| `score`           | `INTEGER` | `NOT NULL`                                | Number of questions answered correctly.           |
| `total_questions` | `INTEGER` | `NOT NULL`                                | Total number of questions in the attempt.         |
| `percentage`      | `REAL`    | `NOT NULL`                                | Score as a percentage (0.0 to 100.0).             |
| `time_taken`      | `INTEGER` |                                           | Time taken to complete the test in seconds.       |
| `completed_at`    | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP`               | Timestamp when the test attempt was completed.    |
| `mode`            | `TEXT`    | `DEFAULT 'test'` (e.g., `'test'`, `'practice'`) | Indicates the mode in which the test was taken. |
| `time_of_day`     | `TEXT`    | *(Nice-to-Have Addition)*                 | Time of day when the test was taken (e.g., "Morning", "Afternoon"). |

```sql
CREATE TABLE test_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    total_questions INTEGER NOT NULL,
    percentage REAL NOT NULL,
    time_taken INTEGER, -- in seconds
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (test_id) REFERENCES tests(id) ON DELETE CASCADE
);
-- Phase 1 Addition:
ALTER TABLE test_attempts ADD COLUMN mode TEXT DEFAULT 'test';
-- Nice-to-Have Addition:
ALTER TABLE test_attempts ADD COLUMN time_of_day TEXT;
```

### `question_responses` Table

Records the user's response for each question within a `test_attempt`.

| Column Name    | Type      | Constraints                               | Description                                               |
| :------------- | :-------- | :---------------------------------------- | :-------------------------------------------------------- |
| `id`           | `INTEGER` | `PRIMARY KEY AUTOINCREMENT`               | Unique identifier for the question response.              |
| `attempt_id`   | `INTEGER` | `NOT NULL`, `FOREIGN KEY` (`test_attempts`) | Foreign key referencing the `test_attempts` table.        |
| `question_id`  | `INTEGER` | `NOT NULL`, `FOREIGN KEY` (`questions`)   | Foreign key referencing the `questions` table.            |
| `user_answer`  | `TEXT`    |                                           | The answer provided by the user.                          |
| `is_correct`   | `BOOLEAN` |                                           | `0` for incorrect, `1` for correct, `NULL` for essay (user evaluates). |
| `was_flagged`  | `BOOLEAN` | `DEFAULT 0`                               | `1` if the user flagged the question for review.          |
| `time_spent`   | `INTEGER` |                                           | Time spent on this specific question in seconds.          |
| `confidence`   | `INTEGER` | *(Nice-to-Have Addition)*                 | User's confidence rating (1-5) for the answer.            |

```sql
CREATE TABLE question_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attempt_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    user_answer TEXT,
    is_correct BOOLEAN,
    was_flagged BOOLEAN DEFAULT 0,
    time_spent INTEGER, -- seconds on this question
    FOREIGN KEY (attempt_id) REFERENCES test_attempts(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);
-- Nice-to-Have Addition:
ALTER TABLE question_responses ADD COLUMN confidence INTEGER;
```

## 2. Phase-Specific Tables and Additions

These tables and column additions support features introduced in later development phases.

### `achievements` Table (Phase 2)

Defines available achievements for gamification.

| Column Name       | Type      | Constraints                               | Description                                         |
| :---------------- | :-------- | :---------------------------------------- | :-------------------------------------------------- |
| `id`              | `INTEGER` | `PRIMARY KEY AUTOINCREMENT`               | Unique identifier for the achievement.              |
| `name`            | `TEXT`    | `NOT NULL`                                | Name of the achievement (e.g., "Perfect Score").    |
| `description`     | `TEXT`    |                                           | Description of how to earn the achievement.         |
| `icon`            | `TEXT`    |                                           | Path or identifier for the achievement's icon.      |
| `requirement_type` | `TEXT`    | (e.g., `'score'`, `'streak'`, `'count'`) | Type of condition for unlocking the achievement.    |
| `requirement_value` | `INTEGER` |                                           | Numerical value required to unlock the achievement. |

```sql
CREATE TABLE achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    icon TEXT,
    requirement_type TEXT,
    requirement_value INTEGER
);
```

### `user_achievements` Table (Phase 2)

Tracks achievements unlocked by the user.

| Column Name     | Type      | Constraints                               | Description                                         |
| :-------------- | :-------- | :---------------------------------------- | :-------------------------------------------------- |
| `id`            | `INTEGER` | `PRIMARY KEY AUTOINCREMENT`               | Unique identifier for the user achievement record.  |
| `achievement_id` | `INTEGER` | `FOREIGN KEY` (`achievements`)            | Foreign key referencing the `achievements` table.   |
| `unlocked_at`   | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP`               | Timestamp when the achievement was unlocked.        |

```sql
CREATE TABLE user_achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    achievement_id INTEGER,
    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (achievement_id) REFERENCES achievements(id)
);
```

### `study_sessions` Table (Phase 2)

Records daily study activity for streak tracking.

| Column Name | Type      | Constraints             | Description                                   |
| :---------- | :-------- | :---------------------- | :-------------------------------------------- |
| `id`        | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Unique identifier for the study session.      |
| `date`      | `DATE`    | `NOT NULL UNIQUE`       | The date of the study session.                |
| `tests_taken` | `INTEGER` | `DEFAULT 0`             | Number of tests taken on this day.            |
| `time_spent` | `INTEGER` | `DEFAULT 0`             | Total time spent studying on this day (seconds). |

```sql
CREATE TABLE study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL UNIQUE,
    tests_taken INTEGER DEFAULT 0,
    time_spent INTEGER DEFAULT 0
);
```

### `question_notes` Table (Phase 2)

Allows users to attach notes to specific questions.

| Column Name    | Type      | Constraints                               | Description                                         |
| :------------- | :-------- | :---------------------------------------- | :-------------------------------------------------- |
| `id`           | `INTEGER` | `PRIMARY KEY AUTOINCREMENT`               | Unique identifier for the note.                     |
| `question_id`  | `INTEGER` | `NOT NULL`, `FOREIGN KEY` (`questions`)   | Foreign key referencing the `questions` table.      |
| `note`         | `TEXT`    | `NOT NULL`                                | The content of the user's note.                     |
| `created_at`   | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP`               | Timestamp when the note was created.                |
| `updated_at`   | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP`               | Timestamp when the note was last updated.           |

```sql
CREATE TABLE question_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    note TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);
```

### `spaced_repetition` Table (Phase 3)

Manages spaced repetition parameters for each question.

| Column Name        | Type      | Constraints                             | Description                                             |
| :----------------- | :-------- | :-------------------------------------- | :------------------------------------------------------ |
| `id`               | `INTEGER` | `PRIMARY KEY AUTOINCREMENT`             | Unique identifier.                                      |
| `question_id`      | `INTEGER` | `NOT NULL UNIQUE`, `FOREIGN KEY` (`questions`) | Foreign key referencing the `questions` table, unique per question. |
| `easiness_factor`  | `REAL`    | `DEFAULT 2.5`                           | SM-2 algorithm's easiness factor.                       |
| `interval`         | `INTEGER` | `DEFAULT 1`                             | Number of days until the next review.                   |
| `repetitions`      | `INTEGER` | `DEFAULT 0`                             | Number of times the question has been successfully repeated. |
| `next_review_date` | `DATE`    |                                         | The calculated date for the next review.                |

```sql
CREATE TABLE spaced_repetition (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL UNIQUE,
    easiness_factor REAL DEFAULT 2.5,
    interval INTEGER DEFAULT 1,
    repetitions INTEGER DEFAULT 0,
    next_review_date DATE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);
```

### `study_plan` Table (Phase 3)

Allows users to schedule study sessions.

| Column Name      | Type      | Constraints                               | Description                                         |
| :--------------- | :-------- | :---------------------------------------- | :-------------------------------------------------- |
| `id`             | `INTEGER` | `PRIMARY KEY AUTOINCREMENT`               | Unique identifier for the study plan entry.         |
| `test_id`        | `INTEGER` | `FOREIGN KEY` (`tests`)                   | Optional foreign key to a specific test.            |
| `scheduled_date` | `DATE`    |                                           | The date the study session is scheduled for.        |
| `scheduled_time` | `TIME`    |                                           | The time the study session is scheduled for.        |
| `completed`      | `BOOLEAN` | `DEFAULT 0`                               | `1` if the session was completed.                   |
| `completed_at`   | `TIMESTAMP` |                                           | Timestamp when the session was marked completed.    |

```sql
CREATE TABLE study_plan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER,
    scheduled_date DATE,
    scheduled_time TIME,
    completed BOOLEAN DEFAULT 0,
    completed_at TIMESTAMP,
    FOREIGN KEY (test_id) REFERENCES tests(id)
);
```

### `user_settings` Table (Nice-to-Have)

Stores user-specific application settings.

| Column Name | Type      | Constraints                 | Description                                         |
| :---------- | :-------- | :-------------------------- | :-------------------------------------------------- |
| `key`       | `TEXT`    | `PRIMARY KEY`               | Setting key (e.g., 'theme', 'font_size').           |
| `value`     | `TEXT`    |                             | Stored value for the setting.                       |

```sql
CREATE TABLE user_settings (
    key TEXT PRIMARY KEY,
    value TEXT
);
```
