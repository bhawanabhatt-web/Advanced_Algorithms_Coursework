from __future__ import annotations
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from packing import Bin, Item, PackingResult  

class TestItem(unittest.TestCase):
    """Validation tests for the :class:`Item` dataclass."""

    def test_empty_dimensions_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            Item(dimensions=())

    def test_non_positive_dimension_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            Item(dimensions=(0.5, 0.0, 0.2))
        with self.assertRaises(ValueError):
            Item(dimensions=(0.5, -0.1, 0.2))

    def test_total_size_sums_dimensions(self) -> None:
        item = Item(dimensions=(0.2, 0.3, 0.1))
        self.assertAlmostEqual(item.total_size, 0.6)


class TestBin(unittest.TestCase):
    """Correctness tests for :class:`Bin`."""

    def test_fits_returns_true_within_capacity(self) -> None:
        bin_ = Bin(capacity=(1.0, 1.0), load=[0.5, 0.5])
        self.assertTrue(bin_.fits(Item((0.3, 0.3))))

    def test_fits_returns_false_when_exceeding_capacity(self) -> None:
        bin_ = Bin(capacity=(1.0, 1.0), load=[0.8, 0.8])
        self.assertFalse(bin_.fits(Item((0.3, 0.3))))

    def test_add_updates_load_and_indices(self) -> None:
        bin_ = Bin(capacity=(1.0,), load=[0.0])
        bin_.add(0, Item((0.4,)))
        self.assertEqual(bin_.item_indices, [0])
        self.assertAlmostEqual(bin_.load[0], 0.4)

    def test_add_raises_value_error_when_item_does_not_fit(self) -> None:
        bin_ = Bin(capacity=(1.0,), load=[0.9])
        with self.assertRaises(ValueError):
            bin_.add(0, Item((0.5,)))

    def test_remove_updates_load_and_indices(self) -> None:
        bin_ = Bin(capacity=(1.0,), load=[0.0])
        item = Item((0.4,))
        bin_.add(0, item)
        bin_.remove(0, item)
        self.assertEqual(bin_.item_indices, [])
        self.assertAlmostEqual(bin_.load[0], 0.0)

    def test_remove_missing_item_raises_value_error(self) -> None:
        bin_ = Bin(capacity=(1.0,), load=[0.0])
        with self.assertRaises(ValueError):
            bin_.remove(0, Item((0.4,)))

    def test_is_empty(self) -> None:
        bin_ = Bin(capacity=(1.0,), load=[0.0])
        self.assertTrue(bin_.is_empty())
        bin_.add(0, Item((0.4,)))
        self.assertFalse(bin_.is_empty())

    def test_copy_is_independent(self) -> None:
        original = Bin(capacity=(1.0,), load=[0.0])
        original.add(0, Item((0.4,)))
        duplicate = original.copy()
        duplicate.add(1, Item((0.3,)))
        self.assertEqual(original.item_indices, [0])
        self.assertEqual(duplicate.item_indices, [0, 1])


class TestPackingResult(unittest.TestCase):
    """Correctness tests for :class:`PackingResult`."""

    def test_num_bins(self) -> None:
        result = PackingResult(bins=[Bin(), Bin()])
        self.assertEqual(result.num_bins, 2)

    def test_is_feasible_true_for_valid_packing(self) -> None:
        items = [Item((0.5,)), Item((0.4,))]
        bin_ = Bin(capacity=(1.0,), load=[0.0])
        bin_.add(0, items[0])
        bin_.add(1, items[1])
        result = PackingResult(bins=[bin_])
        self.assertTrue(result.is_feasible(items))

    def test_is_feasible_false_when_item_missing(self) -> None:
        items = [Item((0.5,)), Item((0.4,))]
        bin_ = Bin(capacity=(1.0,), load=[0.0])
        bin_.add(0, items[0])  # item 1 never placed
        result = PackingResult(bins=[bin_])
        self.assertFalse(result.is_feasible(items))

if __name__ == "__main__":
    unittest.main(verbosity=2)