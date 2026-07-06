from __future__ import annotations
from dataclasses import dataclass
__all__ = ["BFSResult"]

@dataclass
class BFSResult:
    source: int
    visit_order: list[int]
    visited: list[bool]

    @property
    def num_visited(self) -> int:
        """Return the number of vertices reached from ``source``."""
        return sum(self.visited)