# SOFTWARE AVANZADO

**Sistema ISR en tiempo real — cuadro de mando táctico unificado**

Satélites · Cámaras · Zonas de interés · **Alertas** en un solo panel.

---

## Arquitectura (v0.6)

```
┌──────────────────────────────────────────────────────────┐
│         Cuadro de Mando Táctico (React + MapLibre)       │
│  Capas SAT + CAM + AOI · Alertas · Detalle unificado     │
└──────────────────────────┬───────────────────────────────┘
                           │ REST + WebSocket
┌──────────────────────────▼───────────────────────────────┐
│                   Backend FastAPI                        │
│  /satellite  /cameras  /aoi  /alerts/check  /ws          │
└──────────────────────────────────────────────────────────┘
```

## Arranque

```bash
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

cd frontend/tactical-map && npm install && npm run dev
```

- Panel: http://localhost:5173  
- API: http://localhost:8000/docs

## Capas y lógica táctica

| Elemento | Descripción |
|----------|-------------|
| Satélites | Posiciones en vivo (WebSocket) |
| Cámaras | Surface OSINT georreferenciado |
| AOI | Zonas de interés (polígonos) |
| **Alertas** | Satélite dentro de una AOI (`GET /alerts/check`) |

Las alertas se refrescan cada 15s y se muestran en el panel lateral ordenadas por severidad (critical → high → normal).

## Estado

- [x] Space Domain (SGP4 + caché + WebSocket)
- [x] Surface OSINT (cámaras)
- [x] Zonas de interés (AOI)
- [x] Alertas satélite-sobre-AOI
- [x] Cuadro de mando unificado
- [ ] Docker

**Clasificación:** Uso privado / desarrollo interno
