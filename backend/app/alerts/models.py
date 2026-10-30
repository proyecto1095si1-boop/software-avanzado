from typing import List, Optional
from pydantic import BaseModel


class Alert(BaseModel):
    id: str
    type: str  # satellite_over_aoi
    severity: str  # normal | high | critical
    title: str
    message: str
    satellite_name: str
    satellite_norad: Optional[str] = None
    aoi_id: str
    aoi_name: str
    latitude: float
    longitude: float
    altitude_km: float
    timestamp_utc: str


class AlertListResponse(BaseModel):
    count: int
    alerts: List[Alert]
    timestamp_utc: Optional[str] = None
