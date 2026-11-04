"""
Lógica de negocio del módulo de cámaras públicas.
"""

from math import isfinite
from typing import List, Optional
from app.cameras.models import Camera, CameraType, CameraStatus
from app.cameras.data import get_all_cameras


def list_cameras(
    type: Optional[CameraType] = None,
    country: Optional[str] = None,
    status: Optional[CameraStatus] = None,
    bbox: Optional[str] = None,
) -> List[Camera]:
    """
    Lista cámaras con filtros opcionales.

    bbox format: min_lon,min_lat,max_lon,max_lat
    """
    cameras = get_all_cameras()

    if type is not None:
        cameras = [c for c in cameras if c.type == type]

    if country is not None:
        country_upper = country.upper()
        cameras = [
            c for c in cameras
            if c.country and c.country.upper() == country_upper
        ]

    if status is not None:
        cameras = [c for c in cameras if c.status == status]

    if bbox is not None:
        try:
            parts = [float(x.strip()) for x in bbox.split(",")]
        except ValueError as exc:
            raise ValueError("bbox debe contener cuatro coordenadas numéricas") from exc
        if len(parts) != 4 or not all(isfinite(value) for value in parts):
            raise ValueError("bbox debe contener cuatro coordenadas numéricas finitas")
        min_lon, min_lat, max_lon, max_lat = parts
        if not (-180 <= min_lon <= 180 and -180 <= max_lon <= 180):
            raise ValueError("longitudes bbox deben estar entre -180 y 180")
        if not (-90 <= min_lat <= 90 and -90 <= max_lat <= 90):
            raise ValueError("latitudes bbox deben estar entre -90 y 90")
        if min_lat > max_lat:
            raise ValueError("latitud mínima bbox no puede superar la máxima")
        cameras = [
            c for c in cameras
            if (min_lon <= c.longitude <= max_lon if min_lon <= max_lon
                else c.longitude >= min_lon or c.longitude <= max_lon)
            and min_lat <= c.latitude <= max_lat
        ]

    return cameras


def get_camera_by_id(camera_id: str) -> Optional[Camera]:
    """Busca una cámara por su ID."""
    for cam in get_all_cameras():
        if cam.id == camera_id:
            return cam
    return None
