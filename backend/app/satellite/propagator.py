"""
Propagación orbital usando SGP4 + skyfield
Devuelve siempre coordenadas geodésicas listas para mapa táctico.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional

from skyfield.api import load, EarthSatellite, wgs84

# Timescale se carga una sola vez (costoso)
ts = load.timescale()


def propagate(
    line1: str,
    line2: str,
    name: str = "UNKNOWN",
    when: Optional[datetime] = None,
) -> Dict:
    """
    Propaga un satélite y devuelve posición geodésica lista para mapa.

    Returns:
        dict con latitude, longitude, altitude_km, speed_km_s, timestamp_utc
        o {"error": "..."} si falla.
    """
    if when is None:
        when = datetime.now(timezone.utc)

    try:
        sat = EarthSatellite(line1, line2, name)
        t = ts.from_datetime(when.astimezone(timezone.utc))

        geocentric = sat.at(t)
        lat, lon = wgs84.latlon_of(geocentric)
        alt = wgs84.height_of(geocentric).km

        # Velocidad aproximada (magnitud)
        velocity = geocentric.velocity.km_per_s
        speed = (velocity[0] ** 2 + velocity[1] ** 2 + velocity[2] ** 2) ** 0.5

        return {
            "name": name,
            "latitude": round(lat.degrees, 6),
            "longitude": round(lon.degrees, 6),
            "altitude_km": round(alt, 3),
            "speed_km_s": round(speed, 4),
            "timestamp_utc": when.isoformat(),
        }
    except Exception as e:
        return {"error": str(e)}


def propagate_many(satellites: List[Dict], when: Optional[datetime] = None) -> List[Dict]:
    """
    Propaga una lista de satélites (cada uno con name, line1, line2).
    Devuelve solo los que se propagaron correctamente.
    """
    if when is None:
        when = datetime.now(timezone.utc)

    results = []
    for sat in satellites:
        pos = propagate(
            line1=sat["line1"],
            line2=sat["line2"],
            name=sat.get("name", "UNKNOWN"),
            when=when,
        )
        if "error" not in pos:
            pos["norad_id"] = sat.get("norad_id")
            results.append(pos)

    return results
