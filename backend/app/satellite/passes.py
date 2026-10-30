"""
Predicción de pases: cuándo un satélite atraviesa una zona de interés.
Muestrea la órbita a intervalos fijos y detecta entradas/salidas del polígono.
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional

from app.satellite.propagator import propagate
from app.alerts.geo import point_in_polygon
from app.aoi.models import AOI


def predict_passes_for_satellite(
    line1: str,
    line2: str,
    name: str,
    norad_id: Optional[str],
    aoi: AOI,
    hours_ahead: float = 12.0,
    step_seconds: int = 60,
) -> List[Dict]:
    """
    Devuelve lista de pases detectados sobre la AOI.
    Cada pase: enter_utc, exit_utc, duration_s, max_altitude_km, sample points.
    """
    now = datetime.now(timezone.utc)
    steps = int((hours_ahead * 3600) / step_seconds)
    inside = False
    enter_t: Optional[datetime] = None
    max_alt = 0.0
    passes: List[Dict] = []

    for i in range(steps + 1):
        t = now + timedelta(seconds=i * step_seconds)
        pos = propagate(line1, line2, name=name, when=t)
        if "error" in pos:
            continue

        hit = point_in_polygon(pos["longitude"], pos["latitude"], aoi.coordinates)

        if hit and not inside:
            inside = True
            enter_t = t
            max_alt = pos["altitude_km"]
        elif hit and inside:
            max_alt = max(max_alt, pos["altitude_km"])
        elif not hit and inside:
            inside = False
            if enter_t is not None:
                duration = (t - enter_t).total_seconds()
                # Filtrar pases muy cortos (ruido de muestreo)
                if duration >= step_seconds:
                    passes.append({
                        "satellite_name": name,
                        "norad_id": norad_id,
                        "aoi_id": aoi.id,
                        "aoi_name": aoi.name,
                        "enter_utc": enter_t.isoformat(),
                        "exit_utc": t.isoformat(),
                        "duration_s": int(duration),
                        "max_altitude_km": round(max_alt, 1),
                        "priority": aoi.priority,
                    })
            enter_t = None
            max_alt = 0.0

    # Pase aún abierto al final de la ventana
    if inside and enter_t is not None:
        end = now + timedelta(hours=hours_ahead)
        duration = (end - enter_t).total_seconds()
        if duration >= step_seconds:
            passes.append({
                "satellite_name": name,
                "norad_id": norad_id,
                "aoi_id": aoi.id,
                "aoi_name": aoi.name,
                "enter_utc": enter_t.isoformat(),
                "exit_utc": end.isoformat(),
                "duration_s": int(duration),
                "max_altitude_km": round(max_alt, 1),
                "priority": aoi.priority,
                "ongoing": True,
            })

    return passes


def predict_passes(
    satellites: List[Dict],
    aois: List[AOI],
    hours_ahead: float = 6.0,
    step_seconds: int = 90,
    max_sats: int = 40,
) -> List[Dict]:
    """
    Predice pases de varios satélites sobre varias AOI.
    Limita cantidad de satélites para no saturar CPU.
    """
    sats = satellites[:max_sats]
    all_passes: List[Dict] = []

    for sat in sats:
        for aoi in aois:
            passes = predict_passes_for_satellite(
                line1=sat["line1"],
                line2=sat["line2"],
                name=sat.get("name", "UNKNOWN"),
                norad_id=sat.get("norad_id"),
                aoi=aoi,
                hours_ahead=hours_ahead,
                step_seconds=step_seconds,
            )
            all_passes.extend(passes)

    all_passes.sort(key=lambda p: p["enter_utc"])
    return all_passes
