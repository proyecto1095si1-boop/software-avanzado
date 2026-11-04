"""Registro explícito de conectores al arranque.

No realiza descubrimiento dinámico ni carga plugins. Solo registra
los adaptadores que el operador ha activado en código.
"""

import logging

from app.integrations.providers.space import CelesTrakConnector
from app.integrations.registry import connector_registry

logger = logging.getLogger(__name__)

_registered = False


def register_connectors() -> None:
    """Idempotente: registra los conectores activos una sola vez."""
    global _registered
    if _registered:
        return

    try:
        connector_registry.register(CelesTrakConnector())
        logger.info("Conector registrado: celestrak")
    except ValueError as exc:
        # Ya registrado (p. ej. en recarga de uvicorn) — no es error fatal.
        logger.debug("Registro de conector: %s", exc)

    _registered = True
