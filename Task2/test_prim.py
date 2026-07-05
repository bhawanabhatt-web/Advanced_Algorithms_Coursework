from __future__ import annotations
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from graph import Graph  
from prim import prim_mst  

class TestPrim(unittest.TestCase):
    """Correctness tests for :func:`prim_mst`."""

    def test_simple_connected_graph_known_weight(self) -> None:
        graph = Graph(num_vertices=4, directed=False)
        graph.add_edge(0, 1, 1.0)
        graph.add_edge(1, 2, 2.0)
        graph.add_edge(2, 3, 3.0)
        graph.add_edge(0, 3, 10.0)  # should NOT be selected by the MST

        result = prim_mst(graph, source=0)
        self.assertTrue(result.is_connected)
        self.assertEqual(result.total_weight, 6.0)
        self.assertEqual(len(result.mst_edges), 3)  # V - 1 edges for a connected graph

    def test_mst_has_exactly_v_minus_1_edges_for_connected_graph(self) -> None:
        graph = Graph(num_vertices=6, directed=False)
        for u, v, w in [
            (0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2),
            (2, 3, 4), (3, 4, 2), (4, 5, 6),
        ]:
            graph.add_edge(u, v, w)

        result = prim_mst(graph, source=0)
        self.assertEqual(len(result.mst_edges), 5)
        self.assertTrue(result.is_connected)

    def test_disconnected_graph_reports_not_connected(self) -> None:
        graph = Graph(num_vertices=4, directed=False)
        graph.add_edge(0, 1, 1.0)
        # vertices 2 and 3 form a separate component, unreachable from 0
        graph.add_edge(2, 3, 1.0)

        result = prim_mst(graph, source=0)
        self.assertFalse(result.is_connected)
        self.assertEqual(len(result.mst_edges), 1)  # only the 0-1 edge is reachable

    def test_single_vertex_graph_has_zero_weight(self) -> None:
        graph = Graph(num_vertices=1, directed=False)
        result = prim_mst(graph, source=0)
        self.assertEqual(result.total_weight, 0.0)
        self.assertEqual(result.mst_edges, [])
        self.assertTrue(result.is_connected)

    def test_source_out_of_range_raises_value_error(self) -> None:
        graph = Graph(num_vertices=3, directed=False)
        with self.assertRaises(ValueError):
            prim_mst(graph, source=99)


if __name__ == "__main__":
    unittest.main(verbosity=2)