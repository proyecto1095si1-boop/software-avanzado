# APIs e integraciones — estado real y siguientes pasos

## Estado actual

| Fuente | Estado en el código | Configuración / ubicación | Siguiente paso seguro |
|---|---|---|---|
| CelesTrak/TLE | Conectada | `backend/app/satellite/tle.py`; `CELESTRAK_BASE` opcional | Mostrar procedencia y edad de TLE; probar límites y fallos. |
| Space-Track | No implementada | Hay variables de configuración; no hay adaptador proveedor | Implementar solo con cuenta autorizada, límites y políticas del proveedor. |
| N2YO | No implementada | Hay variable de configuración; no hay adaptador proveedor | Definir caso de uso y condiciones de la API antes de integrar. |
| ADS-B | No implementada | Configuración declarada; no hay adaptador proveedor | Conectar feed propio o licenciado y validar su esquema/cuota. |
| AIS | No implementada | Configuración declarada; no hay adaptador proveedor | Conectar fuente propia/licenciada y normalizar su procedencia. |
| Cámaras | Datos semilla de demostración | `backend/app/cameras/data.py` | Crear inventario de equipos propios/autorizados con identidad, permiso y alcance de red. |
| Shodan | No implementada | No hay conector funcional | No usar para encontrar o acceder a cámaras ajenas. Definir, si aplica, un caso defensivo limitado a activos propios. |

Tener una variable de entorno no significa que el proveedor esté conectado. `/system/status` solo debe reflejar la configuración que realmente compruebe el adaptador; no introducir contraseñas o tokens en respuestas de estado.

## Cámaras: integración autorizada

Las cámaras actuales son entradas locales de demostración, no un inventario administrable ni un servicio de descubrimiento de direcciones IP. Para integrar cámaras del operador, primero se requiere registrar propietario, sitio, hostname/IP conocido, protocolo, ámbito de red aprobado y referencia de autorización. El backend aún no autentica usuarios ni aplica permisos por cámara; por eso no se habilitan endpoints mutables ni consultas de red en este incremento.

La dirección de una cámara debe provenir del inventario del propietario, un VMS/CMDB/DHCP/DNS administrado o un agente instalado dentro de la red autorizada. Una futura comprobación de salud solo alcanzará dispositivos registrados y destinos incluidos en una allowlist. No se aceptan URLs arbitrarias para que el backend las solicite, ni se exploran rangos públicos. Las credenciales se obtendrán de un gestor de secretos y nunca formarán parte del frontend o del inventario en texto plano.

La planificación del inventario, el contrato de alta y sus límites están en [docs/IMPLEMENTACION_INICIAL.md](IMPLEMENTACION_INICIAL.md). El esquema actual solo valida una IP/hostname y metadatos de autorización; no establece conexión con el dispositivo.

## Próximos adaptadores

Cada proveedor debe implementar los contratos de `backend/app/integrations/contracts.py` y registrarse explícitamente en `backend/app/integrations/registry.py`. Al introducir una fuente nueva, añadir pruebas de formato, autenticación, cuota, timeout, reintentos acotados, datos obsoletos y red caída. Normalizar procedencia, hora observada, hora de ingestión, licencia/autorización y calidad.

La configuración de secretos se mantiene fuera del repositorio: copiar `backend/.env.example` a `backend/.env` solo para desarrollo local y no subir el archivo `.env`. Las integraciones no deben activarse hasta que existan propietario, permiso, alcance, controles de egress y revisión de datos.
