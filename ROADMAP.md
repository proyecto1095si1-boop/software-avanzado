# Roadmaps — Software Avanzado

La visión integral y el orden de implementación se mantienen en estos documentos:

- **[ROADMAP_PLATAFORMA.md](ROADMAP_PLATAFORMA.md)** — expansión por dominios (cámaras, aeronaves, satélites, radar, meteorología, marítimo e imágenes), matriz de estado, estructura del repositorio, acciones, fases y criterios de aceptación.
- **[ROADMAP_INTEGRAL.md](ROADMAP_INTEGRAL.md)** — arquitectura, salvaguardas de cámaras, seguridad, pruebas y operación.
- **[docs/IMPLEMENTACION_INICIAL.md](docs/IMPLEMENTACION_INICIAL.md)** — contratos, scaffolds y acciones para el siguiente incremento.
- **[docs/arquitectura.md](docs/arquitectura.md)** — arquitectura y límites funcionales actuales.
- **[docs/apis.md](docs/apis.md)** — estado real de conectores y requisitos de integración.

## Estado técnico resumido

Implementado: backend FastAPI, frontend React/MapLibre, TLE CelesTrak y propagación orbital básica, AOI, alertas, pases, posición en WebSocket y cámaras de demostración. Hay contratos iniciales de conector y un esquema para registrar cámaras autorizadas.

En scaffold/documentación: dominios de aviación, marítimo/AIS, radar, meteorología y observación terrestre; módulos de identidad, política, auditoría, persistencia, catálogos de proveedores y funciones frontend por dominio.

No conectado todavía: ADS-B, AIS, feeds de radar externos, API meteorológica, inventario operativo/ONVIF/video, telemetría de satélite, imágenes comerciales o APIs de operador. Una carpeta o variable de configuración no constituye una conexión funcional.

## Prioridad

1. CI, contrato de evento versionado y pruebas continuas.
2. Identidad, autorización por tenant/sitio/objeto y auditoría.
3. Persistencia y catálogo real de fuentes con frescura.
4. Un vertical seguro por vez: elegir una cámara de laboratorio propia o un feed de aviación autorizado; implementarlo de extremo a extremo con adaptador, API, UI, health y pruebas.
5. Seguir con feeds satelitales, radar/clima, marítimo e imágenes según permisos, hardware, licencia y caso de uso.

## Salvaguardas y realidad del alcance

La meta es monitoreo y apoyo a operadores, con supervisión humana. No se buscarán cámaras de terceros, no se escanearán redes ajenas y no se sortearán credenciales. Los datos satelitales de posición calculada no contienen por sí mismos el payload que transmite un satélite: telemetría o contenido solo se integran desde servicios/estaciones autorizados o fuentes abiertas con permiso. No se habilita descifrado de enlaces privados ni control de hardware operacional.

“Grado militar” no es una certificación que pueda afirmarse por el código. Cualquier uso crítico exige requisitos del operador, evaluación independiente, aprobación y acreditación aplicables.
