from __future__ import annotations

import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from dijkstra import dijkstra  
from graph import Graph  


class TestDijkstra(unittest.TestCase):
    """Correctness tests for :func:`dijkstra`."""

    def test_simple_graph_known_distances(self) -> None:
        # Classic textbook example graph.
        graph = Graph(num_vertices=5, directed=True)
        for u, v, w in [
            (0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3),
        ]:
            graph.add_edge(u, v, w)

        result = dijkstra(graph, source=0)
        self.assertEqual(result.distances, [0, 3, 1, 4, 7])

    def test_unreachable_vertex_has_infinite_distance(self) -> None:
        graph = Graph(num_vertices=3, directed=True)
        graph.add_edge(0, 1, 1.0)
        # vertex 2 has no incoming edge -> unreachable from 0
        result = dijkstra(graph, source=0)
        self.assertEqual(result.distances[2], float("inf"))

    def test_source_out_of_range_raises_value_error(self) -> None:
        graph = Graph(num_vertices=3)
        with self.assertRaises(ValueError):
            dijkstra(graph, source=99)

    def test_negative_weight_raises_value_error(self) -> None:
        graph = Graph(num_vertices=2, directed=True)
        graph.add_edge(0, 1, -3.0)
        with self.assertRaises(ValueError):
            dijkstra(graph, source=0)

    def test_path_to_reconstructs_shortest_route(self) -> None:
        graph = Graph(num_vertices=4, directed=True)
        graph.add_edge(0, 1, 1.0)
        graph.add_edge(1, 2, 1.0)
        graph.add_edge(0, 2, 5.0)  # longer direct route
        graph.add_edge(2, 3, 1.0)

        result = dijkstra(graph, source=0)
        self.assertEqual(result.path_to(3), [0, 1, 2, 3])

    def test_single_vertex_graph(self) -> None:
        graph = Graph(num_vertices=1)
        result = dijkstra(graph, source=0)
        self.assertEqual(result.distances, [0.0])


if __name__ == "__main__":
    unittest.main(verbosity=2)