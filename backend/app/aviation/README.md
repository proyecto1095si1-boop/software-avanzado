# Dominio aeronáutico

Estado: scaffold; no hay conector ni endpoints de aeronaves.

Responsabilidad prevista: normalizar tracks recibidos de proveedores ADS-B/Mode-S autorizados, custodiar procedencia/licencia y exponer frescura/cobertura. Debe distinguir ADS-B cooperativo de radar ATC: no son la misma observación ni tienen idéntica cobertura.

Acciones futuras: catálogo de fuentes, consulta por área/tiempo, track histórico según licencia, alertas operativas configurables y calidad del feed. No se implementan identificación de aeronaves privadas fuera de permisos, control ATC ni órdenes a aeronaves. Cada proveedor requiere contrato, límites, política de datos y prueba de desconexión.