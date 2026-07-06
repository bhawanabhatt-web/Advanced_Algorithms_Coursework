from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  

from common.excel_export import export_to_excel 
from common.generator import random_integers, random_intervals  
from common.plotting import plot_bar_comparison, plot_line_comparison 
from common.timer import BenchmarkResult, benchmark  
from common.utils import EXCEL_DIR, PLOTS_DIR, RAW_DATA_DIR, export_to_csv, get_logger  
from job_scheduling import Job, weighted_job_scheduling  
from knights_tour import knights_tour  
from platform_scheduling import min_platforms  

logger = get_logger(__name__)

DP_GREEDY_SIZES: tuple[int, ...] = (100, 1_000, 10_000)
BOARD_SIZES: tuple[int, ...] = (5, 6, 8)
REPEATS: int = 5
SEED: int = 42


def generate_jobs(count: int, seed: int = SEED) -> list[Job]:
    intervals = random_intervals(
        count, max_start=count * 2, min_duration=1, max_duration=50, seed=seed
    )
    profits = random_integers(count, low=1, high=100, seed=seed + 1)
    return [Job(start=s, end=e, profit=p) for (s, e), p in zip(intervals, profits)]


def generate_train_schedule(count: int, seed: int = SEED) -> tuple[list[int], list[int]]:
    intervals = random_intervals(
        count, max_start=1440, min_duration=5, max_duration=120, seed=seed
    )
    arrivals = [start for start, _ in intervals]
    departures = [end for _, end in intervals]
    return arrivals, departures


def benchmark_dynamic_programming() -> list[BenchmarkResult]:
    """Benchmark Weighted Job Scheduling across :data:`DP_GREEDY_SIZES`."""
    results = []
    for n in DP_GREEDY_SIZES:
        jobs = generate_jobs(n)
        result = benchmark(
            weighted_job_scheduling, jobs, repeats=REPEATS, label="DP job scheduling", input_size=n
        )
        results.append(result)
    return results


def benchmark_greedy() -> list[BenchmarkResult]:
    """Benchmark Minimum Number of Platforms across :data:`DP_GREEDY_SIZES`."""
    results = []
    for n in DP_GREEDY_SIZES:
        arrivals, departures = generate_train_schedule(n)
        result = benchmark(
            min_platforms,
            arrivals,
            departures,
            repeats=REPEATS,
            label="Greedy min platforms",
            input_size=n,
        )
        results.append(result)
    return results


def benchmark_backtracking() -> dict[str, BenchmarkResult]:
    results: dict[str, BenchmarkResult] = {}
    for board_size in BOARD_SIZES:
        for use_warnsdorff in (True, False):
            label = f"{board_size}x{board_size}_{'warnsdorff' if use_warnsdorff else 'naive'}"
            results[label] = benchmark(
                knights_tour,
                board_size,
                use_warnsdorff=use_warnsdorff,
                node_limit=500_000,
                repeats=REPEATS,
                label=label,
                input_size=board_size,
            )
    return results


def run() -> None:
    """Run the full Task 3 benchmark suite and export results and plots."""
    logger.info("Starting Task 3 benchmark suite (repeats=%d)", REPEATS)

    logger.info("Benchmarking Dynamic Programming (Weighted Job Scheduling)...")
    dp_results = benchmark_dynamic_programming()
    for result in dp_results:
        logger.info("  n=%-6d mean=%.6es std=%.2es", result.input_size, result.mean, result.std_dev)

    logger.info("Benchmarking Greedy (Minimum Number of Platforms)...")
    greedy_results = benchmark_greedy()
    for result in greedy_results:
        logger.info("  n=%-6d mean=%.6es std=%.2es", result.input_size, result.mean, result.std_dev)

    logger.info("Benchmarking Backtracking (Knight's Tour, Warnsdorff vs. naive)...")
    backtracking_results = benchmark_backtracking()
    nodes_expanded: dict[str, int] = {}
    for label, result in backtracking_results.items():
        tour_result = knights_tour(
            result.input_size, use_warnsdorff="warnsdorff" in label, node_limit=500_000
        )
        nodes_expanded[label] = tour_result.nodes_expanded
        logger.info(
            "  %-20s mean=%.6es nodes_expanded=%d solved=%s",
            label, result.mean, tour_result.nodes_expanded, tour_result.solved,
        )

    logger.info("Exporting raw results to CSV and Excel...")
    dp_records = [{"algorithm": "DP_JobScheduling", **r.to_dict()} for r in dp_results]
    greedy_records = [{"algorithm": "Greedy_MinPlatforms", **r.to_dict()} for r in greedy_results]
    backtracking_records = [
        {"config": label, "nodes_expanded": nodes_expanded[label], **r.to_dict()}
        for label, r in backtracking_results.items()
    ]
    export_to_csv(dp_records + greedy_records, RAW_DATA_DIR / "task3_dp_greedy.csv")
    export_to_csv(backtracking_records, RAW_DATA_DIR / "task3_backtracking.csv")
    export_to_excel(
        EXCEL_DIR / "task3_benchmark.xlsx",
        {
            "DP_and_Greedy": dp_records + greedy_records,
            "Backtracking": backtracking_records,
        },
    )

    logger.info("Generating plots...")
    plot_line_comparison(
        x_values=list(DP_GREEDY_SIZES),
        series={
            "DP: Job Scheduling": [r.mean for r in dp_results],
            "Greedy: Min Platforms": [r.mean for r in greedy_results],
        },
        title="Task 3: DP vs. Greedy Runtime vs. Input Size",
        x_label="Number of jobs / trains (n)",
        y_label="Mean execution time (s)",
        output_path=PLOTS_DIR / "task3_dp_greedy_runtime.png",
    )

    board_labels = [f"{b}x{b}" for b in BOARD_SIZES]
    plot_bar_comparison(
        categories=board_labels,
        series={
            "Naive order": [nodes_expanded[f"{b}x{b}_naive"] for b in BOARD_SIZES],
            "Warnsdorff pruning": [nodes_expanded[f"{b}x{b}_warnsdorff"] for b in BOARD_SIZES],
        },
        title="Task 3: Knight's Tour -- Search Effort by Move Ordering",
        x_label="Board size",
        y_label="Nodes expanded (log scale)",
        output_path=PLOTS_DIR / "task3_knights_tour_pruning.png",
        log_scale_y=True,
    )

    logger.info("Task 3 benchmark suite complete. See results/ for outputs.")


if __name__ == "__main__":
    try:
        run()
    except Exception:  # noqa: BLE001 -- top-level entry point: log and re-raise
        logger.exception("Task 3 benchmark suite failed.")
        raise