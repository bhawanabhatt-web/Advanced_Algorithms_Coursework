from __future__ import annotations
import sys
import unittest
from pathlib import Path
from binary_search_tree import BinarySearchTree  

class TestBinarySearchTree(unittest.TestCase):
    """Correctness tests for :class:`BinarySearchTree`."""

    def setUp(self) -> None:
        self.tree: BinarySearchTree[str] = BinarySearchTree()

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

    def test_contains_operator(self) -> None:
        self.tree.insert(10, "ten")
        self.assertIn(10, self.tree)
        self.assertNotIn(999, self.tree)

    def test_insert_overwrites_existing_key(self) -> None:
        self.tree.insert(10, "ten")
        self.tree.insert(10, "TEN")
        self.assertEqual(self.tree.search(10), "TEN")
        self.assertEqual(len(self.tree), 1)  # overwrite must not grow the tree

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

    def test_delete_leaf_node(self) -> None:
        for key in (50, 20, 70):
            self.tree.insert(key, str(key))
        self.assertTrue(self.tree.delete(20))
        self.assertIsNone(self.tree.search(20))
        self.assertEqual(len(self.tree), 2)

    def test_delete_node_with_two_children(self) -> None:
        for key in (50, 20, 70, 10, 30, 60, 80):
            self.tree.insert(key, str(key))
        self.assertTrue(self.tree.delete(50))  # root has two children
        self.assertIsNone(self.tree.search(50))
        # every other key must still be reachable after the successor swap
        for key in (20, 70, 10, 30, 60, 80):
            self.assertEqual(self.tree.search(key), str(key))

    def test_delete_missing_key_returns_false(self) -> None:
        self.tree.insert(10, "ten")
        self.assertFalse(self.tree.delete(999))
        self.assertEqual(len(self.tree), 1)

    def test_worst_case_sorted_insertion_produces_linear_height(self) -> None:
        """Inserting sorted keys degrades a BST to a linked list: height == n - 1."""
        for key in range(10):
            self.tree.insert(key, key)
        self.assertEqual(self.tree.height(), 9)


if __name__ == "__main__":
    unittest.main(verbosity=2)