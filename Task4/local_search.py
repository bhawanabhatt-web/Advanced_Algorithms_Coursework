from __future__ import annotations
from packing import Item, PackingResult
__all__ = ["local_search"]

def local_search(
    items: list[Item], initial: PackingResult, max_iterations: int = 2000
) -> PackingResult:

    bins = [bin_.copy() for bin_ in initial.bins]

    for _ in range(max_iterations):
        if len(bins) <= 1:
            break

        loads = [sum(bin_.load) for bin_ in bins]
        victim_index = loads.index(min(loads))
        victim = bins[victim_index]

        remaining_bins = [bin_.copy() for i, bin_ in enumerate(bins) if i != victim_index]
        relocation_succeeded = True

        for item_index in victim.item_indices:
            item = items[item_index]
            placed = False
            for bin_ in remaining_bins:
                if bin_.fits(item):
                    bin_.add(item_index, item)
                    placed = True
                    break
            if not placed:
                relocation_succeeded = False
                break

        if relocation_succeeded:
            bins = remaining_bins
        else:
            break  # no further improvement possible with this simple move set

    return PackingResult(bins=bins)