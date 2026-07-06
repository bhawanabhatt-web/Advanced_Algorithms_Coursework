from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  
from common.excel_export import export_to_excel  
from common.generator import random_floats  
from common.plotting import plot_line_comparison 
from common.timer import BenchmarkResult, benchmark  
from common.utils import EXCEL_DIR, PLOTS_DIR, RAW_DATA_DIR, export_to_csv, get_logger  
from first_fit_decreasing import first_fit_decreasing 
from local_search import local_search  
from packing import Item 
from simulated_annealing import simulated_annealing  

logger = get_logger(__name__)

DATASET_SIZES: tuple[int, ...] = (100, 1_000, 10_000)
REPEATS: int = 5
SA_ITERATIONS: int = 1_500
SEED: int = 42


def generate_items(count: int, seed: int = SEED) -> list[Item]:
    
    cpu = random_floats(count, 0.05, 0.4, seed=seed)
    ram = random_floats(count, 0.05, 0.4, seed=seed + 1)
    bandwidth = random_floats(count, 0.05, 0.4, seed=seed + 2)
    return [Item((cpu[i], ram[i], bandwidth[i])) for i in range(count)]


def benchmark_heuristics(items: list[Item]) -> dict[str, tuple[BenchmarkResult, int]]:
    
    n = len(items)

    ffd_time = benchmark(first_fit_decreasing, items, repeats=REPEATS, label="FFD", input_size=n)
    ffd_result = first_fit_decreasing(items)

    ls_time = benchmark(
        local_search, items, ffd_result, repeats=REPEATS, label="LocalSearch", input_size=n
    )
    ls_result = local_search(items, ffd_result)

    sa_time = benchmark(
        simulated_annealing,
        items,
        ffd_result,
        iterations=SA_ITERATIONS,
        repeats=REPEATS,
        label="SimulatedAnnealing",
        input_size=n,
    )
    sa_result = simulated_annealing(items, ffd_result, iterations=SA_ITERATIONS)

    return {
        "FFD": (ffd_time, ffd_result.num_bins),
        "LocalSearch": (ls_time, ls_result.num_bins),
        "SimulatedAnnealing": (sa_time, sa_result.num_bins),
    }


def run() -> None:
    """Run the full Task 4 benchmark suite and export results and plots."""
    logger.info("Starting Task 4 benchmark suite (sizes=%s, repeats=%d)", DATASET_SIZES, REPEATS)

    records: list[dict[str, object]] = []
    bins_by_size: dict[int, dict[str, int]] = {}

    for n in DATASET_SIZES:
        logger.info("Generating %d items and benchmarking heuristics...", n)
        items = generate_items(n)
        results = benchmark_heuristics(items)

        bins_by_size[n] = {}
        for heuristic_name, (timing, bins_used) in results.items():
            logger.info(
                "  %-20s mean=%.6es std=%.2es bins=%d",
                heuristic_name, timing.mean, timing.std_dev, bins_used,
            )
            record = {"heuristic": heuristic_name, "bins_used": bins_used, **timing.to_dict()}
            records.append(record)
            bins_by_size[n][heuristic_name] = bins_used

    logger.info("Exporting raw results to CSV and Excel...")
    export_to_csv(records, RAW_DATA_DIR / "task4_benchmark.csv")
    export_to_excel(EXCEL_DIR / "task4_benchmark.xlsx", {"BinPacking": records})

    logger.info("Generating plots...")
    lookup = {(r["heuristic"], r["input_size"]): r["mean_time_s"] for r in records}
    heuristics = ["FFD", "LocalSearch", "SimulatedAnnealing"]

    plot_line_comparison(
        x_values=list(DATASET_SIZES),
        series={name: [lookup[(name, n)] for n in DATASET_SIZES] for name in heuristics},
        title="Task 4: Heuristic Runtime vs. Number of Items",
        x_label="Number of items (n)",
        y_label="Mean execution time (s)",
        output_path=PLOTS_DIR / "task4_runtime.png",
        log_scale_y=True,
    )

    plot_line_comparison(
        x_values=list(DATASET_SIZES),
        series={
            name: [bins_by_size[n][name] for n in DATASET_SIZES] for name in heuristics
        },
        title="Task 4: Solution Quality (Bins Used) vs. Number of Items",
        x_label="Number of items (n)",
        y_label="Bins used",
        output_path=PLOTS_DIR / "task4_solution_quality.png",
    )

    logger.info("Task 4 benchmark suite complete. See results/ for outputs.")


if __name__ == "__main__":
    try:
        run()
    except Exception: 
        logger.exception("Task 4 benchmark suite failed.")
        raise