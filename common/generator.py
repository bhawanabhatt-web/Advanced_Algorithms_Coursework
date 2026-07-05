from __future__ import annotations

import random

__all__ = [
    "DEFAULT_SEED",
    "random_unique_integers",
    "random_integers",
    "random_floats",
    "random_intervals",
    "random_points_2d",
    "random_weighted_edges",
]

DEFAULT_SEED: int = 42


def random_unique_integers(
    count: int, low: int, high: int, seed: int = DEFAULT_SEED
) -> list[int]:
    """Generate ``count`` unique integers sampled from ``[low, high]``.

    Args:
        count: Number of unique integers to generate.
        low: Inclusive lower bound of the sampling range.
        high: Inclusive upper bound of the sampling range.
        seed: Seed for the private random generator. Defaults to ``42``.

    Returns:
        A list of ``count`` unique integers in arbitrary order.

    Raises:
        ValueError: If ``count`` exceeds the number of integers available
            in ``[low, high]``.
    """
    span = high - low + 1
    if count > span:
        raise ValueError(
            f"Cannot draw {count} unique integers from a range of size {span}."
        )
    rng = random.Random(seed)
    return rng.sample(range(low, high + 1), count)


def random_integers(
    count: int, low: int, high: int, seed: int = DEFAULT_SEED
) -> list[int]:
    """Generate ``count`` integers (with replacement) from ``[low, high]``.

    Args:
        count: Number of integers to generate.
        low: Inclusive lower bound.
        high: Inclusive upper bound.
        seed: Seed for the private random generator. Defaults to ``42``.

    Returns:
        A list of ``count`` integers, duplicates allowed.
    """
    rng = random.Random(seed)
    return [rng.randint(low, high) for _ in range(count)]


def random_floats(
    count: int, low: float, high: float, seed: int = DEFAULT_SEED
) -> list[float]:
    """Generate ``count`` floats uniformly sampled from ``[low, high]``.

    Args:
        count: Number of floats to generate.
        low: Inclusive lower bound.
        high: Inclusive upper bound.
        seed: Seed for the private random generator. Defaults to ``42``.

    Returns:
        A list of ``count`` floats.
    """
    rng = random.Random(seed)
    return [rng.uniform(low, high) for _ in range(count)]


def random_intervals(
    count: int,
    max_start: int,
    min_duration: int,
    max_duration: int,
    seed: int = DEFAULT_SEED,
) -> list[tuple[int, int]]:
    
    if min_duration <= 0:
        raise ValueError("'min_duration' must be a positive integer.")
    if min_duration > max_duration:
        raise ValueError("'min_duration' cannot exceed 'max_duration'.")

    rng = random.Random(seed)
    intervals: list[tuple[int, int]] = []
    for _ in range(count):
        start = rng.randint(0, max_start)
        duration = rng.randint(min_duration, max_duration)
        intervals.append((start, start + duration))
    return intervals


def random_points_2d(
    count: int,
    x_bounds: tuple[float, float],
    y_bounds: tuple[float, float],
    seed: int = DEFAULT_SEED,
) -> list[tuple[float, float]]:
   
    rng = random.Random(seed)
    min_x, max_x = x_bounds
    min_y, max_y = y_bounds
    return [(rng.uniform(min_x, max_x), rng.uniform(min_y, max_y)) for _ in range(count)]


def random_weighted_edges(
    num_vertices: int,
    edge_probability: float,
    weight_range: tuple[int, int],
    directed: bool = True,
    seed: int = DEFAULT_SEED,
) -> list[tuple[int, int, int]]:
    
    if not 0.0 <= edge_probability <= 1.0:
        raise ValueError("'edge_probability' must be within [0, 1].")

    rng = random.Random(seed)
    low, high = weight_range
    edges: list[tuple[int, int, int]] = []

    for u in range(num_vertices):
        v_range = range(num_vertices) if directed else range(u + 1, num_vertices)
        for v in v_range:
            if u == v:
                continue
            if rng.random() < edge_probability:
                edges.append((u, v, rng.randint(low, high)))
    return edges