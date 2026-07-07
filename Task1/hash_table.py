from __future__ import annotations
from typing import Generic, Optional, TypeVar
V = TypeVar("V")
__all__ = ["HashTable"]

_DEFAULT_CAPACITY = 16
_MAX_LOAD_FACTOR = 0.75

class HashTable(Generic[V]):
    
    def __init__(self, initial_capacity: int = _DEFAULT_CAPACITY) -> None:
        
        if initial_capacity <= 0:
            raise ValueError(f"'initial_capacity' must be positive, got {initial_capacity}.")
        self._capacity = initial_capacity
        self._size = 0
        self._buckets: list[list[tuple[int, V]]] = [[] for _ in range(initial_capacity)]

    def __len__(self) -> int:
        """Return the number of key-value pairs currently stored."""
        return self._size

    def __contains__(self, key: int) -> bool:
        """Return ``True`` if ``key`` exists in the table."""
        bucket = self._buckets[self._hash(key)]
        return any(existing_key == key for existing_key, _ in bucket)

    @property
    def load_factor(self) -> float:
        """Return the current ``size / capacity`` ratio."""
        return self._size / self._capacity

    def insert(self, key: int, value: V) -> None:
        
        if self.load_factor > _MAX_LOAD_FACTOR:
            self._resize(self._capacity * 2)

        bucket = self._buckets[self._hash(key)]
        for index, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[index] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1

    def search(self, key: int) -> Optional[V]:
        
        bucket = self._buckets[self._hash(key)]
        for existing_key, value in bucket:
            if existing_key == key:
                return value
        return None

    def delete(self, key: int) -> bool:
        
        bucket = self._buckets[self._hash(key)]
        for index, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                del bucket[index]
                self._size -= 1
                return True
        return False

    def _hash(self, key: int) -> int:
        """Map ``key`` to a bucket index using Python's built-in hash."""
        return hash(key) % self._capacity

    def _resize(self, new_capacity: int) -> None:
        
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._buckets = [[] for _ in range(new_capacity)]
        self._size = 0
        for bucket in old_buckets:
            for key, value in bucket:
                self.insert(key, value)