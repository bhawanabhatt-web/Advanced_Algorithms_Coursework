from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

__all__ = ["Graph", "ShortestPathResult", "MSTResult"]

class Graph:
    
    def __init__(self, num_vertices: int, directed: bool = True) -> None:
        
        if num_vertices <= 0:
            raise ValueError(f"'num_vertices' must be positive, got {num_vertices}.")
        self.num_vertices = num_vertices
        self.directed = directed
        self._adjacency: list[list[tuple[int, float]]] = [[] for _ in range(num_vertices)]
        self._edges: list[tuple[int, int, float]] = []

    def __len__(self) -> int:
        """Return the number of vertices in the graph."""
        return self.num_vertices

    @property
    def edges(self) -> list[tuple[int, int, float]]:
        
        return list(self._edges)

    def neighbors(self, vertex: int) -> list[tuple[int, float]]:
        
        self._validate_vertex(vertex)
        return list(self._adjacency[vertex])

    def add_edge(self, source: int, target: int, weight: float) -> None:
        
        self._validate_vertex(source)
        self._validate_vertex(target)
        if source == target:
            raise ValueError(f"Self-loops are not supported (source == target == {source}).")

        self._adjacency[source].append((target, weight))
        self._edges.append((source, target, weight))
        if not self.directed:
            self._adjacency[target].append((source, weight))

    def _validate_vertex(self, vertex: int) -> None:
        """Raise ``ValueError`` if ``vertex`` is not a valid vertex index."""
        if not 0 <= vertex < self.num_vertices:
            raise ValueError(
                f"Vertex {vertex} is out of range for a graph with {self.num_vertices} vertices."
            )


@dataclass
class ShortestPathResult:
    
    source: int
    distances: list[float]
    predecessors: list[Optional[int]]
    has_negative_cycle: bool = False

    def path_to(self, target: int) -> list[int]:
    
        if self.distances[target] == float("inf"):
            return []
        path = [target]
        while path[-1] != self.source:
            predecessor = self.predecessors[path[-1]]
            if predecessor is None:
                return []  
            path.append(predecessor)
        path.reverse()
        return path


@dataclass
class MSTResult:
    total_weight: float
    mst_edges: list[tuple[int, int, float]] = field(default_factory=list)
    is_connected: bool = True