from __future__ import annotations
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Task2.graph import Graph  
from sequential_bfs import sequential_bfs 

def _build_line_graph(num_vertices: int) -> Graph:
    """Build an undirected 0-1-2-...-(n-1) path graph."""
    graph = Graph(num_vertices=num_vertices, directed=False)
    for vertex in range(num_vertices - 1):
        graph.add_edge(vertex, vertex + 1, 1.0)
    return graph


class TestSequentialBFS(unittest.TestCase):
    """Correctness tests for :func:`sequential_bfs`."""

    def test_source_out_of_range_raises_value_error(self) -> None:
        graph = _build_line_graph(3)
        with self.assertRaises(ValueError):
            sequential_bfs(graph, source=99)

    def test_single_vertex_graph(self) -> None:
        graph = Graph(num_vertices=1, directed=False)
        result = sequential_bfs(graph, source=0)
        self.assertEqual(result.visit_order, [0])
        self.assertEqual(result.num_visited, 1)

    def test_visits_every_vertex_in_a_connected_graph(self) -> None:
        graph = _build_line_graph(6)
        result = sequential_bfs(graph, source=0)
        self.assertEqual(result.num_visited, 6)
        self.assertEqual(sorted(result.visit_order), list(range(6)))

    def test_visit_order_respects_bfs_levels(self) -> None:
        # Star graph: 0 connects directly to 1, 2, 3; BFS must visit all
        # three before any second-level vertex.
        graph = Graph(num_vertices=5, directed=False)
        graph.add_edge(0, 1, 1.0)
        graph.add_edge(0, 2, 1.0)
        graph.add_edge(0, 3, 1.0)
        graph.add_edge(1, 4, 1.0)  # second-level vertex

        result = sequential_bfs(graph, source=0)
        index_of_4 = result.visit_order.index(4)
        for first_level_vertex in (1, 2, 3):
            self.assertLess(result.visit_order.index(first_level_vertex), index_of_4)

    def test_disconnected_vertices_are_not_visited(self) -> None:
        graph = Graph(num_vertices=4, directed=False)
        graph.add_edge(0, 1, 1.0)
        # vertices 2, 3 form a separate, unreachable component
        graph.add_edge(2, 3, 1.0)

        result = sequential_bfs(graph, source=0)
        self.assertEqual(result.num_visited, 2)
        self.assertFalse(result.visited[2])
        self.assertFalse(result.visited[3])


if __name__ == "__main__":
    unittest.main(verbosity=2)