"""Conector CelesTrak (TLE público).

Fuente ya usada por app.satellite.tle. Este adaptador expone el mismo origen
a través del contrato Connector para health checks y catálogo futuro.
No introduce un segundo camino de datos ni cambia la API pública.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

import httpx

from app.config import get_settings
from app.integrations.contracts import ConnectorHealth, SourceState

logger = logging.getLogger(__name__)


class CelesTrakConnector:
    """Health-check y descriptor del feed TLE público de CelesTrak."""

    connector_id = "celestrak"

    def __init__(self, timeout: float = 12.0) -> None:
        self._timeout = timeout

    async def health_check(self) -> ConnectorHealth:
        settings = get_settings()
        # Consulta ligera: un grupo pequeño y formato TLE.
        url = f"{settings.celestrak_base}?GROUP=stations&FORMAT=tle"
        checked_at = datetime.now(timezone.utc)

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.get(url)
                response.raise_for_status()
                text = response.text or ""

            # Validación mínima: debe contener al menos una línea 1 / línea 2.
            has_tle = "1 " in text and "2 " in text
            if not has_tle:
                return ConnectorHealth(
                    connector_id=self.connector_id,
                    state=SourceState.DEGRADED,
                    checked_at=checked_at,
                    message="Respuesta de CelesTrak sin formato TLE reconocido.",
                )

            return ConnectorHealth(
                connector_id=self.connector_id,
                state=SourceState.HEALTHY,
                checked_at=checked_at,
                last_success_at=checked_at,
                message="TLE público disponible.",
            )
        except httpx.TimeoutException:
            logger.warning("CelesTrak health check timed out")
            return ConnectorHealth(
                connector_id=self.connector_id,
                state=SourceState.UNAVAILABLE,
                checked_at=checked_at,
                message="Tiempo de espera agotado al consultar CelesTrak.",
            )
        except httpx.HTTPStatusError as exc:
            logger.warning("CelesTrak HTTP error: %s", exc.response.status_code)
            return ConnectorHealth(
                connector_id=self.connector_id,
                state=SourceState.UNAVAILABLE,
                checked_at=checked_at,
                message=f"CelesTrak respondió HTTP {exc.response.status_code}.",
            )
        except Exception:
            # No filtrar el texto de la excepción al cliente (puede contener URL).
            logger.exception("CelesTrak health check failed")
            return ConnectorHealth(
                connector_id=self.connector_id,
                state=SourceState.UNAVAILABLE,
                checked_at=checked_at,
                message="No se pudo comprobar CelesTrak; revise los logs del servidor.",
            )
