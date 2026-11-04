# Auditoría

Estado: no implementado.

Registrar actor/servicio, tenant/sitio, acción, objeto, decisión de autorización, timestamp UTC, resultado y correlation ID. Auditar cambios de configuración, acceso/exportación de video, credenciales y permisos. No almacenar secretos, contenido de video ni payload sensible en el log.

La persistencia debe ser de solo append para el servicio y con controles de integridad/retención; la consulta de auditoría será un permiso separado. Definir política legal y de conservación antes de producción.