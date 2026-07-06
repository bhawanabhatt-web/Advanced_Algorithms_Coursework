from __future__ import annotations
import random
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from Task2.graph import Graph 
from parallel_bfs import parallel_bfs  
from sequential_bfs import sequential_bfs 

def _build_line_graph(num_vertices: int) -> Graph:
    """Build an undirected 0-1-2-...-(n-1) path graph."""
    graph = Graph(num_vertices=num_vertices, directed=False)
    for vertex in range(num_vertices - 1):
        graph.add_edge(vertex, vertex + 1, 1.0)
    return graph

def _build_random_graph(num_vertices: int, edge_probability: float, seed: int) -> Graph:
    """Build a reproducible random undirected graph."""
    rng = random.Random(seed)
    graph = Graph(num_vertices=num_vertices, directed=False)
    for u in range(num_vertices):
        for v in range(u + 1, num_vertices):
            if rng.random() < edge_probability:
                graph.add_edge(u, v, 1.0)
    return graph

class TestParallelBFS(unittest.TestCase):
    """Correctness tests for :func:`parallel_bfs`."""

    def test_source_out_of_range_raises_value_error(self) -> None:
        graph = _build_line_graph(3)
        with self.assertRaises(ValueError):
            parallel_bfs(graph, source=99)

    def test_non_positive_num_threads_raises_value_error(self) -> None:
        graph = _build_line_graph(3)
        with self.assertRaises(ValueError):
            parallel_bfs(graph, source=0, num_threads=0)
        with self.assertRaises(ValueError):
            parallel_bfs(graph, source=0, num_threads=-2)

    def test_single_vertex_graph(self) -> None:
        graph = Graph(num_vertices=1, directed=False)
        result = parallel_bfs(graph, source=0, num_threads=4)
        self.assertEqual(result.visit_order, [0])

    def test_visits_every_vertex_in_a_connected_graph(self) -> None:
        graph = _build_line_graph(20)
        result = parallel_bfs(graph, source=0, num_threads=4)
        self.assertEqual(result.num_visited, 20)
        self.assertEqual(sorted(result.visit_order), list(range(20)))

    def test_matches_sequential_bfs_visited_set_on_random_graphs(self) -> None:
        for seed in range(5):
            graph = _build_random_graph(num_vertices=60, edge_probability=0.1, seed=seed)
            sequential_result = sequential_bfs(graph, source=0)
            parallel_result = parallel_bfs(graph, source=0, num_threads=4)
            self.assertEqual(
                sequential_result.visited, parallel_result.visited,
                msg=f"Mismatch for seed={seed}",
            )

    def test_works_with_more_threads_than_frontier_vertices(self) -> None:
        # A star graph's first frontier has only 1 vertex; requesting many
        # threads must not crash (chunking degrades gracefully to 1 chunk).
        graph = Graph(num_vertices=5, directed=False)
        for v in range(1, 5):
            graph.add_edge(0, v, 1.0)
        result = parallel_bfs(graph, source=0, num_threads=16)
        self.assertEqual(result.num_visited, 5)

    def test_disconnected_vertices_are_not_visited(self) -> None:
        graph = Graph(num_vertices=4, directed=False)
        graph.add_edge(0, 1, 1.0)
        graph.add_edge(2, 3, 1.0)
        result = parallel_bfs(graph, source=0, num_threads=2)
        self.assertEqual(result.num_visited, 2)
        self.assertFalse(result.visited[2])
        self.assertFalse(result.visited[3])

if __name__ == "__main__":
    unittest.main(verbosity=2)