from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

V = TypeVar("V")

__all__ = ["MinHeap"]


@dataclass(frozen=True, slots=True)
class _HeapEntry(Generic[V]):
    """A single ``(priority, value)`` pair stored in the heap."""

    priority: float
    value: V


class MinHeap(Generic[V]):
    
    def __init__(self) -> None:
        self._entries: list[_HeapEntry[V]] = []

    def __len__(self) -> int:
        """Return the number of items currently in the heap."""
        return len(self._entries)

    def is_empty(self) -> bool:
        """Return ``True`` if the heap contains no items."""
        return len(self._entries) == 0

    def push(self, priority: float, value: V) -> None:
        """Insert ``value`` with the given ``priority``.

        Args:
            priority: The priority key; smaller values are popped first.
            value: The value to store.
        """
        self._entries.append(_HeapEntry(priority, value))
        self._sift_up(len(self._entries) - 1)

    def pop(self) -> tuple[float, V]:
       
        if self.is_empty():
            raise IndexError("pop from an empty MinHeap")

        top = self._entries[0]
        last = self._entries.pop()
        if self._entries:
            self._entries[0] = last
            self._sift_down(0)
        return top.priority, top.value

    def peek(self) -> tuple[float, V]:
        
        if self.is_empty():
            raise IndexError("peek at an empty MinHeap")
        top = self._entries[0]
        return top.priority, top.value

    def _sift_up(self, index: int) -> None:
        """Restore the heap invariant by moving the entry at ``index`` upward."""
        while index > 0:
            parent = (index - 1) // 2
            if self._entries[index].priority < self._entries[parent].priority:
                self._entries[index], self._entries[parent] = (
                    self._entries[parent],
                    self._entries[index],
                )
                index = parent
            else:
                break

    def _sift_down(self, index: int) -> None:
        """Restore the heap invariant by moving the entry at ``index`` downward."""
        size = len(self._entries)
        while True:
            left, right = 2 * index + 1, 2 * index + 2
            smallest = index
            if left < size and self._entries[left].priority < self._entries[smallest].priority:
                smallest = left
            if right < size and self._entries[right].priority < self._entries[smallest].priority:
                smallest = right
            if smallest == index:
                break
            self._entries[index], self._entries[smallest] = (
                self._entries[smallest],
                self._entries[index],
            )
            index = smallest