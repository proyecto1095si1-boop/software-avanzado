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
| `GET /satellite/tle/{group}` | TLE parseado (con caché) |
| `GET /satellite/position?...` | Posición geodésica de un satélite |
| `GET /satellite/positions/{group}` | **Batch** de posiciones listas para mapa |
| `GET /satellite/cache/stats` | Estado de la caché de TLE |
| `DELETE /satellite/cache` | Limpiar caché |
| `WS /ws/satellite/positions?group=stations&interval=5` | **Stream en vivo** de posiciones |

### Ejemplo WebSocket

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/satellite/positions?group=stations&interval=5");
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data.count, "satélites actualizados");
};
```

## Arquitectura actual

- **Propagación**: sgp4 + skyfield → lat/lon/alt listos para mapa
- **Caché TLE**: en memoria, TTL 2 horas
- **Realtime**: WebSocket con push periódico

## Estado

- [x] Propagación geodésica
- [x] Batch positions
- [x] Caché de TLE
- [x] WebSocket de posiciones en vivo
- [ ] Módulo de cámaras públicas
- [ ] Frontend táctico
