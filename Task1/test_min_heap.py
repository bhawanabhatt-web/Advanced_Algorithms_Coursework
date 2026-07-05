from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from min_heap import MinHeap 


class TestMinHeap(unittest.TestCase):
    """Correctness tests for :class:`MinHeap`."""

    def setUp(self) -> None:
        self.heap: MinHeap[str] = MinHeap()

    def test_new_heap_is_empty(self) -> None:
        self.assertTrue(self.heap.is_empty())
        self.assertEqual(len(self.heap), 0)

    def test_push_increases_length(self) -> None:
        self.heap.push(1.0, "a")
        self.heap.push(2.0, "b")
        self.assertEqual(len(self.heap), 2)
        self.assertFalse(self.heap.is_empty())

    def test_pop_returns_minimum_priority_first(self) -> None:
        for priority, value in [(5.0, "e"), (1.0, "a"), (3.0, "c")]:
            self.heap.push(priority, value)
        self.assertEqual(self.heap.pop(), (1.0, "a"))
        self.assertEqual(self.heap.pop(), (3.0, "c"))
        self.assertEqual(self.heap.pop(), (5.0, "e"))

    def test_peek_does_not_remove_item(self) -> None:
        self.heap.push(1.0, "a")
        self.heap.push(2.0, "b")
        self.assertEqual(self.heap.peek(), (1.0, "a"))
        self.assertEqual(len(self.heap), 2)  # unchanged

    def test_pop_from_empty_heap_raises_index_error(self) -> None:
        with self.assertRaises(IndexError):
            self.heap.pop()

    def test_peek_at_empty_heap_raises_index_error(self) -> None:
        with self.assertRaises(IndexError):
            self.heap.peek()

    def test_pops_in_fully_sorted_order_for_random_input(self) -> None:
        rng = random.Random(42)
        priorities = [rng.uniform(0, 1000) for _ in range(500)]
        for priority in priorities:
            self.heap.push(priority, priority)

        popped = [self.heap.pop()[0] for _ in range(len(priorities))]
        self.assertEqual(popped, sorted(priorities))
        self.assertTrue(self.heap.is_empty())

    def test_handles_duplicate_priorities(self) -> None:
        self.heap.push(1.0, "first")
        self.heap.push(1.0, "second")
        first_pop = self.heap.pop()
        second_pop = self.heap.pop()
        self.assertEqual({first_pop[1], second_pop[1]}, {"first", "second"})


if __name__ == "__main__":
    unittest.main(verbosity=2)