from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  

from common.excel_export import export_to_excel  
from common.generator import random_floats, random_unique_integers 
from common.plotting import plot_bar_comparison, plot_line_comparison  
from common.timer import BenchmarkResult, benchmark 
from common.utils import EXCEL_DIR, PLOTS_DIR, RAW_DATA_DIR, export_to_csv, get_logger  # noqa: E402
from Task1.avl_tree import AVLTree 
from Task1.binary_search_tree import BinarySearchTree  
from Task1.city import City  
from Task1.hash_table import HashTable 
from Task1.min_heap import MinHeap  

logger = get_logger(__name__)

DATASET_SIZES: tuple[int, ...] = (100, 1_000, 10_000)
REPEATS: int = 5
SEARCH_SAMPLE_SIZE: int = 200
SEED: int = 42


def generate_cities(count: int, seed: int = SEED) -> list[City]:
    
    ids = random_unique_integers(count, low=0, high=count * 10, seed=seed)
    latitudes = random_floats(count, -90.0, 90.0, seed=seed + 1)
    longitudes = random_floats(count, -180.0, 180.0, seed=seed + 2)
    populations = random_floats(count, 1_000, 5_000_000, seed=seed + 3)
    return [
        City(
            city_id=ids[i],
            name=f"City{ids[i]}",
            latitude=latitudes[i],
            longitude=longitudes[i],
            population=int(populations[i]),
        )
        for i in range(count)
    ]


def _insert_all(structure: object, cities: list[City]) -> None:
    """Insert every city in ``cities`` into ``structure`` (BST/AVL/HashTable)."""
    for city in cities:
        structure.insert(city.city_id, city)  # type: ignore[attr-defined]


def benchmark_bst_avl_hash_insertion(
    cities: list[City],
) -> dict[str, BenchmarkResult]:
    
    n = len(cities)
    results: dict[str, BenchmarkResult] = {}

    results["BST"] = benchmark(
        _insert_all,
        setup=lambda: ((BinarySearchTree(), cities), {}),
        repeats=REPEATS,
        label="BST insert",
        input_size=n,
    )
    results["AVL"] = benchmark(
        _insert_all,
        setup=lambda: ((AVLTree(), cities), {}),
        repeats=REPEATS,
        label="AVL insert",
        input_size=n,
    )
    results["HashTable"] = benchmark(
        _insert_all,
        setup=lambda: ((HashTable(), cities), {}),
        repeats=REPEATS,
        label="HashTable insert",
        input_size=n,
    )
    return results


def benchmark_min_heap_insertion(cities: list[City]) -> BenchmarkResult:
    

    def insert_all_into_heap(city_list: list[City]) -> None:
        heap: MinHeap[City] = MinHeap()
        for city in city_list:
            heap.push(float(city.population), city)

    return benchmark(
        insert_all_into_heap,
        cities,
        repeats=REPEATS,
        label="MinHeap insert",
        input_size=len(cities),
    )


def benchmark_search(
    cities: list[City], sample_size: int = SEARCH_SAMPLE_SIZE
) -> dict[str, BenchmarkResult]:
    
    n = len(cities)
    sample_size = min(sample_size, n)
    search_ids = [city.city_id for city in cities[:sample_size]]

    bst: BinarySearchTree[City] = BinarySearchTree()
    avl: AVLTree[City] = AVLTree()
    table: HashTable[City] = HashTable()
    for city in cities:
        bst.insert(city.city_id, city)
        avl.insert(city.city_id, city)
        table.insert(city.city_id, city)

    def search_all(structure: object, ids: list[int]) -> None:
        for city_id in ids:
            structure.search(city_id)  # type: ignore[attr-defined]

    results: dict[str, BenchmarkResult] = {
        "BST": benchmark(
            search_all, bst, search_ids, repeats=REPEATS, label="BST search", input_size=n
        ),
        "AVL": benchmark(
            search_all, avl, search_ids, repeats=REPEATS, label="AVL search", input_size=n
        ),
        "HashTable": benchmark(
            search_all, table, search_ids, repeats=REPEATS, label="HashTable search", input_size=n
        ),
    }
    return results


def _mean_times_by_structure(
    records: list[dict[str, object]], structure_names: list[str], sizes: tuple[int, ...]
) -> dict[str, list[float]]:
    
    lookup = {(r["structure"], r["input_size"]): r["mean_time_s"] for r in records}
    return {name: [lookup[(name, n)] for n in sizes] for name in structure_names}


def run() -> None:
    """Run the full Task 1 benchmark suite and export results and plots."""
    logger.info("Starting Task 1 benchmark suite (sizes=%s, repeats=%d)", DATASET_SIZES, REPEATS)

    insertion_records: list[dict[str, object]] = []
    search_records: list[dict[str, object]] = []
    height_by_size: dict[int, dict[str, int]] = {}

    for n in DATASET_SIZES:
        logger.info("Generating dataset of %d cities...", n)
        cities = generate_cities(n)

        logger.info("Benchmarking insertion (BST, AVL, HashTable) for n=%d...", n)
        insertion_results = benchmark_bst_avl_hash_insertion(cities)
        heap_result = benchmark_min_heap_insertion(cities)
        insertion_results["MinHeap"] = heap_result
        for structure_name, result in insertion_results.items():
            logger.info(
                "  %-10s insert: mean=%.6es std=%.2es", structure_name, result.mean, result.std_dev
            )
            insertion_records.append({"structure": structure_name, **result.to_dict()})

        logger.info("Benchmarking search (BST, AVL, HashTable) for n=%d...", n)
        search_results = benchmark_search(cities)
        for structure_name, result in search_results.items():
            logger.info(
                "  %-10s search: mean=%.6es std=%.2es", structure_name, result.mean, result.std_dev
            )
            search_records.append({"structure": structure_name, **result.to_dict()})

        bst_final: BinarySearchTree[City] = BinarySearchTree()
        avl_final: AVLTree[City] = AVLTree()
        for city in cities:
            bst_final.insert(city.city_id, city)
            avl_final.insert(city.city_id, city)
        height_by_size[n] = {"BST": bst_final.height(), "AVL": avl_final.height()}
        logger.info("  Tree heights at n=%d: %s", n, height_by_size[n])

    logger.info("Exporting raw results to CSV and Excel...")
    export_to_csv(insertion_records, RAW_DATA_DIR / "task1_insertion.csv")
    export_to_csv(search_records, RAW_DATA_DIR / "task1_search.csv")
    export_to_excel(
        EXCEL_DIR / "task1_benchmark.xlsx",
        {"Insertion": insertion_records, "Search": search_records},
    )

    logger.info("Generating plots...")
    structures_insert = ["BST", "AVL", "HashTable", "MinHeap"]
    plot_line_comparison(
        x_values=list(DATASET_SIZES),
        series=_mean_times_by_structure(insertion_records, structures_insert, DATASET_SIZES),
        title="Task 1: Insertion Time vs. Input Size",
        x_label="Number of cities (n)",
        y_label="Mean insertion time (s)",
        output_path=PLOTS_DIR / "task1_insertion_time.png",
    )

    structures_search = ["BST", "AVL", "HashTable"]
    plot_line_comparison(
        x_values=list(DATASET_SIZES),
        series=_mean_times_by_structure(search_records, structures_search, DATASET_SIZES),
        title=f"Task 1: Search Time vs. Input Size ({SEARCH_SAMPLE_SIZE} lookups)",
        x_label="Number of cities (n)",
        y_label="Mean search time (s)",
        output_path=PLOTS_DIR / "task1_search_time.png",
    )

    plot_bar_comparison(
        categories=[str(n) for n in DATASET_SIZES],
        series={
            "BST": [height_by_size[n]["BST"] for n in DATASET_SIZES],
            "AVL": [height_by_size[n]["AVL"] for n in DATASET_SIZES],
        },
        title="Task 1: Tree Height vs. Input Size",
        x_label="Number of cities (n)",
        y_label="Tree height",
        output_path=PLOTS_DIR / "task1_tree_heights.png",
    )

    logger.info(
        "Task 1 benchmark suite complete. See results/ for outputs."
    )


if __name__ == "__main__":
    try:
        run()
    except Exception:  # noqa: BLE001 -- top-level entry point: log and re-raise
        logger.exception("Task 1 benchmark suite failed.")
        raise