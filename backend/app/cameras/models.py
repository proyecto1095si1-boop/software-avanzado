"""
Modelos de datos para el módulo de cámaras públicas (Surface OSINT).
"""

from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum


class CameraType(str, Enum):
    traffic = "traffic"
    weather = "weather"
    webcam = "webcam"
    tourism = "tourism"
    marine = "marine"
    aviation = "aviation"
    other = "other"


class CameraStatus(str, Enum):
    online = "online"
    offline = "offline"
    unknown = "unknown"


class Camera(BaseModel):
    id: str = Field(..., description="Identificador único de la cámara")
    name: str
    latitude: float
    longitude: float
    url: Optional[str] = Field(None, description="URL del stream o página de la cámara")
    type: CameraType = CameraType.other
    status: CameraStatus = CameraStatus.unknown
    country: Optional[str] = None
    city: Optional[str] = None
    source: Optional[str] = Field(None, description="Origen de la cámara (lista, insecam, etc.)")
    notes: Optional[str] = None


class CameraListResponse(BaseModel):
    count: int
    cameras: List[Camera]


class CameraFilter(BaseModel):
    type: Optional[CameraType] = None
    country: Optional[str] = None
    status: Optional[CameraStatus] = None
    bbox: Optional[str] = Field(
        None,
        description="Bounding box: min_lon,min_lat,max_lon,max_lat",
    )
