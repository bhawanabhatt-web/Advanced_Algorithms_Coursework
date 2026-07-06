from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  
from Task2.graph import Graph 
from bfs_result import BFSResult 
__all__ = ["sequential_bfs"]

def sequential_bfs(graph: Graph, source: int) -> BFSResult:
    if not 0 <= source < graph.num_vertices:
        raise ValueError(f"Source vertex {source} is out of range.")

    visited = [False] * graph.num_vertices
    visited[source] = True
    visit_order = [source]
    frontier = [source]

    while frontier:
        next_frontier: list[int] = []
        for vertex in frontier:
            for neighbour, _weight in graph.neighbors(vertex):
                if not visited[neighbour]:
                    visited[neighbour] = True
                    visit_order.append(neighbour)
                    next_frontier.append(neighbour)
        frontier = next_frontier

    return BFSResult(source=source, visit_order=visit_order, visited=visited)