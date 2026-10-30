from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from app.satellite.tle import get_satellites
from app.satellite.propagator import propagate, propagate_many
from app.satellite.cache import cache_stats, clear_cache

router = APIRouter(prefix="/satellite", tags=["Satellite / Space Domain"])


@router.get("/groups")
async def list_groups():
    """Grupos de TLE disponibles en CelesTrak"""
    return {
        "groups": [
            "stations",
            "visual",
            "active",
            "military",
            "weather",
            "noaa",
            "gps-ops",
            "starlink",
            "science",
        ]
    }


@router.get("/tle/{group}")
async def get_tle(
    group: str = "stations",
    force_refresh: bool = Query(False, description="Forzar descarga fresca desde CelesTrak"),
):
    """Obtiene (y cachea) un grupo de TLE parseado"""
    try:
        sats = await get_satellites(group, force_refresh=force_refresh)
        return {"group": group, "count": len(sats), "satellites": sats}
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/position")
async def get_position(
    line1: str = Query(..., description="Línea 1 del TLE"),
    line2: str = Query(..., description="Línea 2 del TLE"),
    name: str = Query("UNKNOWN", description="Nombre del satélite"),
):
    """Posición geodésica de un satélite (lat/lon/alt) lista para mapa"""
    result = propagate(line1, line2, name=name)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/positions/{group}")
async def get_positions(
    group: str = "stations",
    limit: Optional[int] = Query(None, description="Máximo de satélites a devolver"),
    force_refresh: bool = Query(False, description="Forzar descarga fresca de TLE"),
):
    """
    Posiciones geodésicas de un grupo completo.
    Usa caché de TLE (TTL 2h). Ideal para el mapa táctico.
    """
    try:
        sats = await get_satellites(group, force_refresh=force_refresh)

        if limit is not None and limit > 0:
            sats = sats[:limit]

        positions = propagate_many(sats)

        return {
            "group": group,
            "count": len(positions),
            "timestamp_utc": positions[0]["timestamp_utc"] if positions else None,
            "cached": not force_refresh,
            "satellites": positions,
        }
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/cache/stats")
async def get_cache_stats():
    """Estado actual de la caché de TLE"""
    return {"cache": cache_stats()}


@router.delete("/cache")
async def clear_tle_cache(group: Optional[str] = Query(None)):
    """Limpia la caché (un grupo o toda)"""
    await clear_cache(group)
    return {"status": "cleared", "group": group or "all"}


@router.get("/propagate")
async def propagate_satellite(
    line1: str = Query(..., description="Línea 1 del TLE"),
    line2: str = Query(..., description="Línea 2 del TLE"),
    name: str = Query("UNKNOWN"),
):
    """[Legacy] Propaga un satélite (devuelve geodésicas)"""
    result = propagate(line1, line2, name=name)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
