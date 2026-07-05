from __future__ import annotations
import heapq
from graph import Graph, ShortestPathResult

__all__ = ["dijkstra"]

def dijkstra(graph: Graph, source: int) -> ShortestPathResult:
    if not 0 <= source < graph.num_vertices:
        raise ValueError(f"Source vertex {source} is out of range.")
    for u, v, weight in graph.edges:
        if weight < 0:
            raise ValueError(
                f"Dijkstra's algorithm requires non-negative weights; "
                f"found edge ({u} -> {v}) with weight {weight}. "
                "Use bellman_ford() for graphs with negative weights."
            )

    distances = [float("inf")] * graph.num_vertices
    predecessors: list[int | None] = [None] * graph.num_vertices
    distances[source] = 0.0
    visited = [False] * graph.num_vertices

    priority_queue: list[tuple[float, int]] = [(0.0, source)]
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        if visited[current_vertex]:
            continue
        visited[current_vertex] = True

        for neighbour, weight in graph.neighbors(current_vertex):
            if visited[neighbour]:
                continue
            new_distance = current_distance + weight
            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                predecessors[neighbour] = current_vertex
                heapq.heappush(priority_queue, (new_distance, neighbour))

    return ShortestPathResult(source=source, distances=distances, predecessors=predecessors)