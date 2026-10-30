"""Utilidades geoespaciales simples (sin dependencias extra)."""

from typing import List, Tuple


def point_in_polygon(lon: float, lat: float, ring: List[List[float]]) -> bool:
    """
    Ray-casting: ¿está (lon, lat) dentro del anillo?
    ring: [[lon, lat], ...] (cerrado o no).
    """
    if len(ring) < 3:
        return False

    n = len(ring)
    inside = False
    j = n - 1

    for i in range(n):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]

        if ((yi > lat) != (yj > lat)) and (
            lon < (xj - xi) * (lat - yi) / (yj - yi + 1e-15) + xi
        ):
            inside = not inside
        j = i

    return inside
