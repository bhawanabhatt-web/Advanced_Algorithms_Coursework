from __future__ import annotations
import math
import sys
import unittest
from pathlib import Path
from avl_tree import AVLTree 

class TestAVLTree(unittest.TestCase):
    """Correctness tests for :class:`AVLTree`, including balance guarantees."""

    def setUp(self) -> None:
        self.tree: AVLTree[str] = AVLTree()

    def test_empty_tree_has_zero_length_and_height_minus_one(self) -> None:
        self.assertEqual(len(self.tree), 0)
        self.assertEqual(self.tree.height(), -1)

    def test_insert_and_search_single_key(self) -> None:
        self.tree.insert(10, "ten")
        self.assertEqual(self.tree.search(10), "ten")
        self.assertEqual(len(self.tree), 1)

    def test_search_missing_key_returns_none(self) -> None:
        self.tree.insert(10, "ten")
        self.assertIsNone(self.tree.search(999))

    def test_insert_overwrites_existing_key(self) -> None:
        self.tree.insert(10, "ten")
        self.tree.insert(10, "TEN")
        self.assertEqual(self.tree.search(10), "TEN")
        self.assertEqual(len(self.tree), 1)

    def test_matches_reference_dict_for_many_keys(self) -> None:
        keys = [50, 20, 70, 10, 30, 60, 80, 5, 15, 25, 35]
        reference: dict[int, str] = {}
        for key in keys:
            value = f"city-{key}"
            self.tree.insert(key, value)
            reference[key] = value

        for key, value in reference.items():
            self.assertEqual(self.tree.search(key), value)
        self.assertEqual(len(self.tree), len(reference))

    def test_sorted_insertion_stays_balanced(self) -> None:
        """Unlike a plain BST, inserting keys in sorted order must NOT
        produce a linear-height tree: AVL height must stay O(log n)."""
        n = 1000
        for key in range(n):
            self.tree.insert(key, key)
        max_allowed_height = math.ceil(1.45 * math.log2(n + 2)) - 1
        self.assertLessEqual(self.tree.height(), max_allowed_height)

    def test_delete_leaf_node(self) -> None:
        for key in (50, 20, 70):
            self.tree.insert(key, str(key))
        self.assertTrue(self.tree.delete(20))
        self.assertIsNone(self.tree.search(20))
        self.assertEqual(len(self.tree), 2)

    def test_delete_node_with_two_children(self) -> None:
        for key in (50, 20, 70, 10, 30, 60, 80):
            self.tree.insert(key, str(key))
        self.assertTrue(self.tree.delete(50))
        self.assertIsNone(self.tree.search(50))
        for key in (20, 70, 10, 30, 60, 80):
            self.assertEqual(self.tree.search(key), str(key))

    def test_delete_missing_key_returns_false(self) -> None:
        self.tree.insert(10, "ten")
        self.assertFalse(self.tree.delete(999))
        self.assertEqual(len(self.tree), 1)

    def test_remains_balanced_after_many_deletions(self) -> None:
        n = 500
        for key in range(n):
            self.tree.insert(key, key)
        for key in range(0, n, 2):  # delete every even key
            self.tree.delete(key)
        remaining = n // 2
        max_allowed_height = math.ceil(1.45 * math.log2(remaining + 2)) - 1
        self.assertLessEqual(self.tree.height(), max_allowed_height)
        self.assertEqual(len(self.tree), remaining)


if __name__ == "__main__":
    unittest.main(verbosity=2)