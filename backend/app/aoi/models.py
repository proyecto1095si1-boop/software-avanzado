"""Zonas de interés (Areas of Interest) para el cuadro de mando táctico."""

from typing import List, Optional
from pydantic import BaseModel, Field


class AOI(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    # Polygon as list of [lon, lat] rings (GeoJSON-style exterior ring)
    coordinates: List[List[float]] = Field(
        ...,
        description="Anillo exterior [[lon, lat], ...]"
    )
    color: str = "#3d9eff"
    priority: str = "normal"  # normal | high | critical


class AOIListResponse(BaseModel):
    count: int
    aois: List[AOI]
