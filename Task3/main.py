from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1])) 
from common.utils import get_logger  
from job_scheduling import Job, weighted_job_scheduling 

logger = get_logger(__name__)

def demonstrate_dynamic_programming() -> None:
    """Solve a small Weighted Job Scheduling instance and print the selection."""
    logger.info("--- Dynamic Programming: Weighted Job Scheduling ---")
    jobs = [
        Job(start=1, end=3, profit=5),
        Job(start=2, end=5, profit=6),
        Job(start=4, end=6, profit=5),
        Job(start=6, end=7, profit=4),
    ]
    result = weighted_job_scheduling(jobs)
    logger.info("Maximum profit: %d", result.max_profit)
    for job in result.selected_jobs:
        logger.info("  selected: start=%d end=%d profit=%d", job.start, job.end, job.profit)


def demonstrate_greedy() -> None:
    """Solve a small Minimum Number of Platforms instance and cross-check it."""
    logger.info("--- Greedy: Minimum Number of Platforms ---")
    arrivals = [900, 940, 950, 1100, 1500, 1800]
    departures = [910, 1200, 1120, 1130, 1900, 2000]
    greedy_result = min_platforms(arrivals, departures)
    exact_result = min_platforms_exact(arrivals, departures)
    logger.info("Greedy result: %d platforms", greedy_result)
    logger.info("Exact (brute-force) result: %d platforms (match: %s)",
                exact_result, greedy_result == exact_result)


def demonstrate_backtracking() -> None:
    """Solve Knight's Tour on a 6x6 board, comparing pruning strategies."""
    logger.info("--- Backtracking: Knight's Tour (Warnsdorff pruning) ---")
    warnsdorff_result = knights_tour(6, use_warnsdorff=True)
    logger.info(
        "Warnsdorff heuristic: solved=%s, nodes_expanded=%d",
        warnsdorff_result.solved, warnsdorff_result.nodes_expanded,
    )

    naive_result = knights_tour(6, use_warnsdorff=False, node_limit=500_000)
    logger.info(
        "Naive move ordering:  solved=%s, nodes_expanded=%d",
        naive_result.solved, naive_result.nodes_expanded,
    )
    logger.info(
        "Warnsdorff's rule reduced the search by a factor of ~%.0fx on this board.",
        naive_result.nodes_expanded / warnsdorff_result.nodes_expanded,
    )


def demonstrate_error_handling() -> None:
    """Show that invalid inputs are rejected with clear, informative errors."""
    logger.info("--- Exception Handling Demonstration ---")
    try:
        Job(start=5, end=2, profit=10)
    except ValueError as exc:
        logger.info("Correctly rejected invalid Job: %s", exc)

    try:
        min_platforms([1, 2, 3], [1, 2])
    except ValueError as exc:
        logger.info("Correctly rejected mismatched schedule lengths: %s", exc)

    try:
        knights_tour(board_size=5, start=(10, 10))
    except ValueError as exc:
        logger.info("Correctly rejected out-of-bounds start square: %s", exc)


def main() -> None:
    """Run all three algorithmic strategy demonstrations."""
    demonstrate_dynamic_programming()
    demonstrate_greedy()
    demonstrate_backtracking()
    demonstrate_error_handling()
    logger.info(
        "Task 3 demonstration complete. Run 'python -m Task3.benchmark' for performance results."
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:  
        logger.exception("Task 3 demonstration failed.")
        raise