from __future__ import annotations
from graph import Graph, ShortestPathResult
__all__ = ["bellman_ford"]

def bellman_ford(graph: Graph, source: int) -> ShortestPathResult:
    
    if not 0 <= source < graph.num_vertices:
        raise ValueError(f"Source vertex {source} is out of range.")

    distances = [float("inf")] * graph.num_vertices
    predecessors: list[int | None] = [None] * graph.num_vertices
    distances[source] = 0.0

    edges = graph.edges
    for _ in range(graph.num_vertices - 1):
        relaxed_any = False
        for u, v, weight in edges:
            if distances[u] != float("inf") and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                predecessors[v] = u
                relaxed_any = True
        if not relaxed_any:
            break  # early exit: no more improvements possible

    has_negative_cycle = False
    for u, v, weight in edges:
        if distances[u] != float("inf") and distances[u] + weight < distances[v]:
            has_negative_cycle = True
            break

    return ShortestPathResult(
        source=source,
        distances=distances,
        predecessors=predecessors,
        has_negative_cycle=has_negative_cycle,
    )