import logging
from fastapi import APIRouter, Query, HTTPException
from datetime import datetime, timezone

from app.alerts.models import AlertListResponse
from app.alerts.service import check_satellite_over_aoi

router = APIRouter(prefix="/alerts", tags=["Alerts / Tactical"])
logger = logging.getLogger(__name__)


@router.get("/check", response_model=AlertListResponse)
async def check_alerts(
    group: str = Query("stations", description="Grupo TLE a evaluar"),
    limit: int = Query(
        200, ge=1, le=1000, description="Máximo de satélites a propagar"
    ),
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
    except Exception:
        logger.exception("No se pudieron evaluar alertas para el grupo %s", group)
        raise HTTPException(status_code=502, detail="No se pudieron evaluar las alertas")
