# Política de autorización

Estado: no implementado.

Implementar decisiones por principal, tenant, sitio, dominio, objeto, acción y contexto. Roles iniciales sugeridos: lector, operador, administrador de sitio, integrador y auditor; los roles deben mapearse a permisos explícitos. Comprobar permisos en cada lectura y escritura, no solo ocultar controles en la UI.

Pruebas obligatorias: acceso cruzado cambiando IDs, tenant/sitio equivocado, acciones admin por lector, revocación inmediata y stream expirado/revocado. Denegar por defecto y registrar decisiones sin volcar datos sensibles.