from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  
from common.generator import random_floats  
from common.utils import get_logger  
from packing import Item  
from packing import first_fit_decreasing, local_search, simulated_annealing
logger = get_logger(__name__)

DEMO_ITEM_COUNT = 30
def build_demo_items(count: int = DEMO_ITEM_COUNT) -> list[Item]:
    cpu = random_floats(count, 0.05, 0.4, seed=42)
    ram = random_floats(count, 0.05, 0.4, seed=43)
    bandwidth = random_floats(count, 0.05, 0.4, seed=44)
    return [Item((cpu[i], ram[i], bandwidth[i])) for i in range(count)]

def demonstrate_first_fit_decreasing(items: list[Item]) -> None:
    """Pack ``items`` with the greedy FFD heuristic and report the result."""
    logger.info("--- Greedy Construction: First-Fit-Decreasing ---")
    result = first_fit_decreasing(items)
    logger.info("Bins used: %d. Feasible: %s", result.num_bins, result.is_feasible(items))

def demonstrate_local_search(items: list[Item]) -> None:
    """Improve an FFD packing via hill-climbing local search."""
    logger.info("--- Local Search (hill climbing on FFD's solution) ---")
    initial = first_fit_decreasing(items)
    improved = local_search(items, initial)
    logger.info(
        "Bins before: %d, bins after: %d, feasible: %s",
        initial.num_bins, improved.num_bins, improved.is_feasible(items),
    )

def demonstrate_simulated_annealing(items: list[Item]) -> None:
    """Improve an FFD packing via Simulated Annealing."""
    logger.info("--- Simulated Annealing (escapes local optima via worsening moves) ---")
    initial = first_fit_decreasing(items)
    improved = simulated_annealing(items, initial, iterations=1500)
    logger.info(
        "Bins before: %d, bins after: %d, feasible: %s",
        initial.num_bins, improved.num_bins, improved.is_feasible(items),
    )

def demonstrate_error_handling() -> None:
    """Show that invalid inputs are rejected with clear, informative errors."""
    logger.info("--- Exception Handling Demonstration ---")
    try:
        Item(dimensions=(0.5, -0.1))
    except ValueError as exc:
        logger.info("Correctly rejected invalid Item: %s", exc)

    items = build_demo_items(5)
    initial = first_fit_decreasing(items)
    try:
        simulated_annealing(items, initial, cooling_rate=1.5)
    except ValueError as exc:
        logger.info("Correctly rejected invalid cooling_rate: %s", exc)

def main() -> None:
    """Run all three bin-packing heuristic demonstrations."""
    logger.info("Generating %d demo items (seed=42)...", DEMO_ITEM_COUNT)
    items = build_demo_items()

    demonstrate_first_fit_decreasing(items)
    demonstrate_local_search(items)
    demonstrate_simulated_annealing(items)
    demonstrate_error_handling()

    logger.info(
        "Task 4 demonstration complete. Run 'python -m Task4.benchmark' for performance results."
    )

if __name__ == "__main__":
    try:
        main()
    except Exception:  # noqa: BLE001 -- top-level entry point: log and re-raise
        logger.exception("Task 4 demonstration failed.")
        raise