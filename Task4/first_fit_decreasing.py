from __future__ import annotations
from packing import Bin, Item, PackingResult
__all__ = ["first_fit_decreasing"]
def first_fit_decreasing(items: list[Item]) -> PackingResult:
    if not items:
        return PackingResult(bins=[])

    order = sorted(range(len(items)), key=lambda i: items[i].total_size, reverse=True)
    bins: list[Bin] = []

    for index in order:
        item = items[index]
        placed = False
        for bin_ in bins:
            if bin_.fits(item):
                bin_.add(index, item)
                placed = True
                break
        if not placed:
            dimension_count = len(item.dimensions)
            new_bin = Bin(capacity=tuple([1.0] * dimension_count), load=[0.0] * dimension_count)
            new_bin.add(index, item)
            bins.append(new_bin)

    return PackingResult(bins=bins)