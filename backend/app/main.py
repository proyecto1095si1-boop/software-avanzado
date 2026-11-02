from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.satellite import router as satellite_router
from app.api.websocket import router as websocket_router
from app.api.cameras import router as cameras_router
from app.api.aoi import router as aoi_router
from app.api.alerts import router as alerts_router
from app.api.passes import router as passes_router
from app.api.track import router as track_router
from app.api.system import router as system_router
from app.config import get_settings

settings = get_settings()
app = FastAPI(
    title=f"{settings.app_name} - ISR System",
    description="Sistema de Inteligencia, Vigilancia y Reconocimiento en tiempo real",
    version="0.8.1",
    docs_url="/docs" if settings.docs_enabled else None,
    redoc_url="/redoc" if settings.docs_enabled else None,
    openapi_url="/openapi.json" if settings.docs_enabled else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Rutas internas unificadas ---
app.include_router(system_router)
app.include_router(satellite_router)
app.include_router(passes_router)
app.include_router(track_router)
app.include_router(websocket_router)
app.include_router(cameras_router)
app.include_router(aoi_router)
app.include_router(alerts_router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Return a stable error envelope without leaking implementation details."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected server error occurred.",
            "path": request.url.path,
        },
    )


@app.get("/")
def root():
    return {
        "system": "Software Avanzado",
        "type": "ISR / SDA + OSINT + AOI + Alerts + Passes + Tracks",
        "version": "0.8.1",
        "status": "online",
        "docs": "/docs",
        "integrations": "/system/status",
        "modules": [
            "satellite",
            "passes",
            "tracks",
            "classification",
            "realtime",
            "cameras",
            "aoi",
            "alerts",
            "tactical-map",
        ],
    }


@app.get("/health")
def health():
    return {"status": "ok"}
