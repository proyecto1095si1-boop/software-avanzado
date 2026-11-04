# Hoja de ruta integral — Software Avanzado

## Objetivo del producto

Convertir el repositorio en una plataforma de conciencia situacional que integre fuentes geoespaciales y sensores autorizados en un cuadro operativo común. El objetivo inmediato debe ser una plataforma **segura, verificable y resiliente para uso institucional autorizado**. “Grado militar” no es una propiedad que pueda garantizarse solo con software: cualquier uso en defensa, infraestructura crítica o entornos regulados requiere requisitos del operador, evaluación de amenazas, pruebas independientes, acreditación aplicable y controles de operación.

El alcance propuesto es monitoreo, visualización, alertas y análisis con supervisión humana. Esta hoja de ruta no contempla selección de objetivos, guía de armas, control autónomo de dispositivos ni intrusión en sensores ajenos.

## Qué significa “conectar todo”

El sistema debe integrar cada fuente mediante adaptadores independientes, con contratos comunes y permisos explícitos. Una integración opcional no debe mostrarse como conectada solo porque haya una variable de entorno: debe comprobarse, informar su frescura y estado, y fallar sin derribar las demás fuentes.

Cada registro debe distinguir entre dato observado, dato calculado y dato inferido. Debe incluir fuente, hora del dato, hora de ingestión, calidad, licencia o permiso de uso y nivel de confianza. Un mapa no debe presentar una posición antigua como si fuera actual.

## Cámaras IP: alcance real y seguro

Sí se puede mostrar la IP y los datos técnicos de una cámara cuando el operador aporta la cámara a un inventario autorizado o conecta una red bajo su administración. La IP no se “descubre” mágicamente desde Internet: puede venir del inventario del propietario, de una API del VMS/NVR, de DHCP/DNS/CMDB o de un agente instalado en una red explícitamente autorizada. Si hay NAT, proxy o una VPN, la plataforma puede conocer la dirección del punto de conexión y, si la fuente la proporciona, la dirección privada; no siempre son la misma.

El flujo recomendado es:

1. Un administrador registra un equipo con identificador, propietario, sitio, zona de red, IP o hostname conocido, protocolo, propósito y autorización. No se acepta una URL arbitraria para que el backend la consulte.
2. Un agente situado en la red autorizada valida el alcance contra una lista de rangos aprobados y prueba solo los equipos registrados. No explora rangos públicos ni redes no declaradas. La interfaz muestra IP, puerto, última conexión y método por el que se obtuvo la información.
3. Para equipos compatibles, un conector ONVIF obtiene los perfiles y capacidades soportados. ONVIF Profile T contempla streaming H.264/H.265, ajustes de imagen, eventos de movimiento/manipulación y streaming de metadatos; las capacidades exactas dependen del perfil y del equipo [3].
4. Si el equipo o VMS ofrece una API oficial, se consulta esa API con una cuenta de mínimo privilegio. El inventario puede incluir fabricante, modelo, número de serie cuando el rol lo permita, firmware, capacidades, resolución, codec, perfiles de transmisión, estado y eventos.
5. Los secretos se guardan en un gestor de secretos, nunca en el navegador, el repositorio, la URL, los logs ni la tabla de inventario. El cliente web ve una referencia de credencial y permisos, no la contraseña.
6. El video se entrega a través de un relay/VMS autorizado. El navegador no debe recibir credenciales RTSP ni conectarse directamente a la red privada de la cámara. El acceso al vivo, PTZ, audio, snapshots y exportación se controla por rol y se audita por cámara.
7. Grabación, reconocimiento de personas, análisis de audio y retención requieren una justificación, permiso, política de conservación y revisión legal propios. Se desactivan por defecto.

“Datos completos” no es una garantía técnica: el fabricante puede no exponer número de serie, firmware, analítica o URL de stream al rol configurado. El sistema debe mostrar `no disponible`, `no autorizado` o `no soportado` y no intentar eludirlo. No debe probar contraseñas por defecto, explotar firmware, saltar autenticación ni localizar cámaras de terceros.

## Diagnóstico del repositorio actual

El proyecto ya tiene un punto de partida útil: FastAPI, React/MapLibre, posiciones TLE de CelesTrak, propagación SGP4, AOI, alertas, pases y un WebSocket. En la revisión y los cambios locales recientes se añadieron pruebas iniciales, límites de consulta, validación de bbox, CORS configurable, bind local de Docker, lockfile y correcciones del TTL.

Las cámaras actuales son principalmente una lista semilla local. `CAMERA_LIST_URL`, ADS-B, AIS, Space-Track, N2YO y Shodan aparecen en configuración/documentación, pero no equivalen a conectores funcionales. No hay en el estado revisado autenticación de usuarios, autorización por cámara, almacén de secretos, inventario administrable, conector ONVIF, relay de video, auditoría por usuario, persistencia operativa, CI ni despliegue de alta disponibilidad. Por eso el sistema no debe exponerse a Internet ni presentarse hoy como apto para operación crítica.

La guía NIST CSF 2.0 ofrece un marco de resultados para identificar, priorizar y comunicar riesgo; no prescribe por sí misma una configuración técnica [1]. Para sensores conectados a instalaciones y redes operativas, NIST SP 800-82 Rev. 3 enfatiza las necesidades particulares de disponibilidad, confiabilidad y seguridad de OT [2]. OWASP API Security Top 10 destaca, entre otros riesgos, autorización por objeto, autenticación, consumo no limitado de recursos, SSRF y consumo inseguro de APIs; todos aplican a un backend que consulta cámaras y feeds externos [4].

## Arquitectura objetivo

### Capa de presentación

Panel web adaptable con mapa, catálogo de fuentes, estado de conectividad, frescura de datos, filtros por permiso y vistas de detalle. El navegador habla solo con la API propia; no contiene credenciales de cámaras, tokens privados ni acceso directo a redes de sensores.

### Identidad y control de acceso

Proveedor OIDC compatible con MFA para cuentas administrativas. RBAC por organización, sitio y función; autorización por objeto para cada cámara/AOI/feed; cuentas de servicio separadas por conector. Roles propuestos: lector, operador, administrador de sitio, administrador de integración y auditor. Cambios de permisos requieren bitácora. El acceso a un identificador no implica autorización sobre el objeto correspondiente, riesgo expresamente señalado por OWASP [4].

### API y servicios de dominio

Separar módulos de satélites, cámaras, AOI, alertas, pases, catálogo de fuentes, auditoría y administración. La API valida cada campo, aplica límites de tamaño/tiempo/tasa y devuelve errores tipados sin detalles internos. Los conectores se ejecutan en procesos aislados con egress permitido solo a destinos necesarios.

### Adaptadores e ingestión

Contrato uniforme de conector con `configure`, `health`, `fetch`, `normalize` y `shutdown`. Cada mensaje normalizado conserva `source_id`, `observed_at`, `ingested_at`, `quality`, `license`, `authorization_scope` y `raw_reference`. Reintentos con backoff, circuit breaker, límites de concurrencia e idempotencia. Los datos de terceros se validan como no confiables antes de guardarlos o procesarlos.

### Persistencia

PostgreSQL/PostGIS para usuarios, cámaras autorizadas, AOI, metadatos, eventos y auditoría consultable. Almacenamiento cifrado separado para video solo si existe autorización de grabación. Redis o una cola ligera solo cuando la carga lo justifique. Backups cifrados, restauración probada, migraciones versionadas y política explícita de retención.

### Red y despliegue

Separar frontend, API, conectores y redes de cámaras. El servidor web no se conecta directamente a VLAN de sensores; el agente de borde hace la conexión saliente controlada hacia el servicio central. TLS en tránsito, cifrado de secretos, segmentación, listas de salida, imágenes firmadas, SBOM, escaneo de dependencias y despliegue reproducible. Las medidas OT deben adaptarse al riesgo y no interrumpir sistemas físicos [2].

### Observabilidad y auditoría

Métricas de disponibilidad, latencia, tasa de error, antigüedad de datos, conexiones activas, uso de CPU y colas. Logs estructurados sin secretos ni URLs con credenciales. Auditoría resistente a manipulación para alta/baja de cámara, acceso a video, reproducción, exportación, cambio de permisos y cambios de configuración. Alertas ante conector silencioso, credencial vencida, datos obsoletos o acceso anómalo.

## Fases de entrega

Las duraciones son rangos iniciales para planificación, no compromisos; se ajustan tras definir tamaño de equipo, usuarios y entorno de despliegue.

### Fase 0 — Alcance, permisos y modelo de amenazas (1–2 semanas)

**Entregables:** inventario de operadores y fuentes; declaración de uso permitido; clasificación de datos; jurisdicciones; modelo de amenazas; matriz de roles; política de conservación; plan de respuesta a incidentes; criterios de disponibilidad y recuperación.

**Puerta de salida:** cada fuente tiene propietario, autorización, términos/licencia, alcance técnico y persona responsable. Ninguna fuente de cámara entra al sistema sin este registro.

### Fase 1 — Base de ingeniería y confiabilidad (2–4 semanas)

**Trabajo:** estructura por módulos, configuración tipada, versiones de API, logging sin secretos, health/readiness, migraciones, CI, pruebas unitarias y de API, lint/format, análisis de dependencias, Docker reproducible, usuario no-root y `.gitignore`.

**Criterios:** build reproducible desde lockfile; pruebas en cada PR; cero secretos en el árbol actual; cobertura de rutas críticas; health check distingue que el proceso vive de que sus dependencias están sanas.

### Fase 2 — Identidad, autorización y datos (3–6 semanas)

**Trabajo:** OIDC/MFA para administradores, sesiones seguras, RBAC/ABAC, permisos por sitio y por cámara, auditoría, cifrado/gestión de claves, retención y borrado. Añadir autenticación no es suficiente: cada operación debe comprobar acceso al recurso consultado [4].

**Criterios:** un usuario sin permiso no puede enumerar ni consultar una cámara cambiando su ID; un rol de solo lectura no puede alterar configuración, acceder a funciones administrativas ni exportar datos fuera de su permiso; los eventos sensibles quedan auditados.

### Fase 3 — Catálogo de fuentes y conectores (3–5 semanas)

**Trabajo:** modelo común de fuentes; contratos de adaptador; estado, cuota y frescura; normalización; tolerancia a fallos; egress allowlist; registro de licencia y procedencia. Estabilizar el conector CelesTrak existente y definir prioridades de Space-Track/N2YO/ADS-B/AIS según caso de uso y permisos.

**Criterios:** apagar una fuente no detiene las demás; cada dato muestra origen y hora; los fallos son visibles; se prueban respuestas inválidas, rate limit, timeout y desconexión; no hay reintentos ilimitados.

### Fase 4 — Inventario de cámaras propias o autorizadas (3–6 semanas)

**Trabajo:** esquema de cámaras; importación administrada desde CSV/API de VMS; IP/hostname; sede y VLAN; descubrimiento limitado a inventario y rangos aprobados desde agente de borde; conector ONVIF y API de fabricante; capacidades, eventos y estado; almacenamiento de credenciales en vault.

**Criterios:** la API rechaza destinos fuera del allowlist; el agente no escanea Internet ni subredes no declaradas; cada lectura registra el actor, el dispositivo y el permiso; no se guardan claves en logs; datos no soportados se indican sin intentar evadir permisos. Profile T se implementa por capacidades negociadas, no suponiendo que todos los equipos ofrecen lo mismo [3].

### Fase 5 — Visualización segura de video (3–6 semanas)

**Trabajo:** relay interno o integración con VMS; transporte compatible con navegador; permisos por stream; límites de espectadores y bitrate; expiración de URLs; marca de agua opcional; modo privacy/shutter si está soportado; política de snapshots y grabación separada.

**Criterios:** ningún secreto RTSP aparece en el frontend o URL visible; el stream se corta al revocar permiso; sin permiso no hay snapshot ni exportación; pruebas verifican fuga de credenciales y acceso cruzado entre sitios.

### Fase 6 — Contexto geoespacial y analítica explicable (4–8 semanas)

**Trabajo:** PostGIS; mejoras de AOI; frescura y calidad orbital; predicciones explicables; alertas deduplicadas; reglas configurables; correlación entre eventos con procedencia; vistas para pérdida de señal y degradación de fuentes.

**Criterios:** una alerta explica fuente, tiempo, regla y confianza; las predicciones se etiquetan como cálculos, no observaciones; usuario puede distinguir datos nuevos, atrasados e inválidos.

### Fase 7 — Operación resiliente y preparación de despliegue (4–8 semanas)

**Trabajo:** staging y producción separados; backup/restore; pruebas de recuperación; observabilidad; rate limit; gestión de incidentes; control de cambios; rollbacks; pruebas de carga y desconexión; revisión independiente de seguridad y privacidad.

**Criterios:** se demuestra restauración dentro de objetivos RPO/RTO acordados; se documentan dependencias y responsable de cada servicio; hay procedimiento de rotación/revocación de credenciales; hallazgos críticos se corrigen antes de producción. No se declara certificación ni “grado militar” sin auditoría/acreditación correspondiente.

## Modelo de datos mínimo para cámaras

`Camera`: `id`, `owner_org_id`, `site_id`, `name`, `vendor`, `model`, `serial_number` cuando esté autorizado, `ip_address`/`hostname`, `ip_source`, `network_zone`, `protocol`, `onvif_profiles`, `firmware_version`, `capabilities`, `stream_profile_ids`, `status`, `last_seen_at`, `last_metadata_at`, `authorization_reference`, `retention_policy_id`, `created_by`, `updated_at`.

Las credenciales no pertenecen a ese objeto como texto plano. Debe guardar `secret_ref` a un vault, con rotación y permisos restringidos. Los streams y URLs de gestión deben permanecer dentro de un catálogo autorizado; aceptar un `stream_url` libre de usuarios sin validación crea riesgo SSRF, señalado por OWASP [4].

## Orden de trabajo recomendado ahora

1. Crear rama local de trabajo y preservar el estado actual; revisar el token de CARTO histórico y revocarlo/restringirlo si es real.
2. Añadir autenticación y autorización antes de desplegar cualquier dato sensible.
3. Añadir CI y pruebas de permisos, API y seguridad.
4. Implementar catálogo de cámaras propiedad del operador, con agente de borde y allowlist explícita.
5. Añadir ONVIF Profile T y API de VMS, primero con cámaras de laboratorio y cuentas de solo lectura.
6. Implementar relay de video seguro, luego persistencia y alta disponibilidad.
7. Conectar fuentes geoespaciales adicionales una por una, con licencias, estado de frescura y pruebas de falla.

## Fuera de alcance y salvaguardas

No se añadirá descubrimiento global de cámaras expuestas, acceso a IPs de terceros, prueba de credenciales, bypass de autenticación, explotación de firmware, extracción encubierta de video, identificación de personas ni funciones de armamento. Para una evaluación de seguridad de cámaras, el operador debe aportar autorización escrita, alcance/IPs, ventana de prueba y reglas de manejo de evidencia; la evaluación debe ser separada del producto de monitoreo.

## Referencias

[1]: https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20 "NIST Cybersecurity Framework 2.0"
[2]: https://csrc.nist.gov/pubs/sp/800/82/r3/final "NIST SP 800-82 Rev. 3 OT Security"
[3]: https://www.onvif.org/profiles/profile-t/ "ONVIF Profile T"
[4]: https://owasp.org/API-Security/editions/2023/en/0x11-t10/ "OWASP API Security Top 10 2023"
