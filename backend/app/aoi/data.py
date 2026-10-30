"""Zonas de interés predefinidas para el cuadro de mando."""

from typing import List
from app.aoi.models import AOI

SEED_AOIS: List[AOI] = [
    AOI(
        id="aoi-ba-centro",
        name="Buenos Aires — Centro",
        description="Área metropolitana central",
        coordinates=[[-58.45, -34.55], [-58.30, -34.55], [-58.30, -34.65], [-58.45, -34.65], [-58.45, -34.55]],
        color="#3d9eff",
        priority="normal",
    ),
    AOI(
        id="aoi-ushuaia",
        name="Ushuaia — Canal Beagle",
        description="Acceso marítimo extremo sur",
        coordinates=[[-68.45, -54.75], [-68.15, -54.75], [-68.15, -54.90], [-68.45, -54.90], [-68.45, -54.75]],
        color="#f0a050",
        priority="high",
    ),
    AOI(
        id="aoi-gibraltar",
        name="Estrecho de Gibraltar",
        description="Cuello de botella marítimo",
        coordinates=[[-5.8, 35.9], [-5.2, 35.9], [-5.2, 36.2], [-5.8, 36.2], [-5.8, 35.9]],
        color="#e05c5c",
        priority="critical",
    ),
    AOI(
        id="aoi-malvinas",
        name="Islas Malvinas / Falklands",
        description="Zona de interés geopolítico",
        coordinates=[[-61.5, -51.2], [-57.5, -51.2], [-57.5, -52.5], [-61.5, -52.5], [-61.5, -51.2]],
        color="#5ce1a8",
        priority="high",
    ),
    AOI(
        id="aoi-panama",
        name="Canal de Panamá",
        description="Corredor marítimo estratégico",
        coordinates=[[-80.0, 8.8], [-79.4, 8.8], [-79.4, 9.4], [-80.0, 9.4], [-80.0, 8.8]],
        color="#e05c5c",
        priority="critical",
    ),
    AOI(
        id="aoi-suez",
        name="Canal de Suez",
        description="Corredor marítimo Mediterráneo-Rojo",
        coordinates=[[32.2, 29.7], [32.7, 29.7], [32.7, 31.3], [32.2, 31.3], [32.2, 29.7]],
        color="#e05c5c",
        priority="critical",
    ),
    AOI(
        id="aoi-hormuz",
        name="Estrecho de Ormuz",
        description="Cuello de botella energético",
        coordinates=[[56.0, 25.5], [57.0, 25.5], [57.0, 26.8], [56.0, 26.8], [56.0, 25.5]],
        color="#e05c5c",
        priority="critical",
    ),
    AOI(
        id="aoi-taiwan",
        name="Estrecho de Taiwán",
        description="Corredor Indo-Pacífico",
        coordinates=[[118.0, 22.0], [121.5, 22.0], [121.5, 26.0], [118.0, 26.0], [118.0, 22.0]],
        color="#f0a050",
        priority="high",
    ),
]


def get_all_aois() -> List[AOI]:
    return SEED_AOIS.copy()
