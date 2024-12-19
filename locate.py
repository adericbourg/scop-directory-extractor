#!/usr/bin/env python3
import csv
from typing import List

from geopy.geocoders import Nominatim
from haversine import haversine, Unit

from helper import io
from helper.model import Scop, Coordinates, LocatedScop

REFERENCE = Coordinates(latitude=46.25340495, longitude=0.2448063516198583)


def run():
    scops = _load()
    located_scops = _locate(scops)
    _write(located_scops)


def _load() -> List[Scop]:
    with open(io.SCOP_CSV, 'r') as csvfile:
        reader = csv.reader(csvfile)
        return [Scop(line[0], line[2], line[4], line[3], line[5], line[1]) for line in
                (line for index, line in enumerate(reader) if index > 0)]


def _locate(scops: List[Scop]) -> List[LocatedScop]:
    nominatim = Nominatim(user_agent="Mozilla/5.0")
    located_scops = []
    for scop in scops:
        location = nominatim.geocode(scop.address)
        if not location:
            structured=scop.address.split(',')
            city=structured[-1]
            location = nominatim.geocode(city)
        if not location:
            pass
        coordinates = Coordinates(latitude=location.point.latitude, longitude=location.point.longitude)
        distance = _distance_between(coordinates, REFERENCE)
        located_scops.append(LocatedScop(
            scop=scop,
            coordinates=coordinates,
            distance_from_reference_in_km=distance
        ))
    return located_scops


def _distance_between(c1: Coordinates, c2: Coordinates) -> int:
    return haversine(
        (c1.latitude, c1.longitude),
        (c2.latitude, c2.longitude),
        unit=Unit.KILOMETERS
    )


def _write(located_scops: List[LocatedScop]) -> None:
    with open(io.LOCATED_SCOP_CSV, 'w') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow(['Nom', 'Secteur', "Distance (km)", 'Adresse', 'E-mail', 'Téléphone', "Site", ])
        for located_scop in located_scops:
            scop = located_scop.scop
            writer.writerow([
                scop.name,
                scop.scope,
                located_scop.distance_from_reference_in_km,
                scop.address,
                scop.email,
                scop.phone,
                scop.website
            ])


if __name__ == "__main__":
    run()
