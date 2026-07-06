from __future__ import annotations
import random
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from first_fit_decreasing import first_fit_decreasing  
from local_search import local_search  
from packing import Bin, Item, PackingResult  

class TestLocalSearch(unittest.TestCase):
    """Correctness tests for :func:`local_search`."""

    def test_never_increases_bin_count(self) -> None:
        rng = random.Random(42)
        items = [
            Item((rng.uniform(0.05, 0.4), rng.uniform(0.05, 0.4), rng.uniform(0.05, 0.4)))
            for _ in range(100)
        ]
        initial = first_fit_decreasing(items)
        improved = local_search(items, initial)
        self.assertLessEqual(improved.num_bins, initial.num_bins)

    def test_result_remains_feasible(self) -> None:
        rng = random.Random(42)
        items = [Item((rng.uniform(0.05, 0.4),)) for _ in range(50)]
        initial = first_fit_decreasing(items)
        improved = local_search(items, initial)
        self.assertTrue(improved.is_feasible(items))

    def test_can_eliminate_an_artificially_sparse_bin(self) -> None:
        # Construct a packing where one bin holds a single small item that
        # could clearly be merged into another under-full bin.
        items = [Item((0.5,)), Item((0.1,))]
        full_ish_bin = Bin(capacity=(1.0,), load=[0.0])
        full_ish_bin.add(0, items[0])
        sparse_bin = Bin(capacity=(1.0,), load=[0.0])
        sparse_bin.add(1, items[1])
        initial = PackingResult(bins=[full_ish_bin, sparse_bin])

        improved = local_search(items, initial)
        self.assertEqual(improved.num_bins, 1)
        self.assertTrue(improved.is_feasible(items))

    def test_single_bin_input_is_returned_unchanged(self) -> None:
        items = [Item((0.5,))]
        bin_ = Bin(capacity=(1.0,), load=[0.0])
        bin_.add(0, items[0])
        initial = PackingResult(bins=[bin_])
        improved = local_search(items, initial)
        self.assertEqual(improved.num_bins, 1)

if __name__ == "__main__":
    unittest.main(verbosity=2)