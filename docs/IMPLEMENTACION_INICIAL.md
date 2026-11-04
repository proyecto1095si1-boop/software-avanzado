# Inicio de implementación — módulos, acciones y orden de trabajo

## Estado de este incremento

Este commit inicia la estructura técnica sin fingir que ya existe una integración real de cámaras. Se añaden contratos comunes para integraciones y un esquema de alta de cámaras autorizadas. El esquema solo valida datos; no hace conexiones, escaneo, autenticación ni lectura de video. No se exponen endpoints nuevos porque el backend todavía no autentica usuarios ni puede aplicar permisos por cámara.

## Reglas no negociables

- Solo integrar sensores y fuentes con propietario, alcance, autorización y condiciones de uso documentadas.
- No permitir a un cliente mandar una URL arbitraria para que el backend la visite. El modelo de alta admite IP o hostname, protocolo enumerado y puerto; un registro futuro deberá vincularse a `network_scope_id` aprobado por un administrador.
- No escanear rangos automáticamente. Una comprobación de salud posterior deberá operar únicamente sobre cámaras ya inventariadas y una allowlist verificada por un agente dentro de la red del propietario.
- No guardar contraseñas, tokens, URL RTSP ni secretos en el inventario o frontend. Se usarán referencias a un secret manager cuando se implemente identidad y almacenamiento.
- Aún no hay login/MFA, autorización por objeto, base de datos ni auditoría. Por ello no crear rutas mutables ni de acceso a video hasta cerrar esos requisitos.
- El sistema es de monitoreo y apoyo a operadores. No incorporar funciones de control de armas, targeting autónomo, bypass de autenticación ni acceso encubierto.

## Acciones del producto

| Acción | Actor previsto | Estado | Dependencia y criterio de aceptación |
|---|---|---|---|
| `connectors.catalog` — listar fuentes configuradas | lector autenticado | Contrato inicial | Catálogo persistente; oculta secretos y fuentes fuera del tenant. |
| `connectors.health` — consultar estado/frescura | lector autenticado | Registro en memoria implementado | Cada integración falla aislada; mensaje público redactado y timestamp. |
| `cameras.enroll` — registrar IP/hostname y sitio | administrador de sitio | Esquema inicial | Requiere identidad, permiso de sitio, autorización documentada y alcance permitido. |
| `cameras.list` / `cameras.get` — consultar inventario | usuario con permiso por objeto | Pendiente | Pruebas contra IDOR: cambiar un ID no permite leer otro tenant/sitio. |
| `cameras.check_health` — consultar disponibilidad | agente de borde autorizado | Pendiente, bloqueada por allowlist | Solo equipo registrado, protocolo permitido, egress restringido y rate limit. No hace barrido de red. |
| `cameras.read_metadata` — consultar capacidades/firmware | cuenta técnica de mínimo privilegio | Pendiente, después de ONVIF/VMS | Fuente, hora, permiso y campos disponibles; no solicita ni infiere campos no expuestos. |
| `streams.open` — abrir video autorizado | operador con permiso temporal | Fuera del primer incremento | Relay/VMS, URLs efímeras, no hay credenciales en navegador, auditoría y corte al revocar. |
| `events.ingest` — normalizar eventos de fuente | conector autenticado | Contrato de dato inicial | Procedencia, hora observada/ingestada, calidad, validación e idempotencia. |
| `audit.search` — consultar cambios/accesos | auditor | Pendiente | Solo lectura, acceso segregado y registro resistente a manipulación. |

## Estructura de carpetas propuesta

```text
backend/app/
  api/                         # Adaptadores HTTP/WebSocket; sin lógica de dominio
  auth/                        # OIDC, sesiones y políticas (pendiente; no exponer API aún)
  audit/                       # Eventos de auditoría (pendiente)
  cameras/
    data.py                    # Datos semilla de demo existentes
    models.py                  # Modelo de cámara pública existente
    service.py                 # Lectura/filtros actuales
    inventory_schemas.py       # Alta segura del inventario autorizado [nuevo]
    inventory_repository.py    # Persistencia cuando se incorpore DB [pendiente]
  integrations/
    contracts.py               # Sobre de datos, salud, protocolo y descriptor [nuevo]
    registry.py                # Registro explícito en memoria [nuevo]
    providers/                 # Un adaptador por proveedor, sin autodiscovery [siguiente]
      celestial/               # CelesTrak/Space-Track/N2YO
      cameras/                  # ONVIF/VMS, solo red autorizada
      aviation/                 # ADS-B, sujeto a fuente/licencia
      maritime/                 # AIS, sujeto a fuente/licencia
  persistence/                 # DB, migraciones y repositorios (pendiente)
  policy/                      # Autorizaciones por tenant/sitio/recurso (pendiente)
  satellite/                   # Propagación orbital existente
  aoi/                         # Áreas de interés existentes
  alerts/                      # Reglas/alertas existentes
  common/                      # Errores, reloj y utilidades transversales (según necesidad)

frontend/tactical-map/src/
  app/                          # Composición de vistas (refactor gradual)
  features/
    cameras/                    # Inventario/detalle/estado (siguiente fase)
    sources/                    # Catálogo de fuentes y frescura
    alerts/                     # Alertas y confirmaciones
    map/                        # Mapa y capas, migración gradual del código actual
  shared/                       # Cliente API, controles comunes, formatos

docs/
  decisions/                    # ADRs: decisiones con contexto y consecuencias
  runbooks/                     # Operación, respaldo, incidentes y restauración
  threat-model/                 # Activos, límites de confianza y amenazas
```

Las áreas `auth`, `audit`, `persistence`, `policy`, los dominios de aviación/marítimo/radar/clima/observación terrestre y sus carpetas de proveedor/frontend ya tienen scaffolds documentados. Son estructura y criterios, no funcionalidad operativa. `deploy`, `runbooks` y `threat-model` también contienen guías iniciales. No hay adaptadores activos de esas fuentes, persistencia nueva ni login.

El esquema interoperable versionado está en `contracts/event-envelope.v1.schema.json`; el roadmap de dominios, acciones y etapas está en `ROADMAP_PLATAFORMA.md`. El objetivo es ir convirtiendo cada scaffold en un vertical probado (modelo + adaptador + API autorizada + UI + health + runbook), no crear conectores de muestra que aparenten acceso real.

## Contratos añadidos ahora

### Sobre de dato

`DataEnvelope[T]` lleva `source_id`, `observed_at`, `ingested_at`, `kind` (`observed`, `calculated`, `inferred`), `quality` y una referencia opcional a autorización. El campo `payload` es genérico; cada módulo deberá añadir modelos tipados para no usar diccionarios sin validar en sus APIs.

### Salud de fuente

`ConnectorHealth` distingue `not_configured`, `healthy`, `degraded` y `unavailable`. `ConnectorRegistry` solo registra objetos explícitamente entregados por el código y rechaza IDs duplicados. No busca módulos, no carga plugins dinámicos y no inicia solicitudes de red. Una falla de salud se reporta con texto genérico al usuario.

### Alta de cámara

`CameraEnrollmentRequest` acepta nombre, sitio, ámbito de red aprobado, IP/hostname, puerto, protocolo administrativo y referencia de autorización. Rechaza URLs, credenciales embebidas y campos extra, y no tiene propiedad para contraseña. La validación de host es de formato, no una autorización para conectarse; la política/allowlist debe bloquear destinos no aprobados antes de cualquier tráfico.

## Próximas entregas

### Iteración 1 — Base del catálogo (ahora)

- Añadir contratos del conector, registro en memoria y esquema de inventario.
- Añadir pruebas de IDs duplicados, fallo aislado, IP/hostname válidos, URL rechazada y campos extra rechazados.
- No añadir endpoint público de alta ni hacer llamadas de red.

### Iteración 2 — Identidad y permisos

- Elegir proveedor OIDC, definir tenant, sitio, usuarios, roles y ciclo de revocación.
- Implementar permiso por objeto y pruebas de separación de sitios/tenants.
- Añadir auditoría para alta/edición/baja y acceso al detalle.
- Añadir migraciones y persistencia; luego exponer `POST /cameras/inventory` y `GET /cameras/inventory`.

### Iteración 3 — Conectividad de cámara autorizada

- Definir egress allowlist y agente de borde que opera dentro de la red del propietario.
- Aceptar destinos solo de inventario; validar IP/hostname contra scope antes de conectar y bloquear SSRF a localhost, metadata cloud o redes no registradas.
- Añadir conector ONVIF HTTPS con lectura de capacidades; credenciales desde vault, con permisos mínimos.
- Probar primero con cámara de laboratorio propiedad del operador y capturar solo metadatos consentidos.

### Iteración 4 — Video y operación

- Integrar VMS/relay de video, permisos temporales y registro de accesos.
- Añadir retención y exportación solo bajo política explícita; cifrado, restauración y borrado verificable.
- Pruebas de carga, red desconectada, credencial vencida, revocación y revisión externa antes de cualquier despliegue sensible.

## Validación de este incremento

Desde `backend/`, ejecutar:

```bash
python -m unittest discover -s tests -v
python -m compileall -q app tests
```

El contrato y esquema no deben modificar las rutas API actuales. La próxima fase necesita decisiones del operador sobre proveedor de identidad, base de datos y dónde correrá el agente de cámaras; hasta entonces no se activa descubrimiento ni acceso remoto.
