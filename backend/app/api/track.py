from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from app.satellite.tle import get_satellites
from app.satellite.track import ground_track
from app.satellite.classify import classify_satellite
from app.satellite.propagator import propagate_many

router = APIRouter(prefix="/satellite", tags=["Satellite / Track"])


@router.get("/track")
async def get_track(
    line1: str = Query(...),
    line2: str = Query(...),
    name: str = Query("UNKNOWN"),
    minutes_ahead: float = Query(90, ge=10, le=180),
    minutes_behind: float = Query(30, ge=0, le=90),
):
    """Ground track (traza) de un satélite para dibujar en el mapa."""
    try:
        track = ground_track(
            line1=line1,
            line2=line2,
            name=name,
            minutes_ahead=minutes_ahead,
            minutes_behind=minutes_behind,
            step_seconds=30,
        )
        track["classification"] = classify_satellite(name)
        return track
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/track/{group}/{norad_id}")
async def get_track_by_norad(
    group: str,
    norad_id: str,
    minutes_ahead: float = Query(90, ge=10, le=180),
    minutes_behind: float = Query(30, ge=0, le=90),
):
    """Traza por NORAD id dentro de un grupo cacheado."""
    try:
        sats = await get_satellites(group)
        match = next((s for s in sats if str(s.get("norad_id")) == str(norad_id)), None)
        if not match:
            # búsqueda por nombre parcial
            match = next(
                (s for s in sats if norad_id.upper() in (s.get("name") or "").upper()),
                None,
            )
        if not match:
            raise HTTPException(status_code=404, detail=f"Satélite '{norad_id}' no encontrado en {group}")

        track = ground_track(
            line1=match["line1"],
            line2=match["line2"],
            name=match["name"],
            minutes_ahead=minutes_ahead,
            minutes_behind=minutes_behind,
        )
        track["norad_id"] = match.get("norad_id")
        track["classification"] = classify_satellite(match["name"], group)
        return track
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/classified/{group}")
async def get_classified_positions(
    group: str = "stations",
    limit: Optional[int] = Query(100),
):
    """Posiciones + clasificación táctica (para colorear el mapa)."""
    try:
        sats = await get_satellites(group)
        if limit:
            sats = sats[:limit]
        positions = propagate_many(sats)
        for p in positions:
            p["classification"] = classify_satellite(p.get("name", ""), group)
        return {
            "group": group,
            "count": len(positions),
            "satellites": positions,
        }
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
