# Backend - Software Avanzado (ISR)

## Arranque rápido

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Documentación automática: http://localhost:8000/docs

## Módulos

### Satellite / Space Domain

| Endpoint | Descripción |
|----------|-------------|
| `GET /satellite/groups` | Grupos de TLE disponibles |
| `GET /satellite/tle/{group}` | TLE parseado (con caché) |
| `GET /satellite/position?...` | Posición geodésica de un satélite |
| `GET /satellite/positions/{group}` | Batch de posiciones listas para mapa |
| `GET /satellite/cache/stats` | Estado de la caché de TLE |
| `WS /ws/satellite/positions` | Stream en vivo de posiciones |

### Cameras / Surface OSINT

| Endpoint | Descripción |
|----------|-------------|
| `GET /cameras` | Lista de cámaras públicas (filtros: type, country, status, bbox) |
| `GET /cameras/{id}` | Detalle de una cámara |

Ejemplo de filtro por zona:
```
GET /cameras?bbox=-60,-40,-50,-30&country=AR
```

## Arquitectura actual

- **Propagación**: sgp4 + skyfield → lat/lon/alt
- **Caché TLE**: en memoria, TTL 2 horas
- **Realtime**: WebSocket
- **Cámaras**: inventario curado + API de filtrado geográfico

## Estado (v0.3)

- [x] Propagación geodésica
- [x] Batch positions + caché TLE
- [x] WebSocket de posiciones en vivo
- [x] Módulo de cámaras (inventario inicial + API)
- [ ] Expansión de fuentes de cámaras (Insecam-style, listas oficiales)
- [ ] Frontend táctico
