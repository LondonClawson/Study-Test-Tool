"""Analytics service for performance tracking and visualization data."""

from typing import Dict, List, Optional

from database.db_manager import DatabaseManager

MAX_SCORE_TREND_POINTS = 200


class AnalyticsService:
    """Business logic for analytics, graphs, and weak topic identification."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        self._db = DatabaseManager(db_path)

    def get_scores_over_time(
        self,
        test_id: Optional[int] = None,
        mode: str = "test",
        max_points: Optional[int] = None,
    ) -> List[Dict]:
        """Get chronological scores for line chart.

        Args:
            test_id: Optional filter by test.
            mode: Filter by mode ("test" or "practice").
            max_points: Optional maximum number of chronologically sampled
                points to return. ``None`` preserves the full result set.

        Returns:
            List of dicts with id, percentage, completed_at, test_name.
        """
        return self._db.get_scores_over_time(test_id, mode, max_points)

    def get_average_scores_by_test(self, mode: str = "test") -> List[Dict]:
        """Get average/best/count per test for bar chart.

        Args:
            mode: Filter by mode.

        Returns:
            List of dicts with test_name, avg_score, best_score, attempt_count.
        """
        return self._db.get_average_scores_by_test(mode)

    def get_attempt_frequency(self, days: int = 30) -> List[Dict]:
        """Get daily attempt counts for activity chart.

        Args:
            days: Number of days to look back.

        Returns:
            List of dicts with day and count.
        """
        return self._db.get_attempt_frequency(days)

    def get_category_performance(
        self,
        test_id: Optional[int] = None,
        group_by: str = "auto",
    ) -> List[Dict]:
        """Get raw performance stats grouped by the chosen dimension.

        Args:
            test_id: Optional filter by test.
            group_by: Grouping dimension — ``"auto"`` (legacy fallback),
                ``"category"``, ``"test"``, or ``"group"``. See
                :meth:`DatabaseManager.get_category_performance` for details.

        Returns:
            List of dicts with category, total, correct, percentage.
        """
        return self._db.get_category_performance(test_id, group_by=group_by)

    def get_weak_topics(
        self,
        test_id: Optional[int] = None,
        threshold: float = 70.0,
        group_by: str = "auto",
    ) -> List[Dict]:
        """Get categories with health status classification.

        Args:
            test_id: Optional filter by test.
            threshold: Score below which a topic is "weak" (default 70%).
            group_by: Grouping dimension — ``"auto"``, ``"category"``,
                ``"test"``, or ``"group"``. See
                :meth:`get_category_performance` for details.

        Returns:
            List of dicts with category, total, correct, percentage, status.
            Status is "weak" (<threshold), "moderate" (threshold-85%), or
            "strong" (>85%).
        """
        categories = self._db.get_category_performance(test_id, group_by=group_by)
        result = []
        for cat in categories:
            pct = cat["percentage"]
            if pct < threshold:
                status = "weak"
            elif pct < 85.0:
                status = "moderate"
            else:
                status = "strong"
            result.append({**cat, "status": status})
        return result
