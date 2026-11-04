# Feature: cámaras autorizadas

Este directorio alojará la vista de inventario cuando exista API autenticada y autorización por cámara.

## Vistas previstas

- `CameraInventory`: búsqueda/filtros por sitio, estado, frescura y tipo de capacidad.
- `CameraDetail`: IP/hostname autorizado, método de origen, propietario, estado y metadatos devueltos por el proveedor.
- `CameraStatusBadge`: estados `not_configured`, `healthy`, `degraded`, `unavailable` y `stale`.

## Límites

- No introducir una función de escaneo en el navegador ni de descubrimiento de IPs.
- No persistir contraseñas, tokens, URLs RTSP ni credenciales en el estado del frontend.
- Ocultar metadatos y streams sin permiso del servidor; no depender solo de controles visuales.
- El video solo se integrará a través de un relay/VMS autorizado y permisos temporales.

La UI se implementará tras definir autenticación, permisos por sitio/cámara y contrato de API.
