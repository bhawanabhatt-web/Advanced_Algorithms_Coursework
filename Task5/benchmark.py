from __future__ import annotations
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1])) 
from common.excel_export import export_to_excel  
from common.plotting import plot_line_comparison 
from common.timer import benchmark 
from common.utils import EXCEL_DIR, PLOTS_DIR, RAW_DATA_DIR, export_to_csv, get_logger 
from Task2.graph import Graph 
from parallel_bfs import parallel_bfs 
from sequential_bfs import sequential_bfs 

logger = get_logger(__name__)

GRAPH_SIZE: int = 20_000
EDGE_PROBABILITY: float = 0.0015
THREAD_COUNTS: tuple[int, ...] = (1, 2, 4, 8)
REPEATS: int = 5
SEED: int = 42


def generate_benchmark_graph(
    num_vertices: int = GRAPH_SIZE, edge_probability: float = EDGE_PROBABILITY, seed: int = SEED
) -> Graph:
    rng = random.Random(seed)
    graph = Graph(num_vertices=num_vertices, directed=False)
    for u in range(num_vertices):
        for v in range(u + 1, num_vertices):
            if rng.random() < edge_probability:
                graph.add_edge(u, v, 1.0)
    return graph


def run() -> None:
    """Run the full Task 5 benchmark suite and export results and plots."""
    logger.info(
        "Generating benchmark graph (%d vertices, edge_probability=%s)...",
        GRAPH_SIZE, EDGE_PROBABILITY,
    )
    graph = generate_benchmark_graph()

    logger.info("Benchmarking sequential BFS (baseline)...")
    sequential_result = benchmark(
        sequential_bfs, graph, 0, repeats=REPEATS, label="Sequential", input_size=1
    )
    logger.info("  mean=%.6es std=%.2es", sequential_result.mean, sequential_result.std_dev)

    records: list[dict[str, object]] = [
        {"threads": 1, "mode": "Sequential", **sequential_result.to_dict()}
    ]
    speedups: dict[int, float] = {}

    logger.info("Benchmarking parallel BFS across thread counts %s...", THREAD_COUNTS)
    for thread_count in THREAD_COUNTS:
        result = benchmark(
            parallel_bfs,
            graph,
            0,
            num_threads=thread_count,
            repeats=REPEATS,
            label=f"Parallel-{thread_count}threads",
            input_size=thread_count,
        )
        speedup = sequential_result.mean / result.mean if result.mean > 0 else float("inf")
        speedups[thread_count] = speedup
        logger.info(
            "  threads=%d mean=%.6es std=%.2es speedup=%.3fx",
            thread_count, result.mean, result.std_dev, speedup,
        )
        records.append(
            {"threads": thread_count, "mode": "Parallel", "speedup": speedup, **result.to_dict()}
        )

    logger.info("Exporting raw results to CSV and Excel...")
    export_to_csv(records, RAW_DATA_DIR / "task5_benchmark.csv")
    export_to_excel(EXCEL_DIR / "task5_benchmark.xlsx", {"ConcurrentBFS": records})

    logger.info("Generating plot...")
    plot_line_comparison(
        x_values=list(THREAD_COUNTS),
        series={
            "Measured speedup": [speedups[t] for t in THREAD_COUNTS],
            "Ideal linear speedup": list(THREAD_COUNTS),
        },
        title="Task 5: Parallel BFS Speedup vs. Thread Count (limited by the GIL)",
        x_label="Number of threads",
        y_label="Speedup vs. sequential",
        output_path=PLOTS_DIR / "task5_speedup.png",
    )

    logger.info(
        "Task 5 benchmark suite complete. As expected for a CPU-bound CPython "
        "workload, thread count did not yield real speedup (see the GIL "
        "discussion in the report). See results/ for outputs."
    )


if __name__ == "__main__":
    try:
        run()
    except Exception:  
        logger.exception("Task 5 benchmark suite failed.")
        raise