# Study Testing Tool - Technical Architecture & Systems Documentation

## 📋 Table of Contents
1. [Technology Stack](#technology-stack)
2. [Project Structure](#project-structure)
3. [Core Systems (MVP)](#core-systems-mvp)
4. [Data Models](#data-models)
5. [Phase 1 Systems](#phase-1-systems)
6. [Phase 2 Systems](#phase-2-systems)
7. [Phase 3 Systems](#phase-3-systems)
8. [Nice-to-Have Systems](#nice-to-have-systems)
9. [Dependencies & Libraries](#dependencies--libraries)
10. [Development Roadmap](#development-roadmap)

---

## Technology Stack

### Core Technologies
- **Language**: Python 3.9+
- **GUI Framework**: CustomTkinter (modern) or Tkinter (built-in)
- **Database**: SQLite3 (built-in, file-based, perfect for single-user)
- **Data Serialization**: JSON (for test import/export)
- **Platform**: macOS (cross-platform compatible)

### Why These Choices?
- **SQLite**: No server needed, portable, built-in to Python
- **CustomTkinter**: Modern look, easy to use, Mac-friendly aesthetics
- **JSON**: Human-readable, easy test file creation/editing

---

## Project Structure

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

---

## Core Systems (MVP)

### 1. **Database System**
**Purpose**: Persistent storage for tests, questions, results, and user data

**Key Components**:
- `database/db_manager.py` - Central database operations
- `database/schema.sql` - Database structure

**Tables Needed**:
```sql
-- Tests table
CREATE TABLE tests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Questions table
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

-- Multiple choice options table
CREATE TABLE question_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    option_text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT 0,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);

-- Test attempts/results table
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

-- Individual question responses
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
```

**Key Operations**:
- CRUD operations for tests and questions
- Store test attempts with timestamp
- Query historical results
- Retrieve questions with randomization

---

### 2. **GUI System**
**Purpose**: User interface for all interactions

**Key Components**:

#### **Main Window** (`gui/main_window.py`)
- Application shell
- Navigation between views
- Menu bar (File, Edit, View, Help)

#### **Test Selector** (`gui/test_selector.py`)
- Display all available tests
- Search/filter tests
- Buttons: "Take Test", "Edit Test", "View Results"

#### **Test Editor** (`gui/test_editor.py`)
- Add new test
- Add questions to existing test
- Edit existing questions
- Delete questions
- Form fields:
  - Question text input
  - Question type dropdown (Multiple Choice / Essay)
  - Multiple choice options (dynamic fields)
  - Correct answer marking
  - Category/topic input

#### **Test Taking Interface** (`gui/test_taking.py`)
- Display current question
- Show question number (e.g., "5 of 20")
- Multiple choice: Radio buttons or checkboxes
- Essay: Text area
- Navigation buttons: "Previous", "Next", "Flag for Review"
- Timer display (running clock)
- "Finish Test" button
- Flag indicator for flagged questions
- List of flagged questions (sidebar or popup)

#### **Results View** (`gui/results_view.py`)
- Display score (#/# and %)
- Time taken
- List of questions with:
  - Question text
  - User's answer
  - Correct answer
  - Correct/Incorrect indicator
- Essay questions: Side-by-side comparison
- Button to review incorrect questions only

#### **History View** (`gui/history_view.py`)
- Table of all past test attempts
- Columns: Date, Test Name, Score, Percentage, Time
- Sort by date, score, test name
- Filter by test
- Click to view detailed results

---

### 3. **Test Management System**
**Purpose**: Handle test and question logic

**Key Components**:

#### **Test Service** (`services/test_service.py`)
```python
class TestService:
    def get_all_tests()
    def get_test_by_id(test_id)
    def create_test(name, description)
    def update_test(test_id, name, description)
    def delete_test(test_id)
    def get_test_statistics(test_id)  # avg score, times taken, etc.
```

#### **Question Service** (`services/question_service.py`)
```python
class QuestionService:
    def get_questions_for_test(test_id, randomize=True)
    def add_question(test_id, question_data)
    def update_question(question_id, question_data)
    def delete_question(question_id)
    def get_question_with_options(question_id)
```

#### **Randomizer Service** (`services/randomizer_service.py`)
```python
class RandomizerService:
    def shuffle_questions(questions)
    def shuffle_options(question)  # Maintain correct answer tracking
    def generate_test_order(test_id)  # Returns randomized question IDs
```

---

### 4. **Test Taking System**
**Purpose**: Manage active test session

**Key Components**:

#### **Test Session Manager** (`services/test_session.py`)
```python
class TestSession:
    def __init__(self, test_id):
        self.test_id = test_id
        self.questions = []  # Randomized questions
        self.current_index = 0
        self.responses = {}  # question_id: user_answer
        self.flagged = set()  # question_ids that are flagged
        self.start_time = None
        self.question_times = {}  # Time spent per question
    
    def start()
    def get_current_question()
    def save_response(question_id, answer)
    def flag_question(question_id)
    def next_question()
    def previous_question()
    def finish_test()
    def get_elapsed_time()
```

---

### 5. **Scoring System**
**Purpose**: Calculate and store test results

**Key Components**:

#### **Scoring Service** (`services/scoring_service.py`)
```python
class ScoringService:
    def score_test(test_session):
        # Returns: {
        #   'score': 8,
        #   'total': 10,
        #   'percentage': 80.0,
        #   'correct_questions': [ids],
        #   'incorrect_questions': [ids],
        #   'time_taken': 300  # seconds
        # }
    
    def score_question(question, user_answer):
        # Returns: True/False for multiple choice
        # Returns: None for essay (user evaluates)
    
    def save_attempt(test_id, score_data, responses):
        # Save to database
    
    def get_attempt_details(attempt_id):
        # Retrieve full attempt with all responses
```

---

### 6. **Import/Export System**
**Purpose**: Load tests from files

**Key Components**:

#### **Import Service** (`services/import_service.py`)
```python
class ImportService:
    def import_from_json(file_path):
        # Parse JSON file and create test + questions
    
    def validate_test_format(data):
        # Ensure proper structure
```

**Expected JSON Format**:
```json
{
  "name": "Math Test - Chapter 5",
  "description": "Algebra and equations",
  "questions": [
    {
      "text": "What is 2 + 2?",
      "type": "multiple_choice",
      "category": "Basic Arithmetic",
      "options": [
        {"text": "3", "correct": false},
        {"text": "4", "correct": true},
        {"text": "5", "correct": false},
        {"text": "22", "correct": false}
      ]
    },
    {
      "text": "Explain the Pythagorean theorem",
      "type": "essay",
      "category": "Geometry",
      "expected_answer": "a² + b² = c² for right triangles..."
    }
  ]
}
```

---

### 7. **Timer System**
**Purpose**: Track time during tests

**Key Components**:

#### **Timer Utility** (`utils/timer.py`)
```python
class Timer:
    def __init__(self):
        self.start_time = None
        self.elapsed = 0
        self.running = False
    
    def start()
    def pause()
    def resume()
    def stop()
    def get_elapsed()  # Returns seconds
    def get_formatted_time()  # Returns "MM:SS" or "HH:MM:SS"
```

#### **Timer Widget** (`gui/components/timer_widget.py`)
- Display running time
- Update every second
- Visual component for GUI

---

## Data Models

### Test Model (`models/test.py`)
```python
@dataclass
class Test:
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    questions: List[Question] = field(default_factory=list)
```

### Question Model (`models/question.py`)
```python
@dataclass
class Question:
    id: int
    test_id: int
    text: str
    type: str  # 'multiple_choice' or 'essay'
    category: str
    correct_answer: str
    options: List[QuestionOption] = field(default_factory=list)  # For MC only
    
@dataclass
class QuestionOption:
    id: int
    question_id: int
    text: str
    is_correct: bool
```

### Test Attempt Model (`models/test_result.py`)
```python
@dataclass
class TestAttempt:
    id: int
    test_id: int
    score: int
    total_questions: int
    percentage: float
    time_taken: int  # seconds
    completed_at: datetime
    responses: List[QuestionResponse] = field(default_factory=list)

@dataclass
class QuestionResponse:
    id: int
    attempt_id: int
    question_id: int
    user_answer: str
    is_correct: bool
    was_flagged: bool
    time_spent: int
```

---

## Phase 1 Systems

### 1. **Practice Mode System**
**Purpose**: Immediate feedback while learning

**Components**:
- `gui/practice_mode.py` - Interface for practice mode
- `services/practice_service.py` - Practice mode logic

**Features**:
- After answering, immediately show correct/incorrect
- Display explanation if available
- Don't save to test history (or mark as "practice")
- Option to continue to next question

**Database Addition**:
```sql
-- Add mode field to test_attempts
ALTER TABLE test_attempts ADD COLUMN mode TEXT DEFAULT 'test'; -- 'test' or 'practice'
```

---

### 2. **Missed Questions Review System**
**Purpose**: Focus on weak areas

**Components**:
- `gui/review_mode.py` - Interface for review
- `services/review_service.py` - Logic to retrieve missed questions

**Features**:
```python
class ReviewService:
    def get_missed_questions(test_id=None, limit=None):
        # Return questions user got wrong previously
        # Optional: filter by specific test
        # Optional: limit to N most recent
    
    def get_frequently_missed(min_attempts=3):
        # Questions missed X% of the time
    
    def create_review_session(question_ids):
        # Create a custom session with specific questions
```

---

### 3. **Performance Graphs System**
**Purpose**: Visualize progress over time

**Components**:
- `gui/components/graph_widget.py` - Chart display
- `services/analytics_service.py` - Data aggregation

**Libraries Needed**:
- `matplotlib` - Graph generation
- `matplotlib-backend` for Tkinter integration

**Graphs to Implement**:
1. **Score Over Time**: Line graph of test scores
2. **Average by Test**: Bar chart comparing different tests
3. **Attempt Frequency**: Calendar heatmap of study days

```python
class AnalyticsService:
    def get_score_timeline(test_id=None, days=30):
        # Returns: [(date, score, percentage), ...]
    
    def get_average_by_test():
        # Returns: [(test_name, avg_score), ...]
    
    def get_attempt_calendar(days=90):
        # Returns: [(date, num_attempts), ...]
```

---

### 4. **Weak Topic Identification System**
**Purpose**: Highlight areas needing improvement

**Components**:
- `services/analytics_service.py` - Analysis logic
- Display in `gui/history_view.py`

```python
class AnalyticsService:
    def get_category_performance(test_id=None):
        # Returns: [
        #   {
        #     'category': 'Algebra',
        #     'correct': 15,
        #     'total': 20,
        #     'percentage': 75.0
        #   },
        # ]
    
    def get_weakest_categories(threshold=70.0, min_questions=3):
        # Return categories below threshold percentage
```

**Display**:
- Visual list with red/yellow/green indicators
- "Focus on these topics" section
- Link to review questions from weak categories

---

## Phase 2 Systems

### 1. **Achievement System**
**Purpose**: Gamification and motivation

**Database Addition**:
```sql
CREATE TABLE achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    icon TEXT,  -- icon identifier
    requirement_type TEXT,  -- 'score', 'streak', 'count'
    requirement_value INTEGER
);

CREATE TABLE user_achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    achievement_id INTEGER,
    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (achievement_id) REFERENCES achievements(id)
);
```

**Achievements to Implement**:
- Perfect Score (100%)
- First Test Completed
- 10 Tests Completed
- 100 Tests Completed
- 7-Day Streak
- 30-Day Streak
- Speed Demon (complete test in under X minutes)
- Comeback Kid (improve score by 20%+ on retake)

```python
class AchievementService:
    def check_achievements(attempt_id):
        # Check if any achievements unlocked after this attempt
    
    def get_user_achievements():
        # Get all unlocked achievements
    
    def get_progress_to_next(achievement_id):
        # Show progress toward locked achievement
```

---

### 2. **Study Streak Tracking System**
**Purpose**: Encourage daily practice

**Database Addition**:
```sql
CREATE TABLE study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL UNIQUE,
    tests_taken INTEGER DEFAULT 0,
    time_spent INTEGER DEFAULT 0  -- seconds
);
```

```python
class StreakService:
    def record_study_day():
        # Mark today as studied
    
    def get_current_streak():
        # Return consecutive days studied
    
    def get_longest_streak():
        # Historical best
    
    def get_calendar_data(year, month):
        # For calendar view display
```

**Display**:
- Show current streak on main screen
- Calendar view with highlighted study days
- Notification if about to break streak

---

### 3. **Note-Taking System**
**Purpose**: Personal notes on questions

**Database Addition**:
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

```python
class NoteService:
    def add_note(question_id, note_text):
    def get_note(question_id):
    def update_note(note_id, note_text):
    def delete_note(note_id):
```

**UI Component**:
- Notes section on review/results screens
- Quick note button during test (optional)
- Notes visible in review mode

---

### 4. **Custom Test Builder System**
**Purpose**: Create custom test sessions

**Components**:
- `gui/test_builder.py` - Interface
- `services/test_builder_service.py` - Logic

```python
class TestBuilderService:
    def create_custom_test(config):
        # config = {
        #   'source_tests': [test_ids],
        #   'categories': ['Algebra', 'Geometry'],
        #   'question_count': 20,
        #   'difficulty': 'medium',  # if implemented
        #   'exclude_seen': True  # only new questions
        # }
        # Returns: list of question_ids
```

**UI Features**:
- Multi-select tests as sources
- Filter by category
- Set question limit
- Option to exclude previously answered questions

---

## Phase 3 Systems

### 1. **Spaced Repetition System**
**Purpose**: Optimize review timing based on memory science

**Algorithm**: Simplified SM-2 (SuperMemo 2)

**Database Addition**:
```sql
CREATE TABLE spaced_repetition (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL UNIQUE,
    easiness_factor REAL DEFAULT 2.5,
    interval INTEGER DEFAULT 1,  -- days until next review
    repetitions INTEGER DEFAULT 0,
    next_review_date DATE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);
```

```python
class SpacedRepetitionService:
    def update_after_response(question_id, quality):
        # quality: 0-5 (how well did they know it?)
        # Update easiness factor and next review date
    
    def get_due_questions():
        # Questions due for review today
    
    def get_review_schedule(days=30):
        # Calendar of upcoming reviews
```

**Implementation**:
- After each question, ask: "How well did you know this?" (1-5 scale)
- Calculate next review date
- "Due for Review" section on main screen
- Automatic study session creation from due questions

---

### 2. **Explanation System**
**Purpose**: Help users understand why answers are correct

**Database Addition**:
```sql
ALTER TABLE questions ADD COLUMN explanation TEXT;
```

**Import Format Update**:
```json
{
  "text": "What is 2 + 2?",
  "type": "multiple_choice",
  "options": [...],
  "explanation": "Addition combines values. 2 + 2 = 4 because..."
}
```

**Display**:
- Show explanation after answering in practice mode
- Available in review mode
- Optional: Toggle visibility

---

### 3. **Study Session Planner System**
**Purpose**: Schedule and organize study time

**Database Addition**:
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

```python
class StudyPlannerService:
    def schedule_session(test_id, date, time):
    def get_upcoming_sessions():
    def mark_completed(session_id):
    def get_suggested_schedule(test_id, target_date):
        # AI-like: suggest optimal study schedule before exam
```

**UI Features**:
- Calendar view
- Add/edit/remove sessions
- Reminders (if notifications enabled)
- Auto-suggest based on performance

---

## Nice-to-Have Systems

### 1. **Advanced Analytics**

#### Time-Per-Question Analytics
```python
def get_question_time_stats(question_id):
    # Average time spent on this question
    # User's time vs average
```

#### Best/Worst Time of Day
```sql
-- Add time to test_attempts
ALTER TABLE test_attempts ADD COLUMN time_of_day TEXT;
```

```python
def get_performance_by_time():
    # Returns: [(hour_range, avg_score), ...]
```

#### Learning Curve Visualization
```python
def get_learning_curve(test_id):
    # Plot: attempt number vs score
    # Show trend line
```

---

### 2. **Confidence Rating System**

**Database Addition**:
```sql
ALTER TABLE question_responses ADD COLUMN confidence INTEGER; -- 1-5
```

**Implementation**:
- After each answer, ask: "How confident are you?"
- Track: confident+correct, confident+wrong, uncertain+correct, etc.
- Identify overconfidence or underconfidence patterns

---

### 3. **Flashcard System**

```python
class FlashcardService:
    def generate_from_questions(question_ids):
        # Convert questions to flashcard format
    
    def export_to_anki():
        # Export in Anki-compatible format
```

---

### 4. **Export/Backup System**

```python
class ExportService:
    def export_test_results_csv(test_id):
    def export_study_report_pdf(test_id, date_range):
    def backup_database(filepath):
    def restore_database(filepath):
```

---

### 5. **Dark Mode System**

**Implementation**:
```python
# config/themes.py
LIGHT_THEME = {
    'bg': '#FFFFFF',
    'fg': '#000000',
    'primary': '#007AFF',
    ...
}

DARK_THEME = {
    'bg': '#1E1E1E',
    'fg': '#FFFFFF',
    'primary': '#0A84FF',
    ...
}

class ThemeManager:
    def __init__(self):
        self.current_theme = LIGHT_THEME
    
    def toggle_theme():
    def apply_theme(widget):
```

**Database**:
```sql
CREATE TABLE user_settings (
    key TEXT PRIMARY KEY,
    value TEXT
);
-- Store: theme, font_size, keyboard_shortcuts_enabled, etc.
```

---

### 6. **Keyboard Shortcuts System**

```python
# gui/shortcuts.py
class ShortcutManager:
    SHORTCUTS = {
        'a': select_option_a,
        'b': select_option_b,
        'c': select_option_c,
        'd': select_option_d,
        'n': next_question,
        'p': previous_question,
        'f': flag_question,
        'cmd+s': save_test,
        'cmd+q': quit_app,
    }
    
    def bind_shortcuts(window):
```

---

### 7. **Notification System**

**macOS Notifications**:
```python
# Using pync library (macOS only)
import pync

class NotificationService:
    def send_study_reminder():
        pync.notify(
            'Time to study!',
            title='Study Test Tool',
            sound='default'
        )
    
    def schedule_reminders(time_list):
        # Use apscheduler for scheduling
```

**Requires**:
- `pync` (macOS notifications)
- `apscheduler` (task scheduling)

---

## Dependencies & Libraries

### Required (MVP)
```txt
# requirements.txt

# GUI
customtkinter>=5.0.0        # Modern Tkinter
pillow>=10.0.0              # Image handling

# Database (built-in)
# sqlite3 comes with Python

# Data handling
python-dateutil>=2.8.2      # Date parsing
```

### Phase 1 Additions
```txt
# Analytics & Graphs
matplotlib>=3.7.0           # Graphing
numpy>=1.24.0               # Data processing for graphs
```

### Phase 2 Additions
```txt
# None - use built-in libraries
```

### Phase 3 Additions
```txt
# None - use built-in libraries
```

### Nice-to-Have Additions
```txt
# PDF Export
reportlab>=4.0.0            # PDF generation

# Notifications (macOS)
pync>=2.0.3                 # macOS notifications

# Scheduling
apscheduler>=3.10.0         # Task scheduling

# Data Export
pandas>=2.0.0               # CSV export
```

### Development Tools
```txt
# Testing
pytest>=7.4.0
pytest-cov>=4.1.0

# Code Quality
black>=23.0.0               # Code formatter
pylint>=2.17.0              # Linter
```

---

## Development Roadmap

### Sprint 1: Foundation (Week 1-2)
**Goal**: Basic app structure and database

- [ ] Set up project structure
- [ ] Create database schema
- [ ] Implement database manager
- [ ] Create data models
- [ ] Basic GUI window and navigation
- [ ] Test selector screen (empty state)

### Sprint 2: Core Features (Week 3-4)
**Goal**: Take a test end-to-end

- [ ] Import service (JSON to database)
- [ ] Test editor (add questions)
- [ ] Test taking interface
- [ ] Question randomization
- [ ] Answer randomization
- [ ] Timer implementation
- [ ] Flag question feature

### Sprint 3: Results & History (Week 5-6)
**Goal**: Score tests and view history

- [ ] Scoring service
- [ ] Results view screen
- [ ] Show correct/incorrect answers
- [ ] Essay comparison view
- [ ] Test history screen
- [ ] Historical results storage

### Sprint 4: Phase 1 Features (Week 7-8)
**Goal**: Learning tools

- [ ] Practice mode interface
- [ ] Missed questions review
- [ ] Analytics service
- [ ] Performance graphs
- [ ] Weak topic identification

### Sprint 5: Phase 2 Features (Week 9-10)
**Goal**: Engagement features

- [ ] Achievement system
- [ ] Study streak tracking
- [ ] Note-taking per question
- [ ] Custom test builder

### Sprint 6: Phase 3 Features (Week 11-12)
**Goal**: Advanced learning

- [ ] Spaced repetition algorithm
- [ ] Explanation display
- [ ] Study session planner
- [ ] Due review system

### Sprint 7+: Nice-to-Haves (Week 13+)
**Goal**: Polish and extras

- [ ] Dark mode
- [ ] Keyboard shortcuts
- [ ] Advanced analytics
- [ ] Confidence rating
- [ ] Export/backup
- [ ] Notifications
- [ ] Flashcard generation

---

## Testing Strategy

### Unit Tests
- Test each service independently
- Mock database calls
- Test randomization algorithms
- Test scoring logic

### Integration Tests
- Test GUI interactions
- Test database operations
- Test import/export functionality

### User Testing
- Test on actual macOS systems
- Validate UI/UX flow
- Performance testing with large question sets

---

## Getting Started

### Initial Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

### First Run Setup
1. App creates `data/database/study_tool.db`
2. Initialize database schema
3. Create default settings
4. Show welcome screen with import instructions

---

## Performance Considerations

### Database Optimization
- Index frequently queried columns (test_id, question_id, completed_at)
- Use connection pooling
- Implement database migrations for schema updates

### GUI Responsiveness
- Load large test lists asynchronously
- Paginate history view for many attempts
- Cache frequently accessed data
- Use threading for database operations to prevent UI freeze

### Memory Management
- Don't load all tests into memory at once
- Clear old test session data
- Implement lazy loading for question lists

---

## Security & Privacy

### Data Privacy
- All data stored locally (SQLite)
- No external network calls
- User has full control over data

### Backup Recommendations
- Implement auto-backup feature
- Export functionality for manual backups
- Document backup restoration process

---

This documentation should serve as your technical blueprint. Start with the MVP systems, ensure they work well, then progressively add features from each phase. Good luck with your build!
