from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from app.cameras.models import Camera, CameraType, CameraStatus, CameraListResponse
from app.cameras.service import list_cameras, get_camera_by_id

router = APIRouter(prefix="/cameras", tags=["Cameras / Surface OSINT"])


@router.get("", response_model=CameraListResponse)
async def get_cameras(
    type: Optional[CameraType] = Query(None, description="Filtrar por tipo"),
    country: Optional[str] = Query(None, description="Código de país (AR, ES, US...)"),
    status: Optional[CameraStatus] = Query(None, description="online / offline / unknown"),
    bbox: Optional[str] = Query(
        None,
        description="Bounding box: min_lon,min_lat,max_lon,max_lat",
    ),
):
    """
    Lista de cámaras públicas georreferenciadas.
    Filtros opcionales por tipo, país, estado y bounding box.
    """
    cameras = list_cameras(type=type, country=country, status=status, bbox=bbox)
    return CameraListResponse(count=len(cameras), cameras=cameras)


@router.get("/{camera_id}", response_model=Camera)
async def get_camera(camera_id: str):
    """Detalle de una cámara por ID"""
    camera = get_camera_by_id(camera_id)
    if not camera:
        raise HTTPException(status_code=404, detail=f"Cámara '{camera_id}' no encontrada")
    return camera
