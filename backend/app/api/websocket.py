"""
WebSocket para posiciones satelitales en tiempo real.
El cliente se conecta y recibe actualizaciones periódicas.
"""

import asyncio
import json
from typing import Optional

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query

from app.satellite.tle import get_satellites
from app.satellite.propagator import propagate_many

router = APIRouter(tags=["Realtime"])


@router.websocket("/ws/satellite/positions")
async def ws_satellite_positions(
    websocket: WebSocket,
    group: str = Query("stations"),
    interval: float = Query(5.0, description="Segundos entre actualizaciones"),
    limit: Optional[int] = Query(None),
):
    """
    Stream de posiciones geodésicas en vivo.

    Query params:
    - group: grupo CelesTrak (stations, starlink, ...)
    - interval: segundos entre pushes (mínimo 2)
    - limit: máximo de satélites
    """
    await websocket.accept()

    # Limitar intervalo para no saturar
    interval = max(2.0, min(interval, 60.0))

    try:
        while True:
            try:
                sats = await get_satellites(group)
                if limit is not None and limit > 0:
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

            except Exception as e:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "detail": str(e),
                }))

            await asyncio.sleep(interval)

    except WebSocketDisconnect:
        pass
