from __future__ import annotations
import heapq
from graph import Graph, MSTResult

__all__ = ["prim_mst"]

def prim_mst(graph: Graph, source: int = 0) -> MSTResult:
    
    if not 0 <= source < graph.num_vertices:
        raise ValueError(f"Source vertex {source} is out of range.")

    visited = [False] * graph.num_vertices
    best_edge_weight: list[float] = [float("inf")] * graph.num_vertices
    best_edge_source: list[int | None] = [None] * graph.num_vertices
    best_edge_weight[source] = 0.0

    priority_queue: list[tuple[float, int]] = [(0.0, source)]
    total_weight = 0.0
    mst_edges: list[tuple[int, int, float]] = []

    while priority_queue:
        weight, vertex = heapq.heappop(priority_queue)
        if visited[vertex]:
            continue
        visited[vertex] = True
        total_weight += weight
        origin = best_edge_source[vertex]
        if origin is not None:
            mst_edges.append((origin, vertex, weight))

        for neighbour, edge_weight in graph.neighbors(vertex):
            if not visited[neighbour] and edge_weight < best_edge_weight[neighbour]:
                best_edge_weight[neighbour] = edge_weight
                best_edge_source[neighbour] = vertex
                heapq.heappush(priority_queue, (edge_weight, neighbour))

    return MSTResult(
        total_weight=total_weight,
        mst_edges=mst_edges,
        is_connected=all(visited),
    )