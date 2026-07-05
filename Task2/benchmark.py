from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  

from common.excel_export import export_to_excel  
from common.generator import random_weighted_edges  
from common.plotting import plot_line_comparison  
from common.timer import BenchmarkResult, benchmark  
from common.utils import EXCEL_DIR, PLOTS_DIR, RAW_DATA_DIR, export_to_csv, get_logger  
from bellman_ford import bellman_ford  
from dijkstra import dijkstra  
from graph import Graph 
from prim import prim_mst  

logger = get_logger(__name__)

DATASET_SIZES: tuple[int, ...] = (50, 200, 500)
REPEATS: int = 5
SEED: int = 42


def generate_dijkstra_graph(num_vertices: int, seed: int = SEED) -> Graph:
    
    graph = Graph(num_vertices=num_vertices, directed=True)
    for u, v, w in random_weighted_edges(
        num_vertices, edge_probability=0.05, weight_range=(1, 50), directed=True, seed=seed
    ):
        graph.add_edge(u, v, w)
    return graph


def generate_undirected_graph(num_vertices: int, seed: int = SEED) -> Graph:
    
    graph = Graph(num_vertices=num_vertices, directed=False)
    for u, v, w in random_weighted_edges(
        num_vertices, edge_probability=0.08, weight_range=(1, 50), directed=False, seed=seed
    ):
        graph.add_edge(u, v, w)
    return graph


def generate_bellman_ford_graph(num_vertices: int, seed: int = SEED) -> Graph:
    
    graph = Graph(num_vertices=num_vertices, directed=True)
    for u, v, w in random_weighted_edges(
        num_vertices, edge_probability=0.03, weight_range=(-10, 50), directed=True, seed=seed
    ):
        graph.add_edge(u, v, w)
    return graph


def benchmark_all_algorithms(num_vertices: int) -> dict[str, BenchmarkResult]:
    
    dijkstra_graph = generate_dijkstra_graph(num_vertices)
    undirected_graph = generate_undirected_graph(num_vertices)
    bellman_ford_graph = generate_bellman_ford_graph(num_vertices)

    return {
        "Dijkstra": benchmark(
            dijkstra, dijkstra_graph, 0, repeats=REPEATS, label="Dijkstra", input_size=num_vertices
        ),
        "Prim": benchmark(
            prim_mst, undirected_graph, 0, repeats=REPEATS, label="Prim", input_size=num_vertices
        ),
        "BellmanFord": benchmark(
            bellman_ford,
            bellman_ford_graph,
            0,
            repeats=REPEATS,
            label="Bellman-Ford",
            input_size=num_vertices,
        ),
    }


def run() -> None:
    """Run the full Task 2 benchmark suite and export results and plots."""
    logger.info("Starting Task 2 benchmark suite (sizes=%s, repeats=%d)", DATASET_SIZES, REPEATS)

    records: list[dict[str, object]] = []
    for num_vertices in DATASET_SIZES:
        logger.info("Benchmarking graphs with %d vertices...", num_vertices)
        results = benchmark_all_algorithms(num_vertices)
        for algorithm_name, result in results.items():
            logger.info(
                "  %-12s mean=%.6es std=%.2es", algorithm_name, result.mean, result.std_dev
            )
            records.append({"algorithm": algorithm_name, **result.to_dict()})

    logger.info("Exporting raw results to CSV and Excel...")
    export_to_csv(records, RAW_DATA_DIR / "task2_benchmark.csv")
    export_to_excel(EXCEL_DIR / "task2_benchmark.xlsx", {"GraphAlgorithms": records})

    logger.info("Generating plots...")
    lookup = {(r["algorithm"], r["input_size"]): r["mean_time_s"] for r in records}
    series = {
        name: [lookup[(name, n)] for n in DATASET_SIZES]
        for name in ("Dijkstra", "Prim", "BellmanFord")
    }
    plot_line_comparison(
        x_values=list(DATASET_SIZES),
        series=series,
        title="Task 2: Algorithm Runtime vs. Graph Size",
        x_label="Number of vertices (V)",
        y_label="Mean execution time (s)",
        output_path=PLOTS_DIR / "task2_runtime_comparison.png",
        log_scale_y=True,
    )

    logger.info("Task 2 benchmark suite complete. See results/ for outputs.")


if __name__ == "__main__":
    try:
        run()
    except Exception:  
        logger.exception("Task 2 benchmark suite failed.")
        raise