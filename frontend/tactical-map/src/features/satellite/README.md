# Interfaz de satélites

Estado: el mapa y endpoints actuales cubren TLE/propagación básicos; esta carpeta es scaffold para una feature modular.

Vista futura: posición calculada, timestamp/edad y fuente de elementos orbitales, incertidumbre y pase previsto. Diferenciar posición propagada de telemetría observada. La ubicación orbital no entrega por sí misma contenido que transmite el satélite.

Telemetría/enlaces solo se integran desde una API de operador/ground-station autorizada o emisiones abiertas cuyo uso esté permitido. No incluye interceptar, descifrar o eludir controles de comunicaciones privadas.