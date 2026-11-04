from fastapi import APIRouter

from app.bootstrap import register_connectors
from app.config import get_settings
from app.integrations.registry import connector_registry

router = APIRouter(prefix="/system", tags=["System"])


@router.get("/status")
async def system_status():
    """
    Estado del sistema e integraciones externas.
    Combina la configuración declarada (Settings) con la salud viva
    de los conectores registrados.
    """
    register_connectors()

    settings = get_settings()
    integrations = settings.status()

    # Salud en vivo de los conectores que implementan el protocolo.
    live_health = await connector_registry.check_all()
    health_by_id = {h.connector_id: h.model_dump(mode="json") for h in live_health}

    configured = [k for k, v in integrations.items() if v["configured"]]
    missing_optional = [
        k for k, v in integrations.items()
        if not v["configured"] and not v["required"]
    ]

    return {
        "system": "Software Avanzado",
        "version": "0.9.0",
        "status": "online",
        "integrations": integrations,
        "connector_health": health_by_id,
        "registered_connectors": connector_registry.list_ids(),
        "summary": {
            "configured": configured,
            "optional_missing": missing_optional,
            "required_ok": all(
                v["configured"] for v in integrations.values() if v["required"]
            ),
            "live_connectors": len(live_health),
        },
        "where_to_add_keys": ".env en la raíz del backend (ver .env.example)",
    }
