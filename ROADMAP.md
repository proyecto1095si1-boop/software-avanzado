# Análisis y hoja de ruta — Software Avanzado

## Estado observado

El repositorio implementa un panel ISR/SDA con backend FastAPI y una interfaz React/MapLibre. El backend obtiene TLE de CelesTrak, propaga posiciones, calcula trazas y pases sobre AOI, y expone alertas y datos de cámaras. La interfaz recibe posiciones por WebSocket y consulta alertas, pases, cámaras y AOI.

En la revisión inicial no se encontraron pruebas automatizadas. La documentación enumera integraciones opcionales (Space-Track, N2YO, ADS-B, AIS y un inventario remoto de cámaras) que aparecen como configuración futura, no como conectores ya implementados.

## Mejora incluida en este cambio

La variable `TLE_CACHE_TTL` estaba disponible en la configuración, pero la caché utilizaba siempre un valor fijo de dos horas. Se cambió la expiración y el contador de tiempo restante para que ambos respeten el TTL configurado. Los valores negativos se tratan como cero, evitando que un TTL inválido mantenga datos en caché.

Se restringió CORS a una lista configurable (localhost por defecto), se limitaron los puertos Docker a loopback y se pusieron límites a peticiones masivas de alertas y posiciones. El filtro geográfico de cámaras valida coordenadas, admite cajas que cruzan el antimeridiano y devuelve HTTP 422 para entradas inválidas. Las rutas de TLE, posiciones, alertas y pases ya no devuelven mensajes internos de excepción al cliente; el detalle se conserva en los logs.

La suite estándar `unittest` cubre caché, filtros de cámaras y rutas HTTP. No se agregaron dependencias de prueba al proyecto.

También se actualizaron Vite, el plugin de React y MapLibre a versiones corregidas, se generó un lockfile y se cambió Docker a `npm ci` con Node 22. `npm audit` quedó en cero vulnerabilidades. El mapa ajusta su importación a MapLibre 6 y el panel tiene un layout para móviles; el frontend inicia reintento cuando el WebSocket reporta un error.

Se quitó la clave CARTO del código actual y del ejemplo de entorno; sin clave, el mapa usa el basemap oscuro de Esri. Como la clave estuvo incluida en commits previos del repositorio público, eliminarla en el estado actual no la borra de la historia: si es una clave real, hay que revocarla o restringirla desde CARTO.

La validación ejecutada completó 13 pruebas del backend y compilación de producción del frontend. El build todavía advierte que el paquete JS inicial supera 500 kB, así que conviene aplicar code splitting antes de añadir más funciones visuales.

## Hoja de ruta sugerida

### 1. Confiabilidad y pruebas

Ampliar pruebas para parseo TLE, propagación y cruces de polígonos. Agregar CI que ejecute las pruebas y la compilación TypeScript en cada pull request. Definir respuestas de error tipadas para validación y conectividad.

### 2. Seguridad y operación

Proteger rutas de limpieza de caché si el servicio queda accesible fuera de localhost. Añadir límites de tasa, límites de conexiones WebSocket, validación estricta de grupos TLE y registros estructurados con secretos redactados. Configurar TLS y gestión de secretos para despliegues públicos.

### 3. Integridad temporal y rendimiento orbital

Incluir edad y procedencia de los TLE en las respuestas para distinguir datos frescos de antiguos. Evitar que cada usuario replique innecesariamente las mismas propagaciones: introducir caché de posiciones con actualización controlada. Medir el costo de los cálculos de pases y ejecutar tareas CPU-intensivas fuera del loop asíncrono.

### 4. Calidad del panel

Mostrar estado de carga y errores de cámaras/AOI/alertas/pases en lugar de depender solo de `console.error`. Dividir el paquete inicial (hoy supera 500 kB minificado), añadir controles de tiempo y AOI, y mostrar claramente cuándo el WebSocket está usando datos desactualizados.

### 5. Integraciones, con alcance definido

Priorizar una fuente concreta y documentada (por ejemplo, Space-Track como alternativa para TLE) antes de conectar varias fuentes simultáneamente. Implementar credenciales por variables de entorno, límites y manejo de fallos; mantener inactivas las integraciones que no estén configuradas. Para cámaras remotas, validar esquema y origen de datos y no buscar ni acceder a cámaras no autorizadas.

## Orden sugerido

Primero cerrar pruebas y CI, después endurecer seguridad y errores de operación, y luego mejorar la frescura/rendimiento de posiciones. Las integraciones nuevas deberían priorizarse según una fuente de datos y un uso autorizados, no solo por la lista de variables declaradas.

## Alcance de los cambios

Los archivos están modificados únicamente en el clon local de revisión. No se creó una rama remota, no se abrió un pull request y no se publicaron cambios en GitHub.
