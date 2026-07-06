from __future__ import annotations
from dataclasses import dataclass, field
__all__ = ["Item", "Bin", "PackingResult", "DEFAULT_CAPACITY"]

DEFAULT_CAPACITY: tuple[float, ...] = (1.0, 1.0, 1.0)
_EPSILON = 1e-9

@dataclass(frozen=True)
class Item:
    dimensions: tuple[float, ...]

    def __post_init__(self) -> None:
        
        if not self.dimensions:
            raise ValueError("An Item must have at least one dimension.")
        if any(value <= 0 for value in self.dimensions):
            raise ValueError(f"All Item dimensions must be positive, got {self.dimensions}.")

    @property
    def total_size(self) -> float:
        """Return the sum of this item's demands across all dimensions."""
        return sum(self.dimensions)

@dataclass
class Bin:
    
    capacity: tuple[float, ...] = DEFAULT_CAPACITY
    item_indices: list[int] = field(default_factory=list)
    load: list[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])

    def fits(self, item: Item) -> bool:
        
        return all(
            self.load[i] + item.dimensions[i] <= self.capacity[i] + _EPSILON
            for i in range(len(self.capacity))
        )

    def add(self, item_index: int, item: Item) -> None:
        
        if not self.fits(item):
            raise ValueError(f"Item {item_index} does not fit in this bin (load={self.load}).")
        self.item_indices.append(item_index)
        for i, demand in enumerate(item.dimensions):
            self.load[i] += demand

    def remove(self, item_index: int, item: Item) -> None:
        
        if item_index not in self.item_indices:
            raise ValueError(f"Item {item_index} is not in this bin.")
        self.item_indices.remove(item_index)
        for i, demand in enumerate(item.dimensions):
            self.load[i] -= demand

    def is_empty(self) -> bool:
        """Return ``True`` if this bin currently holds no items."""
        return len(self.item_indices) == 0

    def copy(self) -> "Bin":
        """Return an independent copy of this bin (new lists, same capacity)."""
        return Bin(
            capacity=self.capacity, item_indices=list(self.item_indices), load=list(self.load)
        )


@dataclass
class PackingResult:
  
    bins: list[Bin]

    @property
    def num_bins(self) -> int:
        """Return the number of bins used."""
        return len(self.bins)

    def is_feasible(self, items: list[Item]) -> bool:
        
        assigned_indices: list[int] = []
        for bin_ in self.bins:
            within_capacity = all(
                bin_.load[i] <= bin_.capacity[i] + _EPSILON for i in range(len(bin_.capacity))
            )
            if not within_capacity:
                return False
            assigned_indices.extend(bin_.item_indices)
        return sorted(assigned_indices) == list(range(len(items)))