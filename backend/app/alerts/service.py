"""
Motor de alertas tácticas.
Detecta satélites cuya posición geodésica cae dentro de una AOI.
"""

from typing import List, Optional
from datetime import datetime, timezone

from app.aoi.data import get_all_aois
from app.satellite.tle import get_satellites
from app.satellite.propagator import propagate_many
from app.alerts.geo import point_in_polygon
from app.alerts.models import Alert


async def check_satellite_over_aoi(
    group: str = "stations",
    limit: Optional[int] = 200,
) -> List[Alert]:
    """Propaga el grupo y genera alertas por cada cruce satélite ∩ AOI."""
    sats = await get_satellites(group)
    if limit:
        sats = sats[:limit]

    positions = propagate_many(sats)
    aois = get_all_aois()
    now = datetime.now(timezone.utc).isoformat()
    alerts: List[Alert] = []

    for pos in positions:
        lon = pos["longitude"]
        lat = pos["latitude"]

        for aoi in aois:
            if point_in_polygon(lon, lat, aoi.coordinates):
                alerts.append(
                    Alert(
                        id=f"{pos.get('norad_id', pos['name'])}-{aoi.id}",
                        type="satellite_over_aoi",
                        severity=aoi.priority,
                        title=f"{pos['name']} sobre {aoi.name}",
                        message=(
                            f"Satélite {pos['name']} dentro de la zona "
                            f"'{aoi.name}' ({aoi.priority})"
                        ),
                        satellite_name=pos["name"],
                        satellite_norad=pos.get("norad_id"),
                        aoi_id=aoi.id,
                        aoi_name=aoi.name,
                        latitude=lat,
                        longitude=lon,
                        altitude_km=pos["altitude_km"],
                        timestamp_utc=pos.get("timestamp_utc", now),
                    )
                )

    # Orden: critical > high > normal
    order = {"critical": 0, "high": 1, "normal": 2}
    alerts.sort(key=lambda a: order.get(a.severity, 9))
    return alerts
