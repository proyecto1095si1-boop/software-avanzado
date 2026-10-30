"""
Obtención y parseo de TLE.
Fuente principal: CelesTrak (público, sin API key).
"""

import httpx
from typing import List, Dict

from app.satellite.cache import get_cached, set_cached
from app.config import get_settings


async def fetch_tle_group(group: str = "stations") -> str:
    """Descarga un grupo de TLE desde CelesTrak."""
    base = get_settings().celestrak_base
    url = f"{base}?GROUP={group}&FORMAT=tle"
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


def parse_tle(raw: str) -> List[Dict]:
    lines = [l.strip() for l in raw.strip().splitlines() if l.strip()]
    satellites = []
    i = 0
    while i < len(lines):
        if i + 2 < len(lines) and lines[i + 1].startswith("1 ") and lines[i + 2].startswith("2 "):
            name = lines[i]
            line1 = lines[i + 1]
            line2 = lines[i + 2]
            norad_id = line1[2:7].strip()
            satellites.append({
                "name": name,
                "norad_id": norad_id,
                "line1": line1,
                "line2": line2,
            })
            i += 3
        else:
            i += 1
    return satellites


async def get_satellites(group: str = "stations", force_refresh: bool = False) -> List[Dict]:
    if not force_refresh:
        cached = await get_cached(group)
        if cached is not None:
            return cached

    raw = await fetch_tle_group(group)
    satellites = parse_tle(raw)
    await set_cached(group, satellites)
    return satellites
