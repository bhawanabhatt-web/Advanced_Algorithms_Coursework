from __future__ import annotations
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from job_scheduling import Job, weighted_job_scheduling  # noqa: E402

class TestJob(unittest.TestCase):
    """Validation tests for the :class:`Job` dataclass."""

    def test_end_before_start_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            Job(start=5, end=3, profit=10)

    def test_end_equal_start_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            Job(start=5, end=5, profit=10)

    def test_negative_profit_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            Job(start=1, end=2, profit=-1)

    def test_valid_job_constructs_successfully(self) -> None:
        job = Job(start=1, end=3, profit=5)
        self.assertEqual((job.start, job.end, job.profit), (1, 3, 5))


class TestWeightedJobScheduling(unittest.TestCase):
    """Correctness tests for :func:`weighted_job_scheduling`."""

    def test_empty_job_list_returns_zero_profit(self) -> None:
        result = weighted_job_scheduling([])
        self.assertEqual(result.max_profit, 0)
        self.assertEqual(result.selected_jobs, [])

    def test_single_job_is_always_selected(self) -> None:
        job = Job(start=1, end=3, profit=5)
        result = weighted_job_scheduling([job])
        self.assertEqual(result.max_profit, 5)
        self.assertEqual(result.selected_jobs, [job])

    def test_non_overlapping_jobs_are_all_selected(self) -> None:
        jobs = [Job(1, 2, 5), Job(2, 3, 6), Job(3, 4, 4)]
        result = weighted_job_scheduling(jobs)
        self.assertEqual(result.max_profit, 15)
        self.assertEqual(len(result.selected_jobs), 3)

    def test_known_optimal_selection_with_overlap(self) -> None:
        jobs = [Job(1, 3, 5), Job(2, 5, 6), Job(4, 6, 5), Job(6, 7, 4)]
        result = weighted_job_scheduling(jobs)
        # Optimal: (1,3,5) + (4,6,5) + (6,7,4) = 14 (touching intervals do not overlap)
        self.assertEqual(result.max_profit, 14)
        self.assertEqual(
            sorted((job.start, job.end) for job in result.selected_jobs),
            [(1, 3), (4, 6), (6, 7)],
        )

    def test_greedy_by_profit_alone_would_be_suboptimal(self) -> None:
        # A single highly profitable job that overlaps two smaller, jointly
        # more profitable jobs -- confirms the DP is not simply "pick the
        # highest-profit job first".
        high_value_overlapping = Job(0, 10, 100)
        small_job_a = Job(0, 5, 60)
        small_job_b = Job(5, 10, 60)
        result = weighted_job_scheduling([high_value_overlapping, small_job_a, small_job_b])
        self.assertEqual(result.max_profit, 120)
        self.assertEqual(len(result.selected_jobs), 2)

    def test_selected_jobs_never_overlap(self) -> None:
        jobs = [Job(0, 3, 5), Job(1, 4, 8), Job(3, 6, 4), Job(5, 8, 9), Job(2, 7, 20)]
        result = weighted_job_scheduling(jobs)
        selected = sorted(result.selected_jobs, key=lambda job: job.start)
        for earlier, later in zip(selected, selected[1:]):
            self.assertLessEqual(earlier.end, later.start)


if __name__ == "__main__":
    unittest.main(verbosity=2)