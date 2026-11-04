# Arquitectura de Software Avanzado

## Misión de producto

Integrar observaciones geoespaciales y sensores autorizados para un cuadro de situación con procedencia, frescura y calidad visibles. El sistema actual es un prototipo FastAPI + React/MapLibre; no está acreditado para despliegues militares, de infraestructura crítica ni Internet público.

El alcance técnico es visualización, monitoreo, eventos y análisis con supervisión humana. No incluye selección autónoma de objetivos, guía de armas, control autónomo ni acceso a dispositivos sin autorización.

## Estado implementado

- Backend FastAPI con TLE de CelesTrak, propagación orbital, trazas, pases, AOI y alertas.
- Frontend React/MapLibre con WebSocket y lista semilla local de cámaras.
- Contratos iniciales de conectores (`app/integrations/contracts.py`) para estado, procedencia, tiempo y calidad.
- Registro explícito de conectores (`app/integrations/registry.py`), sin plugin discovery ni solicitudes de red automáticas.
- Esquema de cámara autorizada (`app/cameras/inventory_schemas.py`) que valida IP/hostname y referencia de autorización. No implementa CRUD, persistencia ni conexión a la cámara.

## Arquitectura objetivo

```text
Operadores
   │ HTTPS + identidad/MFA
   ▼
Frontend (features por dominio) ── API FastAPI ── policy por usuario/sitio/recurso
                                      │
                                      ├── catálogo/estado de fuentes
                                      ├── servicios: satélite, cámara, AOI, alertas
                                      ├── repositorios ── PostgreSQL/PostGIS
                                      ├── auditoría y métricas
                                      └── cola/reintentos acotados (cuando se necesite)
                                              │
                              conectores aislados, egress restringido
                               ├── APIs astronómicas/geoespaciales
                               └── agente de borde del propietario ── cámaras/VMS
```

El navegador solo accede a la API de la aplicación y a un relay de video autorizado. Nunca guarda claves de proveedor o credenciales RTSP. Un agente de borde se ejecuta dentro de una red que el propietario administra y solo puede alcanzar los equipos ya inventariados en un scope/allowlist.

## Módulos de dominio

- `satellite/`: ingestión TLE, propagación, trazas y pases.
- `cameras/`: catálogo demo actual; futuro inventario persistente con propietario, sitio, host/IP, protocolo, alcance y autorización.
- `integrations/`: contratos de datos/salud y registro explícito; futuro adaptador individual por fuente.
- `aoi/`, `alerts/`: geometrías, reglas, cálculo de eventos y clasificación de frescura.
- `auth/`, `policy/`, `audit/`: por implementar antes de endpoints mutables o de video.
- `persistence/`: PostgreSQL/PostGIS y migraciones, por implementar antes del inventario operativo.
- `api/`: adaptadores HTTP/WebSocket finos, con autenticación, autorización por objeto, límites y errores tipados.
- `frontend/tactical-map/src/features/`: paneles independientes por dominio; `features/cameras/` define el futuro panel del inventario autorizado.

## Ciclo de una fuente externa

1. Registrar propietario, finalidad, autorización, licencia, alcance y responsable.
2. Configurar secreto fuera del repositorio y limitar permisos de la cuenta técnica.
3. Adaptador explícito valida esquema, cuota, timeout, origen, límite de carga y procedencia.
4. Normalizar como `DataEnvelope` con `source_id`, `observed_at`, `ingested_at`, `kind`, calidad y referencia de autorización.
5. Persistir solo lo necesario con retención documentada; exponer estado/frescura y auditar acceso.
6. Ante una caída, degradar esa fuente sin tumbar el resto ni mostrar datos antiguos como actuales.

## Integración de cámara

El operador aporta IP/hostname o importa el inventario de su VMS/CMDB/DHCP/DNS. El alta requiere `site_id`, `network_scope_id` y `authorization_reference`. El esquema actual valida formato solamente. La futura llamada de salud/metadatos debe comprobar permisos y scope en servidor/agente, usar ONVIF HTTPS o API oficial con privilegio mínimo y fallar de forma segura.

No hay búsqueda global, escaneo de rangos no declarados, bypass de autenticación ni lectura de cámaras de terceros. Los campos no soportados o no autorizados aparecen como no disponibles. El video, si se incorpora y se aprueba, se sirve por relay/VMS y se audita; la grabación está desactivada por defecto.

## Entorno de desarrollo

- Python 3.11+; FastAPI; `unittest` para las pruebas actuales.
- Node compatible con Vite 8; React, TypeScript, MapLibre.
- `docker compose up --build` para ejecución local; puertos loopback por defecto.
- No desplegar fuera de un entorno confiable hasta añadir autenticación, autorización, persistencia, TLS, gestión de secretos, logging seguro y revisión de amenazas.

Ver [IMPLEMENTACION_INICIAL.md](IMPLEMENTACION_INICIAL.md) para acciones, carpetas, dependencias y puertas de salida; y [decisions/ADR-0001-camera-access-scope.md](decisions/ADR-0001-camera-access-scope.md) para la decisión de alcance de cámaras.
