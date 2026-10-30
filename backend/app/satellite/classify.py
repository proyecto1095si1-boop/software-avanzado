"""
Clasificación heurística de satélites para el cuadro de mando ISR.
Basada en nombre + grupo de origen (no es inteligencia oficial).
"""

from typing import Dict, Optional

# Palabras clave orientativas
MILITARY_KW = (
    "USA ", "NROL", "NOSS", "INTRUDER", "LACROSSE", "ONYX",
    "KEYHOLE", "ADVANCED ORION", "MENTOR", "TRUMPET", "SBIRS",
    "DSP ", "MILSTAR", "AEHF", "WGS ", "MUOS", "GPS ", "NAVSTAR",
    "COSMOS", "YUNHAI", "GAOFEN", "YAOGAN", "JILIN",
)
RECON_KW = ("NROL", "KEYHOLE", "LACROSSE", "YAOGAN", "GAOFEN", "JILIN", "NOSS")
COMMS_KW = ("INTELSAT", "IRIDIUM", "GLOBALSTAR", "ORBCOMM", "SES ", "EUTELSAT")
WEATHER_KW = ("NOAA", "GOES", "METEOR", "METOP", "HIMAWARI", "FENGYUN")
NAV_KW = ("GPS", "NAVSTAR", "GLONASS", "GALILEO", "BEIDOU", "QZSS")
SCIENCE_KW = ("HUBBLE", "JWST", "TERRA", "AQUA", "AURA", "LANDSAT", "SENTINEL")
STATION_KW = ("ISS", "ZARYA", "TIANGONG", "CSS", "SALYUT", "MIR ")


def classify_satellite(name: str, group: Optional[str] = None) -> Dict:
    """Devuelve categoría táctica y flags útiles para el panel."""
    n = (name or "").upper()
    g = (group or "").lower()

    category = "unknown"
    tags = []

    if g == "military" or any(k in n for k in MILITARY_KW):
        category = "military"
        tags.append("military")
    if any(k in n for k in RECON_KW):
        category = "reconnaissance"
        tags.append("recon")
    if g == "starlink" or "STARLINK" in n:
        category = "mega-constellation"
        tags.append("starlink")
    if g in ("weather", "noaa") or any(k in n for k in WEATHER_KW):
        category = "weather"
        tags.append("weather")
    if g == "gps-ops" or any(k in n for k in NAV_KW):
        category = "navigation"
        tags.append("nav")
    if any(k in n for k in STATION_KW) or g == "stations":
        if category == "unknown":
            category = "station"
        tags.append("station")
    if any(k in n for k in COMMS_KW):
        if category == "unknown":
            category = "communications"
        tags.append("comms")
    if any(k in n for k in SCIENCE_KW) or g == "science":
        if category == "unknown":
            category = "science"
        tags.append("science")

    if category == "unknown" and g == "visual":
        category = "visual"

    interest = category in ("military", "reconnaissance", "station")

    return {
        "category": category,
        "tags": list(dict.fromkeys(tags)),
        "high_interest": interest,
    }
