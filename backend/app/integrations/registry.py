"""Registro explícito de conectores; no descubre ni carga plugins dinámicamente."""

import logging

from app.integrations.contracts import Connector, ConnectorHealth, SourceState

logger = logging.getLogger(__name__)


class ConnectorRegistry:
    """Registro local por proceso. La persistencia del catálogo queda para otra fase."""

    def __init__(self) -> None:
        self._connectors: dict[str, Connector] = {}

    def register(self, connector: Connector) -> None:
        connector_id = connector.connector_id.strip()
        if not connector_id:
            raise ValueError("connector_id no puede estar vacío")
        if connector_id in self._connectors:
            raise ValueError(f"El conector '{connector_id}' ya está registrado")
        self._connectors[connector_id] = connector

    def get(self, connector_id: str) -> Connector | None:
        return self._connectors.get(connector_id)

    def list_ids(self) -> list[str]:
        return sorted(self._connectors)

    async def check_all(self) -> list[ConnectorHealth]:
        """Consultar salud de conectores conocidos sin abortar por una fuente caída."""
        results: list[ConnectorHealth] = []
        for connector_id in self.list_ids():
            connector = self._connectors[connector_id]
            try:
                health = await connector.health_check()
                if health.connector_id != connector_id:
                    logger.error("Connector health response ID mismatch for %s", connector_id)
                    health = ConnectorHealth(
                        connector_id=connector_id,
                        state=SourceState.DEGRADED,
                        message="El identificador de salud no coincide con el catálogo.",
                    )
                results.append(health)
            except Exception:
                # No registrar el texto crudo de una excepción del proveedor:
                # algunas bibliotecas incluyen URLs o credenciales en ella.
                logger.error("Health check failed for connector %s", connector_id)
                results.append(
                    ConnectorHealth(
                        connector_id=connector_id,
                        state=SourceState.UNAVAILABLE,
                        message="No se pudo comprobar el conector; revise los logs del servidor.",
                    )
                )
        return results


connector_registry = ConnectorRegistry()
