"""
WebSocket para posiciones satelitales en tiempo real.
El cliente se conecta y recibe actualizaciones periódicas.
"""

import asyncio
import json
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query

from app.satellite.tle import get_satellites
from app.satellite.propagator import propagate_many

router = APIRouter(tags=["Realtime"])
logger = logging.getLogger(__name__)


@router.websocket("/ws/satellite/positions")
async def ws_satellite_positions(
    websocket: WebSocket,
    group: str = Query("stations"),
    interval: float = Query(5.0, ge=2.0, le=60.0, description="Segundos entre actualizaciones"),
    limit: int = Query(200, ge=1, le=1000),
):
    """
    Stream de posiciones geodésicas en vivo.

    Query params:
    - group: grupo CelesTrak (stations, starlink, ...)
    - interval: segundos entre pushes (mínimo 2)
    - limit: máximo de satélites
    """
    await websocket.accept()

    try:
        while True:
            try:
                sats = await get_satellites(group)
                sats = sats[:limit]

                positions = propagate_many(sats)

                payload = {
                    "type": "positions",
                    "group": group,
                    "count": len(positions),
                    "timestamp_utc": positions[0]["timestamp_utc"] if positions else None,
                    "satellites": positions,
                }

                await websocket.send_text(json.dumps(payload))

            except Exception:
                logger.exception("Falló el stream de posiciones del grupo %s", group)
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "detail": "No se pudieron actualizar las posiciones",
                }))

            await asyncio.sleep(interval)

    except WebSocketDisconnect:
        pass
