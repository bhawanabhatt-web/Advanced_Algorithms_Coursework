from __future__ import annotations
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from first_fit_decreasing import first_fit_decreasing 
from packing import Item 


class TestFirstFitDecreasing(unittest.TestCase):
    """Correctness tests for :func:`first_fit_decreasing`."""

    def test_empty_item_list_returns_no_bins(self) -> None:
        result = first_fit_decreasing([])
        self.assertEqual(result.num_bins, 0)

    def test_single_item_uses_one_bin(self) -> None:
        result = first_fit_decreasing([Item((0.5, 0.5, 0.5))])
        self.assertEqual(result.num_bins, 1)

    def test_items_that_all_fit_together_use_one_bin(self) -> None:
        items = [Item((0.2, 0.2, 0.2)) for _ in range(4)]  # total 0.8 per dimension
        result = first_fit_decreasing(items)
        self.assertEqual(result.num_bins, 1)

    def test_items_that_cannot_share_a_bin_use_separate_bins(self) -> None:
        items = [Item((0.6, 0.6, 0.6)), Item((0.6, 0.6, 0.6))]
        result = first_fit_decreasing(items)
        self.assertEqual(result.num_bins, 2)

    def test_result_is_always_feasible(self) -> None:
        rng = random.Random(42)
        items = [
            Item((rng.uniform(0.05, 0.4), rng.uniform(0.05, 0.4), rng.uniform(0.05, 0.4)))
            for _ in range(100)
        ]
        result = first_fit_decreasing(items)
        self.assertTrue(result.is_feasible(items))

    def test_never_uses_more_bins_than_items(self) -> None:
        rng = random.Random(7)
        items = [Item((rng.uniform(0.05, 0.4),)) for _ in range(30)]
        result = first_fit_decreasing(items)
        self.assertLessEqual(result.num_bins, len(items))


if __name__ == "__main__":
    unittest.main(verbosity=2)