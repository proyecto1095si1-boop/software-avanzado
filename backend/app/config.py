"""
Configuración del sistema y de APIs externas.
Las claves se leen de variables de entorno (archivo .env en desarrollo).
"""

import os
from functools import lru_cache
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Settings:
    # --- Ya conectado (sin clave) ---
    celestrak_base: str = os.getenv(
        "CELESTRAK_BASE",
        "https://celestrak.org/NORAD/elements/gp.php",
    )

    # --- Space Domain (opcional, mejora datos) ---
    spacetrack_user: Optional[str] = os.getenv("SPACETRACK_USER")
    spacetrack_password: Optional[str] = os.getenv("SPACETRACK_PASSWORD")
    n2yo_api_key: Optional[str] = os.getenv("N2YO_API_KEY")

    # --- Surface / movimiento (opcional) ---
    adsb_api_url: Optional[str] = os.getenv("ADSB_API_URL")  # ej. ads-b exchange o tar1090 local
    adsb_api_key: Optional[str] = os.getenv("ADSB_API_KEY")
    ais_api_url: Optional[str] = os.getenv("AIS_API_URL")
    ais_api_key: Optional[str] = os.getenv("AIS_API_KEY")

    # --- Cámaras / OSINT (opcional) ---
    camera_list_url: Optional[str] = os.getenv("CAMERA_LIST_URL")
    shodan_api_key: Optional[str] = os.getenv("SHODAN_API_KEY")

    # --- Sistema ---
    tle_cache_ttl_seconds: int = int(os.getenv("TLE_CACHE_TTL", str(2 * 60 * 60)))

    def status(self) -> dict:
        """Qué integraciones están configuradas (sin exponer secretos)."""
        return {
            "celestrak": {"configured": True, "required": True, "note": "TLE público"},
            "spacetrack": {
                "configured": bool(self.spacetrack_user and self.spacetrack_password),
                "required": False,
                "note": "TLE oficiales / más grupos",
            },
            "n2yo": {
                "configured": bool(self.n2yo_api_key),
                "required": False,
                "note": "Pases y posiciones online",
            },
            "adsb": {
                "configured": bool(self.adsb_api_url or self.adsb_api_key),
                "required": False,
                "note": "Aviones en tiempo real",
            },
            "ais": {
                "configured": bool(self.ais_api_url or self.ais_api_key),
                "required": False,
                "note": "Buques en tiempo real",
            },
            "cameras_remote": {
                "configured": bool(self.camera_list_url),
                "required": False,
                "note": "Lista externa de cámaras",
            },
            "shodan": {
                "configured": bool(self.shodan_api_key),
                "required": False,
                "note": "Descubrimiento de cámaras expuestas (uso cuidadoso)",
            },
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
