from __future__ import annotations
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from graph import Graph, MSTResult, ShortestPathResult  # noqa: E402


class TestGraph(unittest.TestCase):
    """Correctness tests for :class:`Graph`."""

    def test_invalid_num_vertices_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            Graph(num_vertices=0)
        with self.assertRaises(ValueError):
            Graph(num_vertices=-3)

    def test_len_returns_vertex_count(self) -> None:
        graph = Graph(num_vertices=5)
        self.assertEqual(len(graph), 5)

    def test_directed_edge_only_adds_one_direction(self) -> None:
        graph = Graph(num_vertices=2, directed=True)
        graph.add_edge(0, 1, 3.0)
        self.assertEqual(graph.neighbors(0), [(1, 3.0)])
        self.assertEqual(graph.neighbors(1), [])

    def test_undirected_edge_adds_both_directions(self) -> None:
        graph = Graph(num_vertices=2, directed=False)
        graph.add_edge(0, 1, 3.0)
        self.assertEqual(graph.neighbors(0), [(1, 3.0)])
        self.assertEqual(graph.neighbors(1), [(0, 3.0)])

    def test_edges_property_records_one_entry_per_add_edge_call(self) -> None:
        graph = Graph(num_vertices=3, directed=False)
        graph.add_edge(0, 1, 1.0)
        graph.add_edge(1, 2, 2.0)
        self.assertEqual(graph.edges, [(0, 1, 1.0), (1, 2, 2.0)])

    def test_add_edge_out_of_range_vertex_raises_value_error(self) -> None:
        graph = Graph(num_vertices=3)
        with self.assertRaises(ValueError):
            graph.add_edge(0, 5, 1.0)
        with self.assertRaises(ValueError):
            graph.add_edge(-1, 1, 1.0)

    def test_self_loop_raises_value_error(self) -> None:
        graph = Graph(num_vertices=3)
        with self.assertRaises(ValueError):
            graph.add_edge(1, 1, 1.0)

    def test_neighbors_out_of_range_raises_value_error(self) -> None:
        graph = Graph(num_vertices=3)
        with self.assertRaises(ValueError):
            graph.neighbors(10)

    def test_negative_weight_edges_are_allowed(self) -> None:
        graph = Graph(num_vertices=2)
        graph.add_edge(0, 1, -5.0)  # Graph itself does not forbid this
        self.assertEqual(graph.neighbors(0), [(1, -5.0)])


class TestShortestPathResult(unittest.TestCase):
    """Correctness tests for :class:`ShortestPathResult.path_to`."""

    def test_path_to_reconstructs_correct_route(self) -> None:
        # 0 -> 1 -> 2, distances/predecessors as Dijkstra would produce them.
        result = ShortestPathResult(
            source=0,
            distances=[0.0, 4.0, 6.0],
            predecessors=[None, 0, 1],
        )
        self.assertEqual(result.path_to(2), [0, 1, 2])

    def test_path_to_unreachable_vertex_returns_empty_list(self) -> None:
        result = ShortestPathResult(
            source=0,
            distances=[0.0, float("inf")],
            predecessors=[None, None],
        )
        self.assertEqual(result.path_to(1), [])

    def test_path_to_source_itself(self) -> None:
        result = ShortestPathResult(source=0, distances=[0.0], predecessors=[None])
        self.assertEqual(result.path_to(0), [0])


class TestMSTResult(unittest.TestCase):
    """Basic construction test for :class:`MSTResult`."""

    def test_default_fields(self) -> None:
        result = MSTResult(total_weight=10.0)
        self.assertEqual(result.mst_edges, [])
        self.assertTrue(result.is_connected)


if __name__ == "__main__":
    unittest.main(verbosity=2)