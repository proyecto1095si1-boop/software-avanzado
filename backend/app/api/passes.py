from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from app.satellite.tle import get_satellites
from app.aoi.data import get_all_aois
from app.satellite.passes import predict_passes

router = APIRouter(prefix="/satellite", tags=["Satellite / Passes"])


@router.get("/passes")
async def get_passes(
    group: str = Query("stations", description="Grupo TLE"),
    hours: float = Query(6.0, ge=1.0, le=24.0, description="Horas hacia adelante"),
    max_sats: int = Query(30, ge=1, le=80, description="Máximo de satélites a evaluar"),
    aoi_id: Optional[str] = Query(None, description="Filtrar por una AOI concreta"),
):
    """
    Predice pases de satélites sobre zonas de interés (AOI)
    en las próximas N horas.
    """
    try:
        sats = await get_satellites(group)
        aois = get_all_aois()
        if aoi_id:
            aois = [a for a in aois if a.id == aoi_id]
            if not aois:
                raise HTTPException(status_code=404, detail=f"AOI '{aoi_id}' no encontrada")

        passes = predict_passes(
            satellites=sats,
            aois=aois,
            hours_ahead=hours,
            step_seconds=90,
            max_sats=max_sats,
        )

        return {
            "group": group,
            "hours_ahead": hours,
            "aoi_count": len(aois),
            "satellites_evaluated": min(len(sats), max_sats),
            "count": len(passes),
            "passes": passes,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
