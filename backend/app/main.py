from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.satellite import router as satellite_router
from app.api.websocket import router as websocket_router
from app.api.cameras import router as cameras_router

app = FastAPI(
    title="Software Avanzado - ISR System",
    description="Sistema de Inteligencia, Vigilancia y Reconocimiento en tiempo real",
    version="0.3.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(satellite_router)
app.include_router(websocket_router)
app.include_router(cameras_router)


@app.get("/")
def root():
    return {
        "system": "Software Avanzado",
        "type": "ISR / Space Domain Awareness + Surface OSINT",
        "version": "0.3.0",
        "status": "online",
        "modules": ["satellite", "realtime", "cameras", "tactical-map (pending)"],
    }


@app.get("/health")
def health():
    return {"status": "ok"}
