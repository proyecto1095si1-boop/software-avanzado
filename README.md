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

## Módulos Principales (Roadmap)

### 1. Módulo Satelital (Space Domain Awareness)
- Tracking en tiempo real de satélites (TLE / SGP4)
- Fuentes: CelesTrak, Space-Track, N2YO
- Clasificación de objetos: militares, de reconocimiento, Starlink, ISS, debris
- Predicción de pases sobre zonas de interés
- Visualización de órbitas y footprints

### 2. Módulo Cámaras Públicas (Surface OSINT)
- Agregación de feeds CCTV / tráfico / webcams públicas
- Mapa georreferenciado de cámaras vivas
- Filtrado por región / zona de operaciones
- Posible integración futura de visión artificial (detección de vehículos, personas, anomalías)

### 3. Cuadro de Mando Táctico
- Vista unificada (mapa + lista de activos + feeds en vivo)
- Capas superpuestas: satélites + cámaras + zonas de interés
- Alertas configurables (pase de satélite sobre área, cámara caída, etc.)

### 4. Inteligencia y Análisis
- Registro histórico de posiciones
- Correlación temporal entre eventos orbitales y superficie
- Exportación de datos para informes de inteligencia

---

## Stack Tecnológico

| Capa              | Tecnología                                  |
|-------------------|---------------------------------------------|
| Backend           | Python / FastAPI                            |
| Orbital Mechanics | sgp4 + skyfield                             |
| Realtime          | WebSocket                                   |
| Frontend          | React + MapLibre / Cesium (próximo)         |
| Datos TLE         | CelesTrak                                   |
| Cámaras           | Agregadores open-source + listas públicas   |
| Base de datos     | PostgreSQL + PostGIS (próximo)              |
| Despliegue        | Docker + self-hosted (próximo)              |

---

## Fuentes Open-Source de Referencia

**Satélites:**
- [ShenMian/tracker](https://github.com/ShenMian/tracker)
- [satvisorcom/satvisor](https://github.com/satvisorcom/satvisor)

**Cámaras públicas:**
- [SoCloseSociety/camforge](https://github.com/SoCloseSociety/camforge)

**Combinados / OSINT:**
- [bilawalsidhu/gods-eye-view](https://github.com/bilawalsidhu/gods-eye-view)

---

## Estado Actual (v0.2)

- [x] Repositorio privado creado
- [x] Concepto militar / ISR definido
- [x] Backend FastAPI operativo
- [x] Descarga y parseo de TLE desde CelesTrak
- [x] Propagación SGP4 + skyfield
- [x] Conversión ECI → latitud / longitud / altitud
- [x] Endpoint de posición individual lista para mapa
- [x] Endpoint batch de posiciones (`/satellite/positions/{group}`)
- [x] **Caché de TLE en memoria (TTL 2h)**
- [x] **WebSocket de posiciones en vivo** (`/ws/satellite/positions`)
- [ ] Módulo de cámaras públicas
- [ ] Frontend táctico (MapLibre / Cesium)

**Siguiente paso:** Módulo de cámaras (Surface OSINT) o frontend táctico mínimo.

---

**Clasificación:** Uso privado / desarrollo interno  
**Enfoque:** Conciencia situacional + inteligencia abierta de dominio espacial y terrestre
