# Identidad y autenticación

Estado: no implementado. No declarar este prototipo seguro para Internet hasta completar este módulo.

Destino: OIDC, MFA para roles privilegiados, ciclo de vida de sesiones/tokens, logout/revocación y cuentas de servicio por conector. La autorización de cada recurso pertenece a `policy/`, no a checks dispersos. Secretos no se emiten al frontend.

Criterios: expiración y rotación probadas, protección contra CSRF donde aplique, auditoría de cambios de rol, ninguna identidad anónima puede leer inventarios privados.