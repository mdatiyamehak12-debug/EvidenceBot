"""
Unit tests for Persistent Search History Manager (utils/history_manager.py)
"""

import unittest
from utils.history_manager import (
    load_search_history,
    add_to_history,
    clear_search_history,
)


class TestHistoryManager(unittest.TestCase):
    def setUp(self):
        clear_search_history()

    def tearDown(self):
        clear_search_history()

    def test_empty_history(self):
        history = load_search_history()
        self.assertEqual(history, [])

    def test_add_and_latest_first_order(self):
        add_to_history("First Query", year_range="2010-2020")
        add_to_history("Second Query", year_range="2020-2026")

        history = load_search_history()
        self.assertEqual(len(history), 2)
        # Latest search must appear first
        self.assertEqual(history[0]["query"], "Second Query")
        self.assertEqual(history[0]["year_range"], "2020-2026")
        self.assertEqual(history[1]["query"], "First Query")

    def test_deduplication(self):
        add_to_history("metformin t2d", year_range="All Years")
        add_to_history("zinc cold", year_range="2020-2026")
        # Add duplicate with different casing
        add_to_history("Metformin T2D", year_range="2015-2026")

        history = load_search_history()
        # Should not store duplicate
        self.assertEqual(len(history), 2)
        # Metformin T2D should be promoted to the top
        self.assertEqual(history[0]["query"], "Metformin T2D")
        self.assertEqual(history[1]["query"], "zinc cold")

    def test_clear_history(self):
        add_to_history("Query 1")
        add_to_history("Query 2")
        self.assertEqual(len(load_search_history()), 2)

        clear_search_history()
        self.assertEqual(load_search_history(), [])


if __name__ == "__main__":
    unittest.main()

