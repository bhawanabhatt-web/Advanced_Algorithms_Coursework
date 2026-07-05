from __future__ import annotations
import sys
import unittest
from pathlib import Path
from hash_table import HashTable 

class TestHashTable(unittest.TestCase):
    """Correctness tests for :class:`HashTable`."""

    def setUp(self) -> None:
        self.table: HashTable[int] = HashTable(initial_capacity=4)

    def test_new_table_is_empty(self) -> None:
        self.assertEqual(len(self.table), 0)

    def test_invalid_initial_capacity_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            HashTable(initial_capacity=0)
        with self.assertRaises(ValueError):
            HashTable(initial_capacity=-5)

    def test_insert_and_search(self) -> None:
        self.table.insert(1, 100)
        self.assertEqual(self.table.search(1), 100)

    def test_search_missing_key_returns_none(self) -> None:
        self.assertIsNone(self.table.search(999))

    def test_contains_operator(self) -> None:
        self.table.insert(1, 100)
        self.assertIn(1, self.table)
        self.assertNotIn(2, self.table)

    def test_insert_overwrites_existing_key(self) -> None:
        self.table.insert(1, 100)
        self.table.insert(1, 200)
        self.assertEqual(self.table.search(1), 200)
        self.assertEqual(len(self.table), 1)

    def test_delete_existing_key(self) -> None:
        self.table.insert(1, 100)
        self.assertTrue(self.table.delete(1))
        self.assertIsNone(self.table.search(1))
        self.assertEqual(len(self.table), 0)

    def test_delete_missing_key_returns_false(self) -> None:
        self.assertFalse(self.table.delete(999))

    def test_resizes_automatically_beyond_load_factor(self) -> None:
        initial_capacity = self.table._capacity  # white-box check, test-only
        for key in range(20):
            self.table.insert(key, key * key)
        self.assertGreater(self.table._capacity, initial_capacity)
        # every key must still be retrievable correctly after rehashing
        for key in range(20):
            self.assertEqual(self.table.search(key), key * key)
        self.assertEqual(len(self.table), 20)

    def test_handles_many_keys_matching_reference_dict(self) -> None:
        reference = {key: f"value-{key}" for key in range(200)}
        for key, value in reference.items():
            self.table.insert(key, value)
        for key, value in reference.items():
            self.assertEqual(self.table.search(key), value)
        self.assertEqual(len(self.table), len(reference))


if __name__ == "__main__":
    unittest.main(verbosity=2)