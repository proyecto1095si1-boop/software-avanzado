# Proveedores espaciales

Estado: CelesTrak ya está conectado en `app/satellite/tle.py`; esta carpeta es destino para adaptadores adicionales, no un segundo camino activo.

A considerar: fuentes orbitales públicas/licenciadas y APIs de operador o ground station para telemetría a la que el usuario tenga derecho de acceso. Registrar fuente, timestamp, licencias, cuotas, precisión y fallas. Un TLE permite estimar posición orbital; no revela el contenido de enlace satelital.

No implementar interceptación de comunicaciones privadas, descifrado sin autorización, elusión de cifrado/controles ni transmisiones al satélite.