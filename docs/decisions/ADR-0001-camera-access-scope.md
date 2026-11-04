# ADR-0001: Alcance de integración de cámaras

- Estado: Aceptada para el desarrollo inicial
- Fecha: 2026-11-04

## Contexto

El sistema quiere reunir metadatos y eventualmente video de cámaras IP. El backend actual no dispone de autenticación, autorización por recurso ni persistencia operativa. Una ruta que acepte una URL/host arbitrario podría convertir al servicio en un proxy de red (SSRF) y exponer sensores o redes privadas.

## Decisión

La primera integración será un **inventario administrado de cámaras propias o expresamente autorizadas**. El registro requiere sitio, alcance de red aprobado, IP/hostname y referencia de autorización. Un registro no dispara ninguna conexión. La lectura de salud o metadatos solo se implementará después de autenticar usuarios, aplicar permisos por cámara, validar el destino contra una allowlist y definir un agente dentro de la red propietaria.

Los secretos quedarán fuera del inventario y del navegador. Una integración posterior usará ONVIF/HTTPS o la API oficial de un VMS con credenciales de mínimo privilegio. El video, si se autoriza, pasará por un relay/VMS y tendrá permisos temporales y auditoría.

## Alternativas descartadas

- Escanear Internet o rangos amplios buscando cámaras: fuera de alcance.
- Aceptar URLs libres desde la API y consultarlas desde el servidor: descartado por SSRF y por ausencia de control de destino.
- Almacenar contraseñas, URL RTSP con credenciales o tokens en la fila de cámara: descartado por riesgo de exposición.
- Habilitar rutas CRUD antes de identidad/autorización: descartado por exposición de inventario y falta de separación entre operadores.

## Consecuencias

La entrega inicial contiene únicamente contratos, validación de datos y documentación. No ofrece aún registro persistente, conexión ONVIF, salud de red, video ni acceso remoto. Las próximas fases deben completar identidad, política por objeto, auditoría, base de datos y agente de borde antes de añadir esas capacidades.
