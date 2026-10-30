from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from datetime import datetime, timezone

from app.alerts.models import AlertListResponse
from app.alerts.service import check_satellite_over_aoi

router = APIRouter(prefix="/alerts", tags=["Alerts / Tactical"])


@router.get("/check", response_model=AlertListResponse)
async def check_alerts(
    group: str = Query("stations", description="Grupo TLE a evaluar"),
    limit: Optional[int] = Query(200, description="Máximo de satélites a propagar"),
):
    """
    Evalúa posiciones actuales del grupo contra todas las AOI.
    Devuelve alertas satellite_over_aoi ordenadas por severidad.
    """
    try:
        alerts = await check_satellite_over_aoi(group=group, limit=limit)
        return AlertListResponse(
            count=len(alerts),
            alerts=alerts,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
