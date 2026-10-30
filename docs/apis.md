# APIs del sistema — qué necesitás y dónde van

## Mapa rápido

| API | ¿Obligatoria? | ¿Ya conectada? | Dónde se configura | Dónde se usa en código |
|-----|---------------|----------------|--------------------|-------------------------|
| **CelesTrak** (TLE) | Sí | **Sí** | `CELESTRAK_BASE` (opcional) | `backend/app/satellite/tle.py` |
| **Space-Track** | No | No (lista) | `.env` → `SPACETRACK_*` | Futuro: `integrations/spacetrack.py` |
| **N2YO** | No | No (lista) | `.env` → `N2YO_API_KEY` | Futuro: pases online |
| **ADS-B** | No | No | `.env` → `ADSB_*` | Futuro: capa aviones |
| **AIS** | No | No | `.env` → `AIS_*` | Futuro: capa buques |
| **Lista cámaras** | No | Semilla local | `.env` → `CAMERA_LIST_URL` | `cameras/data.py` |
| **Shodan** | No | No | `.env` → `SHODAN_API_KEY` | Futuro: discovery |

---

## 1. Ya conectada (no hace falta clave)

### CelesTrak
- **Qué da:** TLE de todos los grupos (stations, military, starlink…)
- **Dónde está:** `backend/app/satellite/tle.py`
- **Cómo:** HTTP GET público, sin registro
- El sistema **ya funciona** solo con esto

---

## 2. Recomendadas (mejoran mucho el ISR)

### Space-Track.org
- **Qué da:** TLE oficiales, más objetos, historial
- **Registro:** https://www.space-track.org (gratis, con aprobación)
- **Variables:**
  ```
  SPACETRACK_USER=tu_usuario
  SPACETRACK_PASSWORD=tu_password
  ```
- **Dónde agregar la lógica:** `backend/app/integrations/spacetrack.py`  
  y llamar desde `tle.py` como fuente alternativa si CelesTrak falla

### N2YO
- **Qué da:** posiciones y pases visuales online
- **Registro:** https://www.n2yo.com/api/
- **Variable:** `N2YO_API_KEY=`
- **Dónde:** `backend/app/integrations/n2yo.py` → enriquecer `/satellite/passes`

---

## 3. Capas de superficie / movimiento

### ADS-B (aviones)
- **Qué da:** posiciones de aeronaves en tiempo real
- **Opciones:**
  - Propia: tar1090 / readsb → `ADSB_API_URL=http://IP:8080/data/aircraft.json`
  - OpenSky Network (límites)
  - ADS-B Exchange (comercial)
- **Dónde:** nuevo módulo `backend/app/adsb/` + capa en el mapa

### AIS (buques)
- **Qué da:** tráfico marítimo
- **Opciones:** AISStream.io, MarineTraffic API, datos propios
- **Variables:** `AIS_API_URL` / `AIS_API_KEY`
- **Dónde:** `backend/app/ais/` + capa en el mapa

---

## 4. Cámaras

Hoy: inventario **curado en código** (`cameras/data.py`).

Para escalar:
- `CAMERA_LIST_URL=` → JSON propio con `{id,name,lat,lon,url,...}`
- Shodan solo si sabés lo que hacés (legal/ético)

---

## Cómo conectar una clave (pasos)

1. En `backend/`:
   ```bash
   cp .env.example .env
   # editá .env con tus claves
   ```
2. Reiniciá el backend (`uvicorn` o `docker compose up`)
3. Verificá:
   ```
   GET http://localhost:8000/system/status
   ```
   Ahí ves qué quedó `configured: true`

---

## Prioridad sugerida

1. **Nada** — el núcleo satelital ya va con CelesTrak  
2. **Space-Track** — si querés TLE más robustos / militares  
3. **ADS-B local** — si tenés receptor o acceso a un feed  
4. **CAMERA_LIST_URL** — para crecer el inventario sin tocar código  
5. N2YO / AIS / Shodan — según necesidad operativa
