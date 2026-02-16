-- Study Testing Tool - MVP Database Schema

CREATE TABLE IF NOT EXISTS tests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT DEFAULT '',
    group_name TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    question_type TEXT NOT NULL CHECK (question_type IN ('multiple_choice', 'essay')),
    correct_answer TEXT NOT NULL DEFAULT '',
    category TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (test_id) REFERENCES tests (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS question_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    option_text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT 0,
    FOREIGN KEY (question_id) REFERENCES questions (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS test_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER NOT NULL,
    score INTEGER NOT NULL DEFAULT 0,
    total_questions INTEGER NOT NULL DEFAULT 0,
    percentage REAL NOT NULL DEFAULT 0.0,
    time_taken INTEGER,
    mode TEXT DEFAULT 'test',
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (test_id) REFERENCES tests (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS question_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attempt_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    user_answer TEXT,
    is_correct BOOLEAN,
    was_flagged BOOLEAN DEFAULT 0,
    time_spent INTEGER,
    FOREIGN KEY (attempt_id) REFERENCES test_attempts (id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions (id) ON DELETE CASCADE
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_questions_test_id ON questions (test_id);
CREATE INDEX IF NOT EXISTS idx_question_options_question_id ON question_options (question_id);
CREATE INDEX IF NOT EXISTS idx_test_attempts_test_id ON test_attempts (test_id);
CREATE INDEX IF NOT EXISTS idx_test_attempts_completed_at ON test_attempts (completed_at);
CREATE INDEX IF NOT EXISTS idx_question_responses_attempt_id ON question_responses (attempt_id);
CREATE INDEX IF NOT EXISTS idx_question_responses_question_id ON question_responses (question_id);
CREATE INDEX IF NOT EXISTS idx_question_responses_is_correct ON question_responses (is_correct);

-- Trigger to update the updated_at column on tests
CREATE TRIGGER IF NOT EXISTS update_tests_timestamp
AFTER UPDATE ON tests
FOR EACH ROW
BEGIN
    UPDATE tests SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;
