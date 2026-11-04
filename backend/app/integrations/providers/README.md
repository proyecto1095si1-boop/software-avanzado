# Catálogo de proveedores

Submódulos: `space`, `aviation`, `maritime`, `radar`, `weather`, `earth_observation` y `cameras`. La estructura indica áreas de trabajo, no conectores activos. Solo CelesTrak está cableado hoy y vive en `app/satellite/tle.py`.

Toda fuente nueva debe estar autorizada/licenciada, tener límites, red permitida, contrato tipado, estado de salud, frescura visible, métricas y pruebas deterministas. No cargar plugins arbitrarios ni aceptar endpoints de red suministrados libremente por el usuario.