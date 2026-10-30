# Backend - Software Avanzado (ISR)

## Arranque rápido

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Documentación automática: http://localhost:8000/docs

## Endpoints actuales

- `GET /` → Estado del sistema
- `GET /health` → Health check
- `GET /satellite/groups` → Grupos de TLE disponibles
- `GET /satellite/tle/{group}` → Descarga y parsea TLE de un grupo (ej: stations, military, starlink)
- `GET /satellite/propagate?line1=...&line2=...` → Propaga posición actual de un satélite

## Próximos pasos

1. Convertir ECI a lat/lon/alt (geodésicas)
2. Endpoint de posiciones en tiempo real de múltiples satélites
3. Módulo de cámaras públicas
4. WebSocket para actualizaciones en vivo
