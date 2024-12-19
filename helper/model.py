from dataclasses import dataclass

from typing import Optional


@dataclass(frozen=True)
class Scop:
    name: str
    address: str
    phone: str
    email: str
    website: str
    scope: str


@dataclass(frozen=True)
class Coordinates:
    latitude: float
    longitude: float


@dataclass(frozen=True)
class LocatedScop:
    scop: Scop
    coordinates: Coordinates
    distance_from_reference_in_km: int
