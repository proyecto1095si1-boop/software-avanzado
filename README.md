# SOFTWARE AVANZADO

**Sistema de Inteligencia, Vigilancia y Reconocimiento (ISR) en Tiempo Real**

Plataforma privada orientada a operaciones de conciencia situacional militar. Integra tracking satelital global y feeds de cámaras públicas en un **cuadro de mando táctico unificado**.

---

## Concepto

- **ISR** (Intelligence, Surveillance, Reconnaissance)
- Conciencia situacional en tiempo real
- Sensores espaciales + sensores terrestres abiertos (OSINT)
- Un solo panel: mapa táctico + capas de satélites + cámaras

---

## Arquitectura actual (v0.4)

```
┌─────────────────────────────────────────────────────┐
│           Cuadro de Mando Táctico (React)           │
│  MapLibre · capas satélites + cámaras · panel detalle│
└───────────────────────┬─────────────────────────────┘
                        │ REST + WebSocket
┌───────────────────────▼─────────────────────────────┐
│              Backend FastAPI (Python)               │
│  /satellite/*  ·  /cameras/*  ·  /ws/satellite/*    │
└─────────────────────────────────────────────────────┘
```

### Backend
- Propagación SGP4 + skyfield → lat/lon/alt
- Caché TLE (TTL 2h)
- WebSocket de posiciones en vivo
- API de cámaras públicas con filtros geográficos

### Frontend (`frontend/tactical-map`)
- React + TypeScript + MapLibre + Zustand
- Mapa oscuro táctico
- Capas unificadas (satélites verdes / cámaras naranja)
- Selector de grupo orbital
- Detalle al click + barra de estado LIVE

---

## Arranque completo

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (otra terminal)
cd frontend/tactical-map
npm install
npm run dev
```

- API docs: http://localhost:8000/docs  
- Cuadro de mando: http://localhost:5173

---

## Estado (v0.4)

- [x] Backend satelital (posiciones geodésicas + caché + WebSocket)
- [x] Módulo de cámaras (Surface OSINT)
- [x] **Cuadro de mando táctico unificado** (satélites + cámaras en el mismo mapa)
- [ ] Más fuentes de cámaras
- [ ] Zonas de interés / alertas
- [ ] Docker

---

**Clasificación:** Uso privado / desarrollo interno  
**Enfoque:** Conciencia situacional integrada — dominio espacial + superficie
