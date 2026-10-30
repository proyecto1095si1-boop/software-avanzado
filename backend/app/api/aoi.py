from fastapi import APIRouter, HTTPException

from app.aoi.models import AOI, AOIListResponse
from app.aoi.data import get_all_aois

router = APIRouter(prefix="/aoi", tags=["AOI / Zonas de Interés"])


@router.get("", response_model=AOIListResponse)
async def list_aois():
    """Lista de zonas de interés para el mapa táctico"""
    aois = get_all_aois()
    return AOIListResponse(count=len(aois), aois=aois)


@router.get("/{aoi_id}", response_model=AOI)
async def get_aoi(aoi_id: str):
    for a in get_all_aois():
        if a.id == aoi_id:
            return a
    raise HTTPException(status_code=404, detail=f"AOI '{aoi_id}' no encontrada")
