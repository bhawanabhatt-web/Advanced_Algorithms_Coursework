from __future__ import annotations
import math
import random
from packing import Bin, Item, PackingResult

__all__ = ["simulated_annealing"]
def _cost(bins: list[Bin]) -> float:
    
    return len(bins) * 100.0 - sum(sum(bin_.load) for bin_ in bins) * 0.01

def simulated_annealing(
    items: list[Item],
    initial: PackingResult,
    iterations: int = 3000,
    initial_temperature: float = 1.0,
    cooling_rate: float = 0.995,
    seed: int = 42,
) -> PackingResult:
    
    if initial_temperature <= 0:
        raise ValueError(f"'initial_temperature' must be positive, got {initial_temperature}.")
    if not 0 < cooling_rate <= 1:
        raise ValueError(f"'cooling_rate' must be in (0, 1], got {cooling_rate}.")

    rng = random.Random(seed)
    bins = [bin_.copy() for bin_ in initial.bins]
    temperature = initial_temperature

    current_cost = _cost(bins)
    best_bins = [bin_.copy() for bin_ in bins]
    best_cost = current_cost

    for _ in range(iterations):
        if len(bins) <= 1:
            break

        source_bin = rng.choice(bins)
        if not source_bin.item_indices:
            continue
        item_index = rng.choice(source_bin.item_indices)
        item = items[item_index]

        candidate_targets = [b for b in bins if b is not source_bin and b.fits(item)]
        if not candidate_targets:
            continue
        target_bin = rng.choice(candidate_targets)

        source_bin.remove(item_index, item)
        target_bin.add(item_index, item)

        trial_bins = [b for b in bins if not b.is_empty()]
        new_cost = _cost(trial_bins)
        delta = new_cost - current_cost
        accept = delta < 0 or rng.random() < math.exp(-delta / max(temperature, 1e-9))

        if accept:
            bins = trial_bins
            current_cost = new_cost
            if new_cost < best_cost:
                best_cost = new_cost
                best_bins = [b.copy() for b in bins]
        else:
            source_bin.add(item_index, item)
            target_bin.remove(item_index, item)

        temperature *= cooling_rate

    return PackingResult(bins=best_bins)