from __future__ import annotations
import sys
from pathlib import Path
from common.utils import get_logger   
from graph import Graph  
from dijkstra import dijkstra
from prim import prim_mst

logger = get_logger(__name__)


def build_demo_directed_graph() -> Graph:
    """Build the small textbook-style directed graph used for Dijkstra/Bellman-Ford demos."""
    graph = Graph(num_vertices=5, directed=True)
    for u, v, w in [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3)]:
        graph.add_edge(u, v, w)
    return graph


def build_demo_undirected_graph() -> Graph:
    """Build a small undirected graph used for the Prim MST demo."""
    graph = Graph(num_vertices=5, directed=False)
    for u, v, w in [
        (0, 1, 2), (0, 3, 6), (1, 2, 3), (1, 3, 8), (1, 4, 5), (2, 4, 7), (3, 4, 9),
    ]:
        graph.add_edge(u, v, w)
    return graph


def build_demo_negative_cycle_graph() -> Graph:
    """Build a small directed graph containing a negative-weight cycle."""
    graph = Graph(num_vertices=4, directed=True)
    graph.add_edge(0, 1, 1.0)
    graph.add_edge(1, 2, -1.0)
    graph.add_edge(2, 3, -1.0)
    graph.add_edge(3, 1, -1.0)  
    return graph


def demonstrate_dijkstra() -> None:
    """Run Dijkstra on a small directed graph and print the shortest paths."""
    logger.info("--- Dijkstra's Algorithm ---")
    graph = build_demo_directed_graph()
    result = dijkstra(graph, source=0)
    logger.info("Distances from vertex 0: %s", result.distances)
    logger.info("Shortest path 0 -> 4: %s", result.path_to(4))


def demonstrate_prim() -> None:
    """Run Prim on a small undirected graph and print the resulting MST."""
    logger.info("--- Prim's Algorithm (Minimum Spanning Tree) ---")
    graph = build_demo_undirected_graph()
    result = prim_mst(graph, source=0)
    logger.info("MST total weight: %s", result.total_weight)
    logger.info("MST edges: %s", result.mst_edges)
    logger.info("Spans every vertex: %s", result.is_connected)


def demonstrate_bellman_ford() -> None:
    """Run Bellman-Ford on both a normal graph and one with a negative cycle."""
    logger.info("--- Bellman-Ford Algorithm ---")
    graph = build_demo_directed_graph()
    result = bellman_ford(graph, source=0)
    logger.info("Distances from vertex 0: %s", result.distances)
    logger.info("Negative cycle detected: %s", result.has_negative_cycle)

    logger.info("Running Bellman-Ford on a graph with a deliberate negative cycle...")
    cyclic_graph = build_demo_negative_cycle_graph()
    cyclic_result = bellman_ford(cyclic_graph, source=0)
    logger.info("Negative cycle detected: %s", cyclic_result.has_negative_cycle)


def demonstrate_error_handling() -> None:
    """Show that invalid inputs are rejected with clear, informative errors."""
    logger.info("--- Exception Handling Demonstration ---")
    graph = build_demo_directed_graph()
    try:
        dijkstra(graph, source=99)
    except ValueError as exc:
        logger.info("Correctly rejected out-of-range source: %s", exc)

    negative_graph = Graph(num_vertices=2, directed=True)
    negative_graph.add_edge(0, 1, -5.0)
    try:
        dijkstra(negative_graph, source=0)
    except ValueError as exc:
        logger.info("Correctly rejected negative weight for Dijkstra: %s", exc)


def main() -> None:
    """Run all three graph algorithm demonstrations."""
    demonstrate_dijkstra()
    demonstrate_prim()
    demonstrate_bellman_ford()
    demonstrate_error_handling()
    logger.info(
        "Task 2 demonstration complete. Run 'python -m Task2.benchmark' for performance results."
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:  
        logger.exception("Task 2 demonstration failed.")
        raise