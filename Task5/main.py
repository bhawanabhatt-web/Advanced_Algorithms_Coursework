from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  
from common.utils import get_logger  
from Task2.graph import Graph  
from parallel_bfs import parallel_bfs  
from sequential_bfs import sequential_bfs  

logger = get_logger(__name__)

def build_demo_graph() -> Graph:
    """Build a small undirected demo graph shaped like two connected clusters."""
    graph = Graph(num_vertices=8, directed=False)
    for u, v in [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (6, 7)]:
        graph.add_edge(u, v, 1.0)
    return graph

def demonstrate_sequential_bfs(graph: Graph) -> None:
    """Run sequential BFS from vertex 0 and print the visit order."""
    logger.info("--- Sequential BFS ---")
    result = sequential_bfs(graph, source=0)
    logger.info("Visit order: %s", result.visit_order)
    logger.info("Vertices reached: %d / %d", result.num_visited, graph.num_vertices)

def demonstrate_parallel_bfs(graph: Graph) -> None:
    """Run parallel BFS with 4 threads and confirm it agrees with sequential BFS."""
    logger.info("--- Parallel BFS (4 threads) ---")
    result = parallel_bfs(graph, source=0, num_threads=4)
    logger.info("Visit order: %s", result.visit_order)
    logger.info("Vertices reached: %d / %d", result.num_visited, graph.num_vertices)

    sequential_result = sequential_bfs(graph, source=0)
    logger.info(
        "Agrees with sequential BFS on which vertices were reached: %s",
        sequential_result.visited == result.visited,
    )

def demonstrate_error_handling() -> None:
    """Show that invalid inputs are rejected with clear, informative errors."""
    logger.info("--- Exception Handling Demonstration ---")
    graph = build_demo_graph()
    try:
        sequential_bfs(graph, source=99)
    except ValueError as exc:
        logger.info("Correctly rejected out-of-range source: %s", exc)

    try:
        parallel_bfs(graph, source=0, num_threads=0)
    except ValueError as exc:
        logger.info("Correctly rejected non-positive num_threads: %s", exc)

def main() -> None:
    """Run both BFS demonstrations."""
    graph = build_demo_graph()
    demonstrate_sequential_bfs(graph)
    demonstrate_parallel_bfs(graph)
    demonstrate_error_handling()
    logger.info(
        "Task 5 demonstration complete. Run 'python -m Task5.benchmark' for "
        "performance and scalability results."
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:  
        logger.exception("Task 5 demonstration failed.")
        raise