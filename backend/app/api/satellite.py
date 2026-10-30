from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional

from app.satellite.tle import fetch_tle_group, parse_tle
from app.satellite.propagator import propagate, propagate_many

router = APIRouter(prefix="/satellite", tags=["Satellite / Space Domain"])


@router.get("/groups")
async def list_groups():
    """Grupos de TLE disponibles en CelesTrak"""
    return {
        "groups": [
            "stations",      # ISS y estaciones
            "visual",        # Satélites visibles a ojo
            "active",        # Todos los activos
            "military",      # Satélites militares (cuando disponible)
            "weather",       # Meteorológicos
            "noaa",
            "gps-ops",
            "starlink",
            "science",
        ]
    }


@router.get("/tle/{group}")
async def get_tle(group: str = "stations"):
    """Descarga y parsea un grupo de TLE"""
    try:
        raw = await fetch_tle_group(group)
        sats = parse_tle(raw)
        return {"group": group, "count": len(sats), "satellites": sats}
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/position")
async def get_position(
    line1: str = Query(..., description="Línea 1 del TLE"),
    line2: str = Query(..., description="Línea 2 del TLE"),
    name: str = Query("UNKNOWN", description="Nombre del satélite"),
):
    """
    Propaga un satélite y devuelve posición geodésica lista para mapa.
    (latitud, longitud, altitud_km)
    """
    result = propagate(line1, line2, name=name)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/positions/{group}")
async def get_positions(
    group: str = "stations",
    limit: Optional[int] = Query(None, description="Máximo de satélites a devolver"),
):
    """
    Descarga un grupo de TLE, propaga todos y devuelve posiciones
    geodésicas listas para el mapa táctico.
    """
    try:
        raw = await fetch_tle_group(group)
        sats = parse_tle(raw)

        if limit is not None and limit > 0:
            sats = sats[:limit]

        positions = propagate_many(sats)

        return {
            "group": group,
            "count": len(positions),
            "timestamp_utc": positions[0]["timestamp_utc"] if positions else None,
            "satellites": positions,
        }
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


# Mantener el endpoint antiguo por compatibilidad (ahora redirige a geodésicas)
@router.get("/propagate")
async def propagate_satellite(
    line1: str = Query(..., description="Línea 1 del TLE"),
    line2: str = Query(..., description="Línea 2 del TLE"),
    name: str = Query("UNKNOWN"),
):
    """[Legacy] Propaga un satélite (ahora devuelve geodésicas)"""
    result = propagate(line1, line2, name=name)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
