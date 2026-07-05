
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  

from common.generator import random_floats, random_unique_integers 
from common.utils import get_logger  
from Task1.avl_tree import AVLTree  
from Task1.binary_search_tree import BinarySearchTree  
from Task1.city import City
logger = get_logger(__name__)

DEMO_CITY_COUNT = 10


def build_demo_cities(count: int = DEMO_CITY_COUNT) -> list[City]:
    """Build a small, reproducible list of demo cities.

    Args:
        count: Number of cities to generate. Defaults to ``10``.

    Returns:
        A list of :class:`City` records.
    """
    ids = random_unique_integers(count, low=1, high=count * 5, seed=42)
    populations = random_floats(count, 10_000, 2_000_000, seed=43)
    return [
        City(
            city_id=city_id,
            name=f"City{city_id}",
            latitude=0.0,
            longitude=0.0,
            population=int(population),
        )
        for city_id, population in zip(ids, populations)
    ]


def demonstrate_binary_search_tree(cities: list[City]) -> None:
    """Insert every city into a BST and demonstrate search/delete."""
    logger.info("--- Binary Search Tree ---")
    tree: BinarySearchTree[City] = BinarySearchTree()
    for city in cities:
        tree.insert(city.city_id, city)
    logger.info("Inserted %d cities. Tree height = %d", len(tree), tree.height())

    sample = cities[0]
    found = tree.search(sample.city_id)
    logger.info("Search for city_id=%d -> %s", sample.city_id, found)

    deleted = tree.delete(sample.city_id)
    logger.info("Deleted city_id=%d -> %s. Remaining size = %d", sample.city_id, deleted, len(tree))

def demonstrate_avl_tree(cities: list[City]) -> None:
    """Insert every city into an AVL tree and demonstrate its balance."""
    logger.info("--- AVL Tree ---")
    tree: AVLTree[City] = AVLTree()
    for city in cities:
        tree.insert(city.city_id, city)
    logger.info("Inserted %d cities. Tree height = %d (kept balanced)", len(tree), tree.height())
 
    sample = cities[-1]
    found = tree.search(sample.city_id)
    logger.info("Search for city_id=%d -> %s", sample.city_id, found)
 


def main() -> None:
    """Run all four data structure demonstrations."""
    logger.info("Generating %d demo cities (seed=42)...", DEMO_CITY_COUNT)
    cities = build_demo_cities()

    demonstrate_binary_search_tree(cities)
    demonstrate_avl_tree(cities)

    logger.info(
        "Task 1 demonstration complete. Run 'python -m Task1.benchmark' for performance results."
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:  # noqa: BLE001 -- top-level entry point: log and re-raise
        logger.exception("Task 1 demonstration failed.")
        raise