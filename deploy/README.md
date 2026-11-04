# Despliegue

Estado: solo existe Compose local con puertos limitados a loopback. `local/`, `edge/` y `cloud/` son perfiles destino.

No añadir manifiestos que abran cámaras, APIs o puertos públicamente sin requisitos del operador, threat model, TLS, autenticación, secretos, egress/network policy y observabilidad. Las redes de sensores quedan segregadas; el agente de borde se despliega y aprueba por el propietario.

Cada perfil futuro requiere health/readiness, versiones fijadas, SBOM, escaneo, rollback, backup y runbook.