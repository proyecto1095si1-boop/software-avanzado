# Persistencia

Estado: no implementada; las listas actuales son en memoria/semilla.

Destino: repositorios desacoplados, migraciones versionadas, PostgreSQL/PostGIS para inventario/eventos/AOI/metadatos; almacenamiento de video separado solo con autorización y política de retención. Añadir índices y particionado según cargas medidas.

Requisitos: backups cifrados, restauración probada, borrado/retención auditables, aislamiento por tenant, transacciones e idempotencia de ingestión. Antes de elegir versión, hosting o alta disponibilidad, definir volumen, RPO/RTO y entorno del operador.