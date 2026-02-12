"""Test management service — wraps database operations for tests."""

from typing import Dict, List, Optional

from database.db_manager import DatabaseManager
from models.test import Test


class TestService:
    """Business logic for test CRUD operations."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        self._db = DatabaseManager(db_path)

    def create_test(self, name: str, description: str = "") -> int:
        """Create a new test and return its id."""
        test = Test(name=name, description=description)
        return self._db.create_test(test)

    def get_all_tests(self) -> List[Test]:
        """Get all tests (without questions)."""
        return self._db.get_all_tests()

    def get_test_by_id(self, test_id: int) -> Optional[Test]:
        """Get a test with all questions and options."""
        return self._db.get_test_by_id(test_id)

    def update_test(self, test: Test) -> None:
        """Update a test's name and description."""
        self._db.update_test(test)

    def delete_test(self, test_id: int) -> None:
        """Delete a test and all associated data."""
        self._db.delete_test(test_id)

    def get_question_count(self, test_id: int) -> int:
        """Get the number of questions in a test."""
        return self._db.get_question_count(test_id)

    def get_test_statistics(self, test_id: int) -> Dict:
        """Get attempt statistics for a test."""
        return self._db.get_test_statistics(test_id)
