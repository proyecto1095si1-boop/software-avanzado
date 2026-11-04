# Proveedores espaciales

**Activo:** `CelesTrakConnector` (`celestrak.py`)

- Implementa el protocolo `Connector` (health check real contra CelesTrak).
- Se registra al arranque vía `app.bootstrap.register_connectors`.
- La descarga de TLE para el mapa sigue en `app.satellite.tle` (mismo origen, sin duplicar lógica de negocio).

**Scaffolds / no activos:** Space-Track, N2YO, telemetría de misión / ground station autorizada.

A considerar más adelante: fuentes orbitales públicas o licenciadas y APIs de operador o ground station para telemetría a la que el usuario tenga derecho de acceso. Registrar fuente, timestamp, licencias, cuotas, precisión y fallas. Un TLE permite estimar posición orbital; no revela el contenido de enlace satelital.

No implementar interceptación de comunicaciones privadas, descifrado sin autorización, elusión de cifrado/controles ni transmisiones al satélite.
