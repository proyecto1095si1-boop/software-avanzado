# Contratos compartidos

Esta carpeta contiene contratos versionados entre backend, conectores y servicios auxiliares. Un cambio incompatible debe incrementar la versión y mantener una transición documentada.

`event-envelope.v1.schema.json` define un sobre común; cada dominio mantiene un `payload` específico y tipado. El sobre conserva fuente, identidad de evento, tiempo observado/ingerido, clase de dato, calidad, alcance de autorización, licencia y referencia de correlación. No contiene credenciales, URLs secretas ni datos personales innecesarios.

Los mensajes de fuentes distintas no se fusionan sin preservar la procedencia original. La coordenada representa una observación o cálculo según `data_kind`; no se debe inferir precisión a partir de un dibujo en el mapa.
