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

# Pruebas del backend (sin dependencias adicionales)
cd backend && python -m unittest discover -s tests -v
```

| Servicio | URL |
|----------|-----|
| Cuadro de mando | http://localhost:5173 |
| API + docs | http://localhost:8000/docs |
| **Estado integraciones** | http://localhost:8000/system/status |

Por defecto, Docker publica el panel y la API solo en `127.0.0.1`. Para permitir
otros orígenes web, configura `CORS_ORIGINS` en `backend/.env` como una lista
separada por comas. No uses `*` en despliegues expuestos a Internet.

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
| **Space-Track** | No | No implementada | Configuración declarada; sin adaptador activo |
| **N2YO** | No | No implementada | Configuración declarada; sin adaptador activo |
| **ADS-B** (aviones) | No | No implementada | Configuración declarada; sin adaptador activo |
| **AIS** (buques) | No | No implementada | Configuración declarada; sin adaptador activo |
| **Cámaras** | No | Datos semilla de demostración | Sin inventario ni descubrimiento IP; plan de cámaras autorizadas |
| **Shodan** | No | No implementada | No se usa para encontrar cámaras ajenas |

### Cómo agregar una clave

```bash
cd backend
cp .env.example .env
# editá .env
```

Reiniciá el backend y mirá: **http://localhost:8000/system/status**

Guía detallada: **[docs/apis.md](docs/apis.md)**

### Prioridad recomendada

1. **Identidad y permisos** — requeridos antes de exponer inventario sensible
2. **Inventario autorizado de cámaras** — alcance aprobado, sin escaneo de terceros
3. **Space-Track / ADS-B / AIS** — conectores explícitos según permiso y caso de uso

---

## Plan de implementación

La estructura de conectores, las acciones previstas y sus criterios de aceptación están en **[docs/IMPLEMENTACION_INICIAL.md](docs/IMPLEMENTACION_INICIAL.md)**. El esquema inicial de cámara solo valida datos de inventario; aún no abre conexiones ni expone endpoints de administración.

La expansión por dominios, carpetas y fases está en **[ROADMAP_PLATAFORMA.md](ROADMAP_PLATAFORMA.md)**. Aviación ADS-B, radar, AIS, clima y telemetría/contenido satelital externo no están conectados todavía. Para cámaras y telemetría se requieren fuentes, hardware y permisos del operador; no se buscan equipos o enlaces privados.

## Capacidades del panel

- Satélites LIVE (WebSocket)
- Trazas orbitales al click
- Clasificación táctica
- Cámaras de demostración + AOI (sin acceso remoto a cámaras)
- Alertas (satélite sobre zona)
- Pases previstos  

**Clasificación:** Uso privado / desarrollo interno


### Satélites: órbita y telemetría no son lo mismo

Hoy la capa satelital calcula posiciones a partir de TLE de CelesTrak. La telemetría/contenido transmitido no está conectado: requerirá una API o estación terrestre autorizada y hardware/servicio compatible. No se accede a enlaces privados ni se sortean protecciones.
