# SOFTWARE AVANZADO

**Sistema ISR en tiempo real — cuadro de mando táctico unificado**

Satélites · Cámaras · AOI · Alertas · **Pases previstos** · Docker

---

## Arranque rápido (Docker)

```bash
docker compose up --build
```

- Cuadro de mando: http://localhost:5173  
- API: http://localhost:8000/docs

## Arranque en desarrollo

```bash
# Backend
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend/tactical-map && npm install && npm run dev
```

---

## Capacidades (v0.7)

| Módulo | Descripción |
|--------|-------------|
| **Space Domain** | TLE CelesTrak + SGP4/skyfield → lat/lon/alt |
| **Realtime** | WebSocket de posiciones en vivo |
| **Surface OSINT** | Cámaras públicas georreferenciadas |
| **AOI** | Zonas de interés (polígonos tácticos) |
| **Alertas** | Satélite **ahora** dentro de una AOI |
| **Pases** | Predicción de entradas/salidas sobre AOI (próximas horas) |
| **Panel** | Un solo mapa: capas + alertas + pases + detalle |

### Endpoints clave

- `GET /satellite/positions/{group}` — batch geodésico
- `WS /ws/satellite/positions` — stream en vivo
- `GET /alerts/check?group=stations` — cruces actuales
- `GET /satellite/passes?group=stations&hours=6` — pases previstos
- `GET /cameras` · `GET /aoi`

---

## Arquitectura

```
┌─────────────────────────────────────────────────┐
│     Cuadro de Mando (React + MapLibre)          │
│  SAT · CAM · AOI · Alertas · Pases · Detalle    │
└──────────────────────┬──────────────────────────┘
                       │ REST + WS
┌──────────────────────▼──────────────────────────┐
│              Backend FastAPI                    │
│  satellite · passes · alerts · cameras · aoi    │
└─────────────────────────────────────────────────┘
```

**Clasificación:** Uso privado / desarrollo interno
