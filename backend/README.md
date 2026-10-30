# Backend - Software Avanzado (ISR)

## Arranque rápido

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Documentación automática: http://localhost:8000/docs

## Endpoints actuales

| Endpoint | Descripción |
|----------|-------------|
| `GET /` | Estado del sistema |
| `GET /health` | Health check |
| `GET /satellite/groups` | Grupos de TLE disponibles |
| `GET /satellite/tle/{group}` | Descarga y parsea TLE de un grupo |
| `GET /satellite/position?line1=...&line2=...&name=...` | **Posición geodésica** de un satélite (lat/lon/alt) |
| `GET /satellite/positions/{group}?limit=50` | **Batch** de posiciones geodésicas listas para mapa |
| `GET /satellite/propagate?...` | Legacy (ahora también devuelve geodésicas) |

### Ejemplo de respuesta (`/satellite/positions/stations`)

```json
{
  "group": "stations",
  "count": 12,
  "timestamp_utc": "2026-10-30T02:15:00+00:00",
  "satellites": [
    {
      "name": "ISS (ZARYA)",
      "norad_id": "25544",
      "latitude": -12.345678,
      "longitude": -45.678901,
      "altitude_km": 421.5,
      "speed_km_s": 7.66,
      "timestamp_utc": "2026-10-30T02:15:00+00:00"
    }
  ]
}
```

## Estado actual

- ✅ Propagación SGP4 + skyfield
- ✅ Conversión ECI → latitud / longitud / altitud
- ✅ Endpoint batch listo para mapa táctico
- ⏳ Caché de TLE
- ⏳ WebSocket de posiciones en vivo
- ⏳ Módulo de cámaras públicas

## Próximos pasos

1. Caché en memoria / Redis de grupos TLE
2. WebSocket `/ws/satellite/positions`
3. Módulo de cámaras (Surface OSINT)
4. Frontend táctico (MapLibre / Cesium)
