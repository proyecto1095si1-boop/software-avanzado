# Cuadro de Mando Táctico

Panel unificado de Software Avanzado (ISR).

Muestra en el mismo mapa:
- **Satélites** en tiempo real (WebSocket → backend)
- **Cámaras públicas** (API Surface OSINT)

## Requisitos

1. Backend corriendo en `http://localhost:8000`
2. Node.js 18+

## Arranque

```bash
# Terminal 1 — backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 — frontend
cd frontend/tactical-map
npm install
npm run dev
```

Abrir: http://localhost:5173

## Qué verás

- Mapa oscuro táctico (CARTO dark)
- Puntos verdes = satélites (grupo seleccionable)
- Puntos naranja = cámaras públicas
- Panel lateral: capas, grupo orbital, detalle al hacer click
- Barra de estado: LIVE / OFFLINE + contadores + timestamp UTC

## Arquitectura

```
App
├── WebSocket → /ws/satellite/positions  (posiciones en vivo)
├── REST     → /cameras                  (inventario de cámaras)
├── MapCanvas (MapLibre, 2 capas GeoJSON)
└── SidePanel (capas + detalle unificado)
```

Todo el estado vive en un store Zustand único. No hay lógica orbital en el frontend.
