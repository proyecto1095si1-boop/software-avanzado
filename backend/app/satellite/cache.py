"""
Caché simple en memoria para grupos TLE.
TTL por defecto: 2 horas (los TLE cambian lentamente).
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple
import asyncio

# Estructura: group -> (timestamp, list_of_satellites)
_cache: Dict[str, Tuple[datetime, List[Dict]]] = {}
_lock = asyncio.Lock()

DEFAULT_TTL_SECONDS = 2 * 60 * 60  # 2 horas


async def get_cached(group: str) -> Optional[List[Dict]]:
    """Devuelve la lista de satélites si está en caché y no ha expirado."""
    async with _lock:
        entry = _cache.get(group)
        if not entry:
            return None

        cached_at, satellites = entry
        age = (datetime.now(timezone.utc) - cached_at).total_seconds()

        if age > DEFAULT_TTL_SECONDS:
            del _cache[group]
            return None

        return satellites


async def set_cached(group: str, satellites: List[Dict]) -> None:
    """Guarda un grupo de satélites en caché."""
    async with _lock:
        _cache[group] = (datetime.now(timezone.utc), satellites)


async def clear_cache(group: Optional[str] = None) -> None:
    """Limpia la caché (un grupo o toda)."""
    async with _lock:
        if group:
            _cache.pop(group, None)
        else:
            _cache.clear()


def cache_stats() -> Dict:
    """Estado actual de la caché (útil para debug)."""
    now = datetime.now(timezone.utc)
    stats = {}
    for group, (cached_at, sats) in _cache.items():
        age = (now - cached_at).total_seconds()
        stats[group] = {
            "count": len(sats),
            "age_seconds": int(age),
            "expires_in_seconds": max(0, int(DEFAULT_TTL_SECONDS - age)),
        }
    return stats
