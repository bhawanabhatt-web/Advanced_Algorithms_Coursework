from __future__ import annotations
import random
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from first_fit_decreasing import first_fit_decreasing 
from packing import Bin, Item, PackingResult  
from simulated_annealing import simulated_annealing  

class TestSimulatedAnnealing(unittest.TestCase):
    """Correctness tests for :func:`simulated_annealing`."""

    def test_invalid_initial_temperature_raises_value_error(self) -> None:
        items = [Item((0.5,))]
        initial = first_fit_decreasing(items)
        with self.assertRaises(ValueError):
            simulated_annealing(items, initial, initial_temperature=0.0)
        with self.assertRaises(ValueError):
            simulated_annealing(items, initial, initial_temperature=-1.0)

    def test_invalid_cooling_rate_raises_value_error(self) -> None:
        items = [Item((0.5,))]
        initial = first_fit_decreasing(items)
        with self.assertRaises(ValueError):
            simulated_annealing(items, initial, cooling_rate=0.0)
        with self.assertRaises(ValueError):
            simulated_annealing(items, initial, cooling_rate=1.5)

    def test_never_returns_more_bins_than_initial(self) -> None:
        rng = random.Random(42)
        items = [
            Item((rng.uniform(0.05, 0.4), rng.uniform(0.05, 0.4), rng.uniform(0.05, 0.4)))
            for _ in range(60)
        ]
        initial = first_fit_decreasing(items)
        improved = simulated_annealing(items, initial, iterations=1000)
        self.assertLessEqual(improved.num_bins, initial.num_bins)

    def test_result_remains_feasible(self) -> None:
        rng = random.Random(42)
        items = [Item((rng.uniform(0.05, 0.4),)) for _ in range(50)]
        initial = first_fit_decreasing(items)
        improved = simulated_annealing(items, initial, iterations=1000)
        self.assertTrue(improved.is_feasible(items))

    def test_is_reproducible_given_the_same_seed(self) -> None:
        rng = random.Random(1)
        items = [Item((rng.uniform(0.05, 0.4),)) for _ in range(40)]
        initial = first_fit_decreasing(items)
        result_a = simulated_annealing(items, initial, iterations=500, seed=99)
        result_b = simulated_annealing(items, initial, iterations=500, seed=99)
        self.assertEqual(result_a.num_bins, result_b.num_bins)

    def test_single_bin_input_is_returned_unchanged(self) -> None:
        items = [Item((0.5,))]
        bin_ = Bin(capacity=(1.0,), load=[0.0])
        bin_.add(0, items[0])
        initial = PackingResult(bins=[bin_])
        result = simulated_annealing(items, initial, iterations=100)
        self.assertEqual(result.num_bins, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)