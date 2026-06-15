"""Tests for test grouping and sorting features."""

import pytest

from models.test import Test
from gui.mix_test_display import build_mix_test_display


class TestGroupNameModel:
    """Test group_name field on the Test dataclass."""

    def test_default_group_name_empty(self):
        test = Test(name="T")
        assert test.group_name == ""

    def test_group_name_set(self):
        test = Test(name="T", group_name="Week 1")
        assert test.group_name == "Week 1"


class TestGroupNameCRUD:
    """Test group_name persistence through DatabaseManager."""

    def test_create_test_with_group_name(self, db):
        test = Test(name="Grouped", group_name="Cert Prep")
        test_id = db.create_test(test)
        fetched = db.get_test_by_id(test_id)
        assert fetched.group_name == "Cert Prep"

    def test_create_test_without_group_name(self, db):
        test = Test(name="Ungrouped")
        test_id = db.create_test(test)
        fetched = db.get_test_by_id(test_id)
        assert fetched.group_name == ""

    def test_update_test_group_name(self, db):
        test_id = db.create_test(Test(name="T"))
        test = db.get_test_by_id(test_id)
        test.group_name = "Week 2"
        db.update_test(test)
        fetched = db.get_test_by_id(test_id)
        assert fetched.group_name == "Week 2"

    def test_get_all_tests_includes_group_name(self, db):
        db.create_test(Test(name="A", group_name="Group 1"))
        db.create_test(Test(name="B", group_name="Group 2"))
        db.create_test(Test(name="C"))
        tests = db.get_all_tests()
        groups = {t.name: t.group_name for t in tests}
        assert groups["A"] == "Group 1"
        assert groups["B"] == "Group 2"
        assert groups["C"] == ""


class TestGroupNameMigration:
    """Test that group_name migration works on existing databases."""

    def test_migration_adds_group_name_column(self, db):
        """The migration in __init__ should have already added group_name."""
        conn = db._conn()
        try:
            columns = [
                row["name"]
                for row in conn.execute("PRAGMA table_info(tests)").fetchall()
            ]
            assert "group_name" in columns
        finally:
            conn.close()

    def test_migration_is_idempotent(self, db):
        """Running migration twice should not raise."""
        db._run_migrations()
        db._run_migrations()
        # Should still work
        test_id = db.create_test(Test(name="OK", group_name="G"))
        assert db.get_test_by_id(test_id).group_name == "G"


class TestSortingLogic:
    """Test the sorting logic that will be used in the home screen.

    We replicate the sort functions here as pure-Python unit tests
    since the GUI sort functions delegate to simple list operations.
    """

    @pytest.fixture
    def sample_tests(self, db):
        """Create tests with various names, groups, and timestamps."""
        db.create_test(Test(name="Zebra Test", group_name="Week 2"))
        db.create_test(Test(name="Alpha Test", group_name="Week 1"))
        db.create_test(Test(name="Middle Test", group_name=""))
        return db

    def test_sort_name_az(self, sample_tests):
        tests = sample_tests.get_all_tests()
        sorted_tests = sorted(tests, key=lambda t: t.name.lower())
        names = [t.name for t in sorted_tests]
        assert names == ["Alpha Test", "Middle Test", "Zebra Test"]

    def test_sort_name_za(self, sample_tests):
        tests = sample_tests.get_all_tests()
        sorted_tests = sorted(tests, key=lambda t: t.name.lower(), reverse=True)
        names = [t.name for t in sorted_tests]
        assert names == ["Zebra Test", "Middle Test", "Alpha Test"]

    def test_sort_by_group_then_name(self, sample_tests):
        tests = sample_tests.get_all_tests()
        sorted_tests = sorted(
            tests, key=lambda t: (t.group_name or "", t.name.lower())
        )
        names = [t.name for t in sorted_tests]
        # Empty group ("") sorts first, then "Week 1", then "Week 2"
        assert names == ["Middle Test", "Alpha Test", "Zebra Test"]

    def test_sort_last_updated_returns_all(self, sample_tests):
        """Default DB order returns all tests."""
        tests = sample_tests.get_all_tests()
        assert len(tests) == 3
        names = {t.name for t in tests}
        assert names == {"Zebra Test", "Alpha Test", "Middle Test"}

    def test_sort_date_created_desc(self, sample_tests):
        """Sorting by created_at desc produces a valid ordering."""
        tests = sample_tests.get_all_tests()
        sorted_tests = sorted(
            tests, key=lambda t: t.created_at or "", reverse=True
        )
        assert len(sorted_tests) == 3
        # Timestamps should be monotonically non-increasing
        timestamps = [t.created_at for t in sorted_tests]
        assert timestamps == sorted(timestamps, reverse=True)

    def test_group_headers_logic(self, sample_tests):
        """Test the grouping logic that produces group headers."""
        tests = sample_tests.get_all_tests()
        sorted_tests = sorted(
            tests, key=lambda t: (t.group_name or "", t.name.lower())
        )

        groups_seen = []
        current_group = None
        for test in sorted_tests:
            group = test.group_name if test.group_name else "Ungrouped"
            if group != current_group:
                current_group = group
                groups_seen.append(group)

        assert groups_seen == ["Ungrouped", "Week 1", "Week 2"]


class TestDistinctGroupNames:
    """Test get_distinct_group_names on DatabaseManager."""

    def test_get_distinct_group_names(self, db):
        db.create_test(Test(name="A", group_name="Week 2"))
        db.create_test(Test(name="B", group_name="Week 1"))
        db.create_test(Test(name="C", group_name="Week 2"))
        db.create_test(Test(name="D", group_name="Cert Prep"))
        result = db.get_distinct_group_names()
        assert result == ["Cert Prep", "Week 1", "Week 2"]

    def test_get_distinct_group_names_excludes_empty(self, db):
        db.create_test(Test(name="A", group_name=""))
        db.create_test(Test(name="B"))
        db.create_test(Test(name="C", group_name="Real Group"))
        result = db.get_distinct_group_names()
        assert result == ["Real Group"]

    def test_get_distinct_group_names_empty_table(self, db):
        result = db.get_distinct_group_names()
        assert result == []


class TestMixTestDisplay:
    """Test mixed-test title and subtitle display rules."""

    def test_complete_single_group_uses_group_title(self):
        tests = [
            Test(name="A", group_name="Contracts", id=1),
            Test(name="B", group_name="Contracts", id=2),
        ]
        display = build_mix_test_display(tests, [(t, 5) for t in tests], 10)

        assert display.title == "Contracts Mixed Test"
        assert display.subtitle == "10 questions from 2 tests in Contracts"

    def test_partial_single_group_mentions_selected_of_available(self):
        selected = [
            Test(name="A", group_name="Contracts", id=1),
            Test(name="B", group_name="Contracts", id=2),
        ]
        all_tests = selected + [
            Test(name="C", group_name="Contracts", id=3),
            Test(name="D", group_name="Contracts", id=4),
            Test(name="E", group_name="Contracts", id=5),
        ]
        display = build_mix_test_display(selected, [(t, 5) for t in all_tests], 12)

        assert display.title == "Contracts Mixed Test"
        assert display.subtitle == "12 questions from 2 of 5 tests in Contracts"

    def test_partial_single_group_singular_selected_still_uses_group_tests(self):
        selected = [Test(name="A", group_name="Contracts", id=1)]
        all_tests = selected + [
            Test(name="B", group_name="Contracts", id=2),
            Test(name="C", group_name="Contracts", id=3),
        ]
        display = build_mix_test_display(selected, [(t, 5) for t in all_tests], 1)

        assert display.title == "Contracts Mixed Test"
        assert display.subtitle == "1 question from 1 of 3 tests in Contracts"

    def test_two_groups_uses_both_group_names(self):
        tests = [
            Test(name="A", group_name="Torts", id=1),
            Test(name="B", group_name="Contracts", id=2),
        ]
        display = build_mix_test_display(tests, [(t, 5) for t in tests], 8)

        assert display.title == "Contracts + Torts Mixed Test"
        assert display.subtitle == "8 questions from 2 groups and 2 tests"

    def test_three_groups_uses_mixed_review(self):
        tests = [
            Test(name="A", group_name="Torts", id=1),
            Test(name="B", group_name="Contracts", id=2),
            Test(name="C", group_name="Evidence", id=3),
        ]
        display = build_mix_test_display(tests, [(t, 5) for t in tests], 9)

        assert display.title == "Mixed Review"
        assert display.subtitle == "9 questions from 3 groups and 3 tests"

    def test_ungrouped_only_uses_generic_mixed_test(self):
        tests = [
            Test(name="A", id=1),
            Test(name="B", id=2),
        ]
        display = build_mix_test_display(tests, [(t, 5) for t in tests], 7)

        assert display.title == "Mixed Test"
        assert display.subtitle == "7 questions from 2 tests"

    def test_named_group_plus_ungrouped_uses_named_group_title(self):
        tests = [
            Test(name="A", group_name="Contracts", id=1),
            Test(name="B", id=2),
        ]
        display = build_mix_test_display(tests, [(t, 5) for t in tests], 6)

        assert display.title == "Contracts Mixed Test"
        assert display.subtitle == "6 questions from 2 groups and 2 tests"


class TestTestServiceGroupName:
    """Test group_name through TestService layer."""

    def test_create_test_with_group(self, db_path):
        from config.database import initialize_database
        from services.test_service import TestService

        initialize_database(db_path)
        svc = TestService(db_path)
        test_id = svc.create_test("My Test", "desc", "Study Group")
        test = svc.get_test_by_id(test_id)
        assert test.group_name == "Study Group"

    def test_create_test_without_group(self, db_path):
        from config.database import initialize_database
        from services.test_service import TestService

        initialize_database(db_path)
        svc = TestService(db_path)
        test_id = svc.create_test("My Test")
        test = svc.get_test_by_id(test_id)
        assert test.group_name == ""
