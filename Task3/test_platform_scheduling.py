from __future__ import annotations
import random
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from platform_scheduling import (  
    min_platforms,
    min_platforms_exact,
)


class TestMinPlatforms(unittest.TestCase):
    """Correctness tests for :func:`min_platforms`."""

    def test_mismatched_lengths_raise_value_error(self) -> None:
        with self.assertRaises(ValueError):
            min_platforms([1, 2], [1])

    def test_empty_schedule_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            min_platforms([], [])

    def test_departure_before_arrival_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            min_platforms([100], [50])

    def test_single_train_needs_one_platform(self) -> None:
        self.assertEqual(min_platforms([900], [910]), 1)

    def test_known_textbook_example(self) -> None:
        arrivals = [900, 940, 950, 1100, 1500, 1800]
        departures = [910, 1200, 1120, 1130, 1900, 2000]
        self.assertEqual(min_platforms(arrivals, departures), 3)

    def test_all_trains_overlap_completely(self) -> None:
        arrivals = [100, 100, 100, 100]
        departures = [200, 200, 200, 200]
        self.assertEqual(min_platforms(arrivals, departures), 4)

    def test_no_trains_overlap(self) -> None:
        arrivals = [100, 200, 300]
        departures = [150, 250, 350]
        self.assertEqual(min_platforms(arrivals, departures), 1)

    def test_agrees_with_exact_reference_on_known_case(self) -> None:
        arrivals = [900, 940, 950, 1100, 1500, 1800]
        departures = [910, 1200, 1120, 1130, 1900, 2000]
        greedy_result = min_platforms(arrivals, departures)
        exact_result = min_platforms_exact(arrivals, departures)
        self.assertEqual(greedy_result, exact_result)

    def test_agrees_with_exact_reference_on_random_instances(self) -> None:
        rng = random.Random(42)
        for _ in range(20):
            n = rng.randint(1, 30)
            arrivals = [rng.randint(0, 200) for _ in range(n)]
            departures = [a + rng.randint(1, 50) for a in arrivals]
            self.assertEqual(
                min_platforms(arrivals, departures),
                min_platforms_exact(arrivals, departures),
            )

if __name__ == "__main__":
    unittest.main(verbosity=2)