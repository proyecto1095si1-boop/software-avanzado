from fastapi import APIRouter, Query, HTTPException
from typing import List

from app.satellite.tle import fetch_tle_group, parse_tle
from app.satellite.propagator import propagate

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


@router.get("/propagate")
async def propagate_satellite(
    line1: str = Query(..., description="Línea 1 del TLE"),
    line2: str = Query(..., description="Línea 2 del TLE"),
):
    """Propaga un satélite a la hora actual (UTC)"""
    result = propagate(line1, line2)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
