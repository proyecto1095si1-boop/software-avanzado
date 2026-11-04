# SatCom y telemetría satelital

Estado: scaffold; no hay receptor SDR, decodificador, API de estación terrestre ni conector de misión implementado.

Objetivo admisible: normalizar telemetría o productos de misión que el operador esté autorizado a recibir por API oficial, ground station propia/contratada o fuente abierta/licenciada. El operador debe aportar hardware/servicio, bandas/formatos permitidos, derechos, alcance, límites y política de datos.

El módulo debe mantenerse separado de `satellite/`: TLE/efemérides calculan posición orbital; telemetría es información medida recibida por una fuente autorizada. No implementar interceptación de enlaces privados, elusión/descifrado de protección ni transmisión de comandos.