# SOFTWARE AVANZADO

**Sistema ISR unificado** — satélites, cámaras, AOI, alertas, pases y trazas en un solo cuadro de mando.

---

## Arranque

```bash
# Todo junto
docker compose up --build

# O en desarrollo
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8000
cd frontend/tactical-map && npm install && npm run dev
```

| Servicio | URL |
|----------|-----|
| Cuadro de mando | http://localhost:5173 |
| API + docs | http://localhost:8000/docs |
| **Estado integraciones** | http://localhost:8000/system/status |

---

## Qué está conectado internamente

```
Frontend (panel)  ──proxy──►  Backend FastAPI
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
   /satellite/*            /cameras  /aoi          /alerts /ws
   /passes /track              │                       │
         │                     │                       │
         ▼                     ▼                       ▼
   CelesTrak (TLE)      inventario local         motor AOI
```

Todo el frontend habla **solo** con tu backend. El backend es el que habla con el exterior.

---

## APIs externas — cuáles necesitás

| API | ¿Obligatoria? | Estado | Dónde poner la clave |
|-----|---------------|--------|----------------------|
| **CelesTrak** | Sí | **Ya conectada** | No requiere clave |
| **Space-Track** | No | Lista para cablear | `backend/.env` → `SPACETRACK_USER/PASSWORD` |
| **N2YO** | No | Lista | `N2YO_API_KEY` |
| **ADS-B** (aviones) | No | Lista | `ADSB_API_URL` / `ADSB_API_KEY` |
| **AIS** (buques) | No | Lista | `AIS_API_URL` / `AIS_API_KEY` |
| **Lista cámaras** | No | Semilla local | `CAMERA_LIST_URL` |
| **Shodan** | No | Lista | `SHODAN_API_KEY` |

### Cómo agregar una clave

```bash
cd backend
cp .env.example .env
# editá .env
```

Reiniciá el backend y mirá: **http://localhost:8000/system/status**

Guía detallada: **[docs/apis.md](docs/apis.md)**

### Prioridad recomendada

1. **Nada extra** — con CelesTrak el sistema ya opera  
2. **Space-Track** — TLE más robustos  
3. **ADS-B** (ideal feed propio) — capa aviones  
4. **CAMERA_LIST_URL** — más cámaras sin tocar código  

---

## Capacidades del panel

- Satélites LIVE (WebSocket)  
- Trazas orbitales al click  
- Clasificación táctica  
- Cámaras + AOI estratégicas  
- Alertas (satélite sobre zona)  
- Pases previstos  

**Clasificación:** Uso privado / desarrollo interno
