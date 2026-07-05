from __future__ import annotations

import statistics
import time
from dataclasses import dataclass, field
from typing import Any, Callable, TypeVar

T = TypeVar("T")

__all__ = ["BenchmarkResult", "benchmark", "time_once"]


@dataclass(frozen=True)
class BenchmarkResult:

    label: str
    input_size: int
    repeats: int
    times: tuple[float, ...] = field(repr=False)
    mean: float
    std_dev: float
    minimum: float
    maximum: float

    def to_dict(self) -> dict[str, Any]:
        
        return {
            "label": self.label,
            "input_size": self.input_size,
            "repeats": self.repeats,
            "mean_time_s": self.mean,
            "std_dev_s": self.std_dev,
            "min_time_s": self.minimum,
            "max_time_s": self.maximum,
        }


def time_once(func: Callable[..., T], *args: Any, **kwargs: Any) -> tuple[T, float]:
    
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed


def benchmark(
    func: Callable[..., Any],
    *args: Any,
    repeats: int = 5,
    label: str = "",
    input_size: int = 0,
    setup: Callable[[], tuple[tuple[Any, ...], dict[str, Any]]] | None = None,
    **kwargs: Any,
) -> BenchmarkResult:
    
    if repeats <= 0:
        raise ValueError(f"'repeats' must be a positive integer, got {repeats}.")

    times: list[float] = []
    for _ in range(repeats):
        call_args, call_kwargs = args, kwargs
        if setup is not None:
            call_args, call_kwargs = setup()
        _, elapsed = time_once(func, *call_args, **call_kwargs)
        times.append(elapsed)

    return BenchmarkResult(
        label=label,
        input_size=input_size,
        repeats=repeats,
        times=tuple(times),
        mean=statistics.mean(times),
        std_dev=statistics.stdev(times) if len(times) > 1 else 0.0,
        minimum=min(times),
        maximum=max(times),
    )