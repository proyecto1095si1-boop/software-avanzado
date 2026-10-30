"""
Propagación orbital usando SGP4
"""

from sgp4.api import Satrec, jday
from datetime import datetime, timezone
from typing import Dict, Optional


def propagate(line1: str, line2: str, when: Optional[datetime] = None) -> Dict:
    """
    Propaga la posición de un satélite a un momento dado.
    Retorna latitud, longitud, altitud (km) y velocidad.
    """
    if when is None:
        when = datetime.now(timezone.utc)

    satellite = Satrec.twoline2rv(line1, line2)

    jd, fr = jday(
        when.year, when.month, when.day,
        when.hour, when.minute, when.second + when.microsecond / 1e6
    )

    error, position, velocity = satellite.sgp4(jd, fr)

    if error != 0:
        return {"error": f"SGP4 error code {error}"}

    # position está en km (ECI)
    # Para una primera versión devolvemos ECI + magnitud de velocidad
    import math
    x, y, z = position
    vx, vy, vz = velocity
    speed = math.sqrt(vx**2 + vy**2 + vz**2)

    return {
        "eci_km": {"x": x, "y": y, "z": z},
        "velocity_km_s": {"vx": vx, "vy": vy, "vz": vz},
        "speed_km_s": speed,
        "timestamp_utc": when.isoformat(),
    }
