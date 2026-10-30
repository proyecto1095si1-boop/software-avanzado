"""
Inventario inicial de cámaras públicas (Surface OSINT).
Lista curada y de alta calidad. Se irá expandiendo.
Solo feeds públicos por diseño.
"""

from typing import List
from app.cameras.models import Camera, CameraType, CameraStatus

# Inventario semilla — cámaras públicas conocidas y estables
SEED_CAMERAS: List[Camera] = [
    Camera(
        id="iss-hd",
        name="ISS HD Earth Viewing Experiment",
        latitude=0.0,
        longitude=0.0,
        url="https://www.youtube.com/watch?v=xRFjfp9RAHR",
        type=CameraType.other,
        status=CameraStatus.online,
        country="Space",
        city="ISS",
        source="nasa",
        notes="Cámara a bordo de la ISS mirando la Tierra (referencia)",
    ),
    Camera(
        id="ushuaia-port",
        name="Ushuaia - Puerto",
        latitude=-54.8019,
        longitude=-68.3030,
        url="https://www.ultracam.com.ar/",
        type=CameraType.marine,
        status=CameraStatus.unknown,
        country="AR",
        city="Ushuaia",
        source="curated",
        notes="Zona estratégica extremo sur",
    ),
    Camera(
        id="buenos-aires-obelisco",
        name="Buenos Aires - Obelisco",
        latitude=-34.6037,
        longitude=-58.3816,
        url=None,
        type=CameraType.traffic,
        status=CameraStatus.unknown,
        country="AR",
        city="Buenos Aires",
        source="curated",
    ),
    Camera(
        id="madrid-plaza-mayor",
        name="Madrid - Plaza Mayor",
        latitude=40.4154,
        longitude=-3.7074,
        url=None,
        type=CameraType.tourism,
        status=CameraStatus.unknown,
        country="ES",
        city="Madrid",
        source="curated",
    ),
    Camera(
        id="london-trafalgar",
        name="London - Trafalgar Square",
        latitude=51.5081,
        longitude=-0.1281,
        url=None,
        type=CameraType.tourism,
        status=CameraStatus.unknown,
        country="GB",
        city="London",
        source="curated",
    ),
    Camera(
        id="nyc-times-square",
        name="New York - Times Square",
        latitude=40.7580,
        longitude=-73.9855,
        url=None,
        type=CameraType.tourism,
        status=CameraStatus.unknown,
        country="US",
        city="New York",
        source="curated",
    ),
    Camera(
        id="tokyo-shibuya",
        name="Tokyo - Shibuya Crossing",
        latitude=35.6595,
        longitude=139.7004,
        url=None,
        type=CameraType.traffic,
        status=CameraStatus.unknown,
        country="JP",
        city="Tokyo",
        source="curated",
    ),
    Camera(
        id="singapore-marina",
        name="Singapore - Marina Bay",
        latitude=1.2868,
        longitude=103.8545,
        url=None,
        type=CameraType.tourism,
        status=CameraStatus.unknown,
        country="SG",
        city="Singapore",
        source="curated",
    ),
]


def get_all_cameras() -> List[Camera]:
    """Devuelve el inventario actual de cámaras."""
    return SEED_CAMERAS.copy()
