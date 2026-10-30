"""
Ground track: secuencia de posiciones geodésicas a lo largo de la órbita.
Útil para dibujar la traza en el mapa táctico.
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional

from app.satellite.propagator import propagate


def ground_track(
    line1: str,
    line2: str,
    name: str = "UNKNOWN",
    minutes_ahead: float = 90.0,
    minutes_behind: float = 30.0,
    step_seconds: int = 30,
) -> Dict:
    """
    Genera puntos de la traza orbital (pasado cercano + futuro).
    Maneja cruce de antimeridiano partiendo la línea en segmentos.
    """
    now = datetime.now(timezone.utc)
    start = now - timedelta(minutes=minutes_behind)
    total_s = int((minutes_behind + minutes_ahead) * 60)
    steps = max(1, total_s // step_seconds)

    points: List[List[float]] = []
    for i in range(steps + 1):
        t = start + timedelta(seconds=i * step_seconds)
        pos = propagate(line1, line2, name=name, when=t)
        if "error" in pos:
            continue
        points.append([pos["longitude"], pos["latitude"]])

    # Partir en segmentos si hay salto grande de longitud (antimeridiano)
    segments: List[List[List[float]]] = []
    current: List[List[float]] = []
    for pt in points:
        if current and abs(pt[0] - current[-1][0]) > 180:
            if len(current) >= 2:
                segments.append(current)
            current = [pt]
        else:
            current.append(pt)
    if len(current) >= 2:
        segments.append(current)

    return {
        "name": name,
        "point_count": len(points),
        "segment_count": len(segments),
        "minutes_behind": minutes_behind,
        "minutes_ahead": minutes_ahead,
        "segments": segments,
        "timestamp_utc": now.isoformat(),
    }
