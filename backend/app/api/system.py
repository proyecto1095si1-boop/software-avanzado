from fastapi import APIRouter

from app.config import get_settings

router = APIRouter(prefix="/system", tags=["System"])


@router.get("/status")
def system_status():
    """
    Estado del sistema e integraciones externas.
    Indica qué APIs están configuradas y cuáles faltan.
    """
    settings = get_settings()
    integrations = settings.status()

    configured = [k for k, v in integrations.items() if v["configured"]]
    missing_optional = [
        k for k, v in integrations.items()
        if not v["configured"] and not v["required"]
    ]

    return {
        "system": "Software Avanzado",
        "version": "0.8.1",
        "status": "online",
        "integrations": integrations,
        "summary": {
            "configured": configured,
            "optional_missing": missing_optional,
            "required_ok": all(
                v["configured"] for v in integrations.values() if v["required"]
            ),
        },
        "where_to_add_keys": ".env en la raíz del backend (ver .env.example)",
    }
