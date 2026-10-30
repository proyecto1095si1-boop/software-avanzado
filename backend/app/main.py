from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.satellite import router as satellite_router

app = FastAPI(
    title="Software Avanzado - ISR System",
    description="Sistema de Inteligencia, Vigilancia y Reconocimiento en tiempo real",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(satellite_router)


@app.get("/")
def root():
    return {
        "system": "Software Avanzado",
        "type": "ISR / Space Domain Awareness",
        "status": "online",
        "modules": ["satellite", "cameras", "tactical-map"],
    }


@app.get("/health")
def health():
    return {"status": "ok"}
