from __future__ import annotations

from dataclasses import dataclass

__all__ = ["City"]

@dataclass(frozen=True, slots=True)
class City:
    city_id: int
    name: str
    latitude: float
    longitude: float
    population: int