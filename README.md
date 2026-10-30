# SOFTWARE AVANZADO

**Sistema ISR en tiempo real — cuadro de mando táctico unificado**

Satélites + cámaras públicas + zonas de interés (AOI) en un solo panel.

---

## Arquitectura (v0.5)

```
┌──────────────────────────────────────────────────────────┐
│         Cuadro de Mando Táctico (React + MapLibre)       │
│   Capas: Satélites · Cámaras · AOI · Detalle unificado   │
└──────────────────────────┬───────────────────────────────┘
                           │ REST + WebSocket
┌──────────────────────────▼───────────────────────────────┐
│                   Backend FastAPI                        │
│  /satellite/*  ·  /cameras/*  ·  /aoi/*  ·  /ws/*        │
└──────────────────────────────────────────────────────────┘
```

## Arranque

```bash
# Backend
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend/tactical-map && npm install && npm run dev
```

- Panel: http://localhost:5173  
- API: http://localhost:8000/docs

## Capas del mapa

| Capa | Color | Fuente |
|------|-------|--------|
| Satélites | Verde | WebSocket en vivo |
| Cámaras | Naranja | `/cameras` |
| Zonas AOI | Según prioridad | `/aoi` |

## Estado

- [x] Space Domain (SGP4 + caché + WebSocket)
- [x] Surface OSINT (cámaras georreferenciadas)
- [x] Zonas de interés (AOI)
- [x] Cuadro de mando unificado
- [ ] Alertas (satélite sobre AOI)
- [ ] Docker

**Clasificación:** Uso privado / desarrollo interno
