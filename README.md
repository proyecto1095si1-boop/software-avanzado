# SOFTWARE AVANZADO

**Sistema de Inteligencia, Vigilancia y Reconocimiento (ISR) en Tiempo Real**

Plataforma privada orientada a operaciones de conciencia situacional militar. Integra tracking satelital global y feeds de cámaras públicas para generar un cuadro de mando unificado de inteligencia geoespacial.

---

## Concepto Militar

Este sistema está diseñado con una **esencia táctica / militar**:

- **ISR** (Intelligence, Surveillance, Reconnaissance)
- Conciencia situacional en tiempo real (Real-Time Situational Awareness)
- Integración de sensores espaciales + sensores terrestres abiertos (OSINT)
- Visualización en mapa táctico / globo 3D
- Enfoque en activos de interés (satélites militares, comerciales y de reconocimiento)
- Feeds de cámaras públicas como fuente de inteligencia abierta de superficie

No es un juguete civil. Está pensado como núcleo de un **sistema de apoyo a la decisión** para análisis de escenarios, monitoreo de zonas de interés y seguimiento de objetos orbitales.

---

## Módulos Principales

### 1. Módulo Satelital (Space Domain Awareness) — OPERATIVO
- Tracking en tiempo real de satélites (TLE / SGP4 + skyfield)
- Caché de TLE + WebSocket de posiciones en vivo
- Coordenadas geodésicas listas para mapa

### 2. Módulo Cámaras Públicas (Surface OSINT) — OPERATIVO (v0.3)
- Inventario curado de cámaras públicas georreferenciadas
- API de filtrado por tipo, país, estado y bounding box
- Base lista para expandir con más fuentes (Insecam-style, listas oficiales)

### 3. Cuadro de Mando Táctico — PENDIENTE
- Vista unificada (mapa + capas de satélites + cámaras)
- Capas superpuestas + alertas

### 4. Inteligencia y Análisis — FUTURO
- Correlación temporal entre eventos orbitales y superficie

---

## Stack Tecnológico

| Capa              | Tecnología                                  |
|-------------------|---------------------------------------------|
| Backend           | Python / FastAPI                            |
| Orbital Mechanics | sgp4 + skyfield                             |
| Realtime          | WebSocket                                   |
| Frontend          | React + MapLibre / Cesium (próximo)         |
| Datos TLE         | CelesTrak                                   |
| Cámaras           | Inventario curado + APIs públicas           |

---

## Estado Actual (v0.3)

- [x] Backend FastAPI operativo
- [x] Propagación SGP4 + skyfield (lat/lon/alt)
- [x] Endpoint batch de posiciones
- [x] Caché de TLE (TTL 2h)
- [x] WebSocket de posiciones en vivo
- [x] **Módulo de cámaras públicas (API + inventario inicial)**
- [ ] Expansión de fuentes de cámaras
- [ ] Frontend táctico (MapLibre / Cesium)

**Siguiente paso:** Frontend táctico mínimo que consuma satélites + cámaras.

---

**Clasificación:** Uso privado / desarrollo interno  
**Enfoque:** Conciencia situacional + inteligencia abierta de dominio espacial y terrestre
