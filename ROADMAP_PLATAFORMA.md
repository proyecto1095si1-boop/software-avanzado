# Roadmap de plataforma — Software Avanzado

## 1. Visión y límites

La meta es una plataforma geoespacial multimodal: un mapa común donde operadores autorizados consulten cámaras propias, vuelos disponibles, posiciones orbitales, productos de radar, clima, tráfico marítimo, imágenes y otras fuentes. Cada capa debe conservar fuente, hora, calidad, cobertura, licencia/permiso y límites del dato.

“Grado militar” o “extraterrestre” puede expresar ambición de alcance, resiliencia e integración; no es una certificación. No se debe publicitar como sistema certificado, listo para defensa u operación crítica sin requisitos del cliente, threat modeling, pruebas independientes, acreditación y autorización pertinentes. La primera meta verificable es **plataforma de observación y apoyo humano**, resiliente y segura; no control de armas, targeting autónomo ni intrusión.

No existe una conexión universal a todos los sensores. Cámaras, aviación, satélites y radares tienen protocolos, licencias, cobertura, latencia y permisos diferentes. Un adaptador solo se declara conectado después de una prueba real autorizada, un health check y una indicación de frescura.

## 2. Análisis del estado actual en GitHub

En la rama principal hay un panel React/MapLibre, backend FastAPI, datos TLE de CelesTrak, propagación orbital básica, AOI, alertas, pases, tracks y WebSocket. Las cámaras que aparecen en el mapa son inventario de demostración, no acceso a equipos IP del usuario.

Se añadieron contratos de salud/procedencia de conectores, un registro local explícito, esquema de alta de cámara autorizada, pruebas y estructura documental. Esos elementos no equivalen a persistencia, login, ONVIF, vídeo, ADS-B, AIS, radar, clima ni descarga de imágenes. No hay sistema de identidad, política por objeto, base de datos, auditoría de usuarios, cola, agente de borde ni despliegue productivo.

El siguiente desarrollo no debe abrir rutas administrativas o de red hasta instalar controles de identidad, autorización, egress y auditoría. La estructura nueva indica destinos de módulos; no significa que su función esté implementada.

## 3. Catálogo de dominios y alcance

| Dominio | Producto visible | Fuentes posibles | Estado real / límite |
|---|---|---|---|
| Cámaras | Inventario, estado, metadatos y más adelante video | VMS/ONVIF de cámaras propias, CMDB o agente del sitio | Semillas de demo y esquema. Sin login, CRUD, conexión, stream ni inventario operativo. |
| Aviación | Tracks disponibles, fuente, altura/velocidad reportada, edad y cobertura | Feed ADS-B propio/público o proveedor contratado; productos de tránsito autorizados | No hay conector activo. ADS-B no es radar primario, plan de vuelo ni vista total del espacio aéreo. |
| Satélites — órbita | Posiciones propagadas, trazas, pases y calidad temporal | TLE/efemérides públicas, comerciales o autorizadas | CelesTrak/TLE ya conectado. Posición propagada es cálculo, no medición instantánea. |
| Satélites — telemetría/contenido | Solo datos que el operador tiene derecho a recibir | API del dueño de satélite/ground station, downlink abierto y permitido, archivos o streams contratados | No implementado. Un TLE no entrega comunicaciones. Recibir telemetría requiere hardware/servicio compatible, licencias, operación de estación terrestre y permiso. No se intercepta ni descifra un enlace privado o protegido. |
| SatCom/telemetría | Telemetría y productos de misión desde una fuente autorizada | API de misión/ground station propia o contratada; datos abiertos/licenciados | Se separó como carpeta scaffold (`backend/app/satcom/`); sin receptor, API ni decodificador. |
| Radar | Productos meteorológicos, mosaicos o tracks autorizados | API/feed público o licenciado, radar propio integrado por su operador | No conectado ni controla hardware. Radar meteorológico, radar ATC primario y track de proveedor son productos diferentes. |
| Meteorología | Observaciones, pronósticos y capas radar | Servicios públicos/oficiales o contratados | No conectado. Pronóstico y observación deben aparecer diferenciados. |
| Marítimo | Tracks AIS con fuente y antigüedad | Receptor propio y proveedor AIS con licencia | No conectado. AIS es cooperativo y su ausencia no prueba ausencia física. |
| Observación terrestre | Catálogo de escenas, huellas y derivados | Catálogos públicos o comerciales | No conectado. La cobertura, resolución, latencia y licencia dependen del sensor/proveedor. |
| AOI y alertas | Geometrías y reglas explicables | Datos existentes del backend | Parcialmente funcional; ampliar persistencia, permisos, deduplicación y procedencia. |
| Catálogo de fuentes | Estado, último éxito, frescura, licencia y cuota | Todos los conectores | Contratos iniciales y registro in-memory; no hay catálogo persistente ni health checks externos activos. |
| Identidad/auditoría | Usuarios, roles, permisos y rastro de acceso | OIDC/MFA y repositorio/audit store | No implementado; prerrequisito de datos sensibles. |

## 4. Acciones de producto por actor

### Lector

Consultar mapa, capas y metadatos permitidos; filtrar por tiempo, área, fuente y calidad; identificar observación/calculado/inferido; abrir el detalle solo si tiene permiso; ver cuándo un feed no está disponible o está obsoleto.

### Operador

Crear/confirmar alertas, anotar eventos, comparar fuentes autorizadas, solicitar acceso a un stream con permiso temporal, exportar solo los campos y periodos autorizados. Toda acción sensible se audita.

### Administrador de sitio

Gestionar cámaras y ámbitos de red de su sitio, aprobar inventario, asignar credenciales mediante vault, habilitar/deshabilitar conectores de su área y revocar accesos. No puede consultar otros sitios por cambiar un ID.

### Integrador

Configurar adaptadores y fuentes con owner, finalidad, alcance, licencia, cuota, egress y responsable documentados. No recibe automáticamente acceso al video ni privilegios de operador.

### Auditor

Leer trazas de acceso/cambio y evidencia de cumplimiento, sin permisos para cambiar cámaras, credenciales ni datos.

## 5. Diseño de sistema completo

```text
Frontend por features
        │ HTTPS/OIDC; permisos se validan de nuevo en servidor
        ▼
API FastAPI ── policy por tenant/sitio/recurso ── auditoría
        │
        ├── dominios: satellite, aviation, cameras, radar, weather, maritime, EO
        ├── catálogo de fuentes y sobre común con procedencia/frescura
        ├── servicios de alerta, AOI, búsqueda geoespacial y timeline
        ├── PostgreSQL/PostGIS + migraciones; event store/queue solo según volumen
        └── conectores aislados / procesos de ingestión
                ├── APIs públicas o contratadas con egress limitado
                └── agente de borde del propietario → VMS/sensores registrados

Video autorizado → relay/VMS con URL temporal → navegador
```

El sobre común contiene `event_id`, `source_id`, dominio, clase de dato, `observed_at`, `ingested_at`, posición/unidades si aplica, calidad, licencia/alcance y `payload` tipado. El usuario debe poder reconstruir de qué feed y hora salió cada capa. Un dato retrasado nunca se pinta como real-time sin señal de antigüedad.

Persistencia inicial sugerida: PostgreSQL/PostGIS para catálogo, AOI, cámara, permisos, eventos y metadatos. No guardar el video junto al inventario por defecto; para grabación se necesita almacén separado, cifrado, retención, autorización y borrado comprobable. Añadir colas solo cuando métricas muestren beneficio; comenzar con tareas acotadas y sin reintentos infinitos.

## 6. Estructura de carpetas en el repositorio

### Backend

```text
backend/app/
  api/                         rutas HTTP/WebSocket finas ya existentes
  auth/                        OIDC, sesiones y MFA [scaffold]
  policy/                      permisos tenant/sitio/recurso [scaffold]
  audit/                       eventos de cambios/consultas [scaffold]
  persistence/                 repositorios y migraciones [scaffold]
  integrations/
    contracts.py               contrato inicial existente
    registry.py                registro explícito in-memory existente
    providers/
      cameras/                 VMS/ONVIF autorizado [scaffold]
      aviation/                ADS-B permitido [scaffold]
      space/                   APIs orbitales/telemetría autorizada [scaffold]
      satcom/                  servicios de misión/ground station autorizados [scaffold]
      radar/                   productos radar autorizados [scaffold]
      weather/                 observación/pronóstico [scaffold]
      maritime/                AIS permitido [scaffold]
      earth_observation/       catálogos EO autorizados [scaffold]
  cameras/                     datos demo y esquema de inventario
  satellite/                   propagación TLE actual
  satcom/                      telemetría autorizada, separada de órbita [scaffold]
  aviation/ maritime/ radar/ weather/ earth_observation/ [scaffold]
  aoi/ alerts/                 dominios existentes
```

### Frontend

```text
frontend/tactical-map/src/
  app/                         shell/rutas [scaffold]
  shared/                      cliente API y componentes seguros [scaffold]
  features/
    cameras/ aviation/ satellite/ radar/ maritime/
    earth-observation/ alerts/ sources/ [scaffolds por dominio]
  components/                  componentes de mapa existentes
```

### Contratos, operación y documentación

```text
contracts/                     sobre de eventos versionado
  event-envelope.v1.schema.json
  README.md
deploy/                         perfiles futuro local / edge / cloud, sin puertos abiertos
  README.md
docs/
  decisions/                    ADRs
  runbooks/                     rollback, incidentes, backup, operación de fuentes
  threat-model/                 activos, límites de confianza y amenazas
  ROADMAP_INTEGRAL.md           visión y salvaguardas
  ROADMAP_PLATAFORMA.md         roadmap expandido por dominios y fases
```

Las carpetas marcadas scaffold tienen documentación/contratos, no código de proveedor o autorización. Cada nueva carpeta funcional debe iniciar con contrato, pruebas y un primer comportamiento acotado; no llenar el repositorio de carpetas vacías.

## 7. Fases, dependencias y puertas de salida

### Fase 0 — Base y alcance

Inventariar usuarios, dueño de datos, fuentes, licencias, jurisdicción, necesidades de latencia, disponibilidad, RPO/RTO, hardware existente y modo de despliegue. Crear threat model, ADRs, CI, matriz de riesgo y estado explícito por feature.

**Salida:** producto y fuentes tienen owner/permiso/caso de uso; pipeline ejecuta tests/build y dependencias escaneadas; secretos no están en el repo.

### Fase 1 — Identidad, autorización y auditoría

OIDC/MFA, tenant/sitio, roles, policy por objeto, ciclo de revocación, cuenta de servicio por adaptador, repositorio/audit log y pruebas contra IDOR/BOLA/SSRF. No construir APIs de inventario o streams antes de esta fase.

**Salida:** pruebas demuestran separación de sitios/tenants, logs redactados, revocación de permiso efectiva y privilegio mínimo.

### Fase 2 — Plataforma de ingestión

Persistencia PostGIS, migraciones, catálogo persistente de fuentes, envelope v1, límites de payload, deduplicación/idempotencia, frescura, circuit breaker, métricas, contrato de API y UI de estado.

**Salida:** una fuente cae sin derribar otras; cada evento es rastreable y los datos viejos se reconocen.

### Fase 3 — Cámaras autorizadas

Inventario persistente/importación VMS, owner/sitio/scope, agente edge, allowlist de destinos, pruebas de laboratorio con cámara propia, ONVIF HTTPS o API del VMS y credencial vault. Primero lectura de estado/capacidades; video solo después con relay y permiso temporal.

**Salida:** no hay conexión a host no inventariado; no hay secreto frontend/log/URL; la cuenta no puede cambiar configuración física; auditoría completa.

### Fase 4 — Aviación

Elegir un feed permitido y un caso de uso. Añadir adaptador ADS-B/provider, cobertura, timestamps, altitude reference, filtros por área y licencia/retención. Distinguir feeds cooperativos, producto de radar, plan de vuelo y feeds comerciales.

**Salida:** estado, cuota, esquema y retraso visibles; tests de rate-limit, desconexión, invalid fields, datos duplicados e históricos.

### Fase 5 — Satélites y SatCom

Mejorar TLE/efemérides con procedencia, antigüedad, incertidumbre y comparación de fuentes autorizadas. Telemetría de misión solo mediante API autorizada del propietario/ground station o contenido abierto/legalmente distribuido; documentar equipo, frecuencia/servicio, licencia y decoder del proveedor sin romper cifrado.

**Salida:** UI diferencia cálculo orbital de telemetría observada; el contenido se acepta solo por canal autorizado; no se promete descifrado ni comunicación bidireccional al satélite.

La implementación satcom permanece separada en `backend/app/satcom/` y `frontend/tactical-map/src/features/satellite/telemetry/`; órbita calculada permanece en el módulo satelital existente.

### Fase 6 — Radar y meteorología

Comenzar por capas meteorológicas públicas/licenciadas y visualización con leyenda, unidades, georreferencia, scan time, cobertura y atribución. Después, integrar tracks radar ya procesados que un operador proporcione. Hardware activo es proyecto separado con requisitos safety/OT y autorización.

**Salida:** capas georreferenciadas/reproducibles, timestamp válido y ningún control del radar desde la plataforma base.

### Fase 7 — Marítimo e imágenes terrestres

AIS con feed permitido, disclaimers de cobertura y deduplicación; catálogos de imágenes con metadatos/atribución, huella, hora, resolución y cuotas. Descarga/procesado bajo retención y licencias.

**Salida:** cada capa demuestra proveniencia, ventana de validez, permisos/licencia y límites de cobertura.

### Fase 8 — Correlación geoespacial y alertas

Timeline común, AOI persistente, reglas expresables, correlación de eventos por tiempo/espacio, calidad/uncertainty y explicación de cada alerta. Revisión humana obligatoria para impactos externos; no automatizar decisiones de alto impacto.

**Salida:** replay reproducible, provenance completa, tasa de falsos positivos medida y regla auditable.

### Fase 9 — Resiliencia y operación

Alta disponibilidad según perfil, separación edge/cloud, backup y restore, monitoring, runbooks, respuesta a incidentes, gestión de parches, SBOM, pruebas de carga/chaos seguras, auditoría independiente y acreditación si se reclama.

**Salida:** RPO/RTO demostrados, recuperación ensayada y aceptación formal del operador. La etiqueta “grado militar” no se usa como afirmación de certificación sin evidencia.

## 8. Clasificación de cada función

El catálogo de fuentes/product features deberá usar al menos: `planned`, `scaffold`, `configured`, `connected`, `degraded`, `stale`, `disabled`. `connected` requiere health check exitoso reciente, no solo credenciales presentes. `scaffold` no aparece como función operativa en el panel.

## 9. Riesgos que deben cerrarse antes de producción

- APIs sin identidad/autorización, datos cruzados por ID, secretos, SSRF y abuso de recursos.
- Feed de mala calidad o atrasado presentado como vivo; coordenadas o unidades incompatibles.
- Licencias/retención inadecuadas; cámaras o vuelos personales expuestos a usuarios incorrectos.
- Falla o cambio de esquema de proveedor; dependencia de tercero y saturación.
- Conexión desde nube a redes de cámaras; no debe haber egress arbitrario.
- Afirmar acceso a payload satelital sin tener ground station, frecuencia/servicio, derechos, decoder y permiso.
- Dependencia operacional sin backups, restauración, runbook, monitoreo ni responsable.

## 10. Próximas tres entregas sugeridas

1. Cerrar CI y contrato de eventos; mantener las capas actuales con estado real y pruebas.
2. Implementar identidad/políticas/auditoría antes de inventario sensible.
3. Seleccionar una fuente concreta de aviación o una cámara de laboratorio autorizada, definir quién proporciona acceso/hardware y entregar un adaptador vertical completo con su UI, health, pruebas y límites.

## 11. Referencias y documentos del repositorio

- [Hoja integral y alcance seguro](ROADMAP_INTEGRAL.md)
- [Plan inicial de acciones e implementación](docs/IMPLEMENTACION_INICIAL.md)
- [Inventario actual de APIs](docs/apis.md)
- [Arquitectura](docs/arquitectura.md)
- [Contrato de eventos v1](contracts/event-envelope.v1.schema.json)
- [NIST CSF 2.0](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20)
- [NIST OT Security SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final)
- [ONVIF Profile T](https://www.onvif.org/profiles/profile-t/)
- [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
