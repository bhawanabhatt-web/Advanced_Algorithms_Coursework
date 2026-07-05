from __future__ import annotations
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from bellman_ford import bellman_ford  
from dijkstra import dijkstra 
from graph import Graph  

class TestBellmanFord(unittest.TestCase):
    """Correctness tests for :func:`bellman_ford`."""

    def test_agrees_with_dijkstra_on_non_negative_graph(self) -> None:
        graph = Graph(num_vertices=5, directed=True)
        for u, v, w in [
            (0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3),
        ]:
            graph.add_edge(u, v, w)

        dijkstra_result = dijkstra(graph, source=0)
        bf_result = bellman_ford(graph, source=0)
        self.assertEqual(dijkstra_result.distances, bf_result.distances)
        self.assertFalse(bf_result.has_negative_cycle)

    def test_handles_negative_weights_correctly(self) -> None:
        graph = Graph(num_vertices=3, directed=True)
        graph.add_edge(0, 1, 4.0)
        graph.add_edge(0, 2, 5.0)
        graph.add_edge(1, 2, -3.0)  # negative edge, but no cycle

        result = bellman_ford(graph, source=0)
        self.assertFalse(result.has_negative_cycle)
        self.assertEqual(result.distances[2], 1.0)  # via 0 -> 1 -> 2 = 4 - 3

    def test_detects_negative_cycle(self) -> None:
        graph = Graph(num_vertices=4, directed=True)
        graph.add_edge(0, 1, 1.0)
        graph.add_edge(1, 2, -1.0)
        graph.add_edge(2, 3, -1.0)
        graph.add_edge(3, 1, -1.0)  # 1 -> 2 -> 3 -> 1 has total weight -3

        result = bellman_ford(graph, source=0)
        self.assertTrue(result.has_negative_cycle)

    def test_no_negative_cycle_when_negative_edge_is_unreachable(self) -> None:
        graph = Graph(num_vertices=4, directed=True)
        graph.add_edge(0, 1, 1.0)
        # Vertices 2, 3 form a negative cycle unreachable from source 0.
        graph.add_edge(2, 3, -5.0)
        graph.add_edge(3, 2, -5.0)

        result = bellman_ford(graph, source=0)
        self.assertFalse(result.has_negative_cycle)

    def test_source_out_of_range_raises_value_error(self) -> None:
        graph = Graph(num_vertices=3)
        with self.assertRaises(ValueError):
            bellman_ford(graph, source=99)


if __name__ == "__main__":
    unittest.main(verbosity=2)