from __future__ import annotations
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from knights_tour import knights_tour  


class TestKnightsTour(unittest.TestCase):
    """Correctness tests for :func:`knights_tour`."""
    def test_invalid_board_size_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            knights_tour(0)
        with self.assertRaises(ValueError):
            knights_tour(-5)

    def test_start_outside_board_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            knights_tour(5, start=(10, 10))

    def test_trivial_one_by_one_board_is_solved_immediately(self) -> None:
        result = knights_tour(1)
        self.assertTrue(result.solved)
        self.assertEqual(result.path, [(0, 0)])

    def test_5x5_board_is_solved_with_warnsdorff(self) -> None:
        result = knights_tour(5, use_warnsdorff=True)
        self.assertTrue(result.solved)
        self.assertEqual(len(result.path), 25)

    def test_tour_visits_every_square_exactly_once(self) -> None:
        board_size = 6
        result = knights_tour(board_size, use_warnsdorff=True)
        self.assertTrue(result.solved)
        assert result.path is not None
        self.assertEqual(len(result.path), board_size * board_size)
        self.assertEqual(len(set(result.path)), board_size * board_size)

    def test_consecutive_moves_are_valid_knight_moves(self) -> None:
        result = knights_tour(5, use_warnsdorff=True)
        assert result.path is not None
        for (r1, c1), (r2, c2) in zip(result.path, result.path[1:]):
            delta = (abs(r1 - r2), abs(c1 - c2))
            self.assertIn(delta, {(1, 2), (2, 1)})

    def test_warnsdorff_expands_far_fewer_nodes_than_naive_ordering(self) -> None:
        naive_result = knights_tour(6, use_warnsdorff=False, node_limit=500_000)
        warnsdorff_result = knights_tour(6, use_warnsdorff=True, node_limit=500_000)
        self.assertTrue(warnsdorff_result.solved)
        self.assertLess(warnsdorff_result.nodes_expanded, naive_result.nodes_expanded)
        # Warnsdorff's rule should be at least two orders of magnitude more efficient here.
        self.assertLess(warnsdorff_result.nodes_expanded * 100, naive_result.nodes_expanded)

    def test_node_limit_is_respected_when_search_fails(self) -> None:
        result = knights_tour(8, use_warnsdorff=False, node_limit=1000)
        self.assertFalse(result.solved)
        # The limit is checked once per backtracking call; sibling branches
        # at shallow recursion depth may each add a few more calls before
        # the whole search unwinds, so allow a small margin above the limit.
        self.assertLess(result.nodes_expanded, 1000 + 500)


if __name__ == "__main__":
    unittest.main(verbosity=2)