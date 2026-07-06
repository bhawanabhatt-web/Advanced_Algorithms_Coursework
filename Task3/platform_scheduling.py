from __future__ import annotations
__all__ = ["min_platforms", "min_platforms_exact"]
def _validate_schedule(arrivals: list[int], departures: list[int]) -> None:
    if len(arrivals) != len(departures):
        raise ValueError(
            f"'arrivals' ({len(arrivals)}) and 'departures' ({len(departures)}) "
            "must have the same length."
        )
    if not arrivals:
        raise ValueError("At least one train is required.")
    for index, (arrival, departure) in enumerate(zip(arrivals, departures)):
        if departure < arrival:
            raise ValueError(
                f"Train {index}: departure ({departure}) precedes arrival ({arrival})."
            )


def min_platforms(arrivals: list[int], departures: list[int]) -> int:
    
    _validate_schedule(arrivals, departures)

    sorted_arrivals = sorted(arrivals)
    sorted_departures = sorted(departures)
    n = len(sorted_arrivals)

    arrival_index, departure_index = 1, 0
    platforms_in_use = 1
    max_platforms = 1

    while arrival_index < n and departure_index < n:
        if sorted_arrivals[arrival_index] <= sorted_departures[departure_index]:
            platforms_in_use += 1
            arrival_index += 1
            max_platforms = max(max_platforms, platforms_in_use)
        else:
            platforms_in_use -= 1
            departure_index += 1

    return max_platforms


def min_platforms_exact(arrivals: list[int], departures: list[int]) -> int:
    _validate_schedule(arrivals, departures)

    events: list[tuple[int, int]] = []
    for arrival, departure in zip(arrivals, departures):
        events.append((arrival, 1))
        events.append((departure + 1, -1))  # departs strictly after `departure`
    events.sort()

    current_platforms = 0
    max_platforms = 0
    for _, delta in events:
        current_platforms += delta
        max_platforms = max(max_platforms, current_platforms)
    return max_platforms