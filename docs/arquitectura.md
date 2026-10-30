# Arquitectura del Sistema - Software Avanzado

## Visión General

Sistema ISR (Intelligence, Surveillance, Reconnaissance) de conciencia situacional en tiempo real.

### Dominios

1. **Space Domain Awareness (SDA)**
   - Tracking orbital de satélites militares, de reconocimiento y comerciales
   - Fuentes: CelesTrak, Space-Track, N2YO
   - Propagación: SGP4

2. **Surface OSINT**
   - Agregación de feeds de cámaras públicas (CCTV, tráfico, webcams)
   - Fuentes prioritarias: Argus, camforge, listas gubernamentales abiertas

3. **Cuadro de Mando Táctico**
   - Visualización unificada en mapa/globo 3D
   - Capas: satélites + cámaras + bases + alertas

## Stack Inicial Recomendado

- **Backend**: Python 3.11+ + FastAPI
- **Orbital**: `sgp4` + `skyfield` o `satellite.js` (si frontend)
- **Frontend**: React + MapLibre / Cesium
- **Base de datos**: PostgreSQL + PostGIS
- **Datos TLE**: CelesTrak (público)

## Estructura de Carpetas

```
software-avanzado/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── satellite/
│   │   ├── cameras/
│   │   └── api/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   └── tactical-map/
├── data/
│   ├── tle/
│   └── camera-lists/
├── docs/
└── docker-compose.yml
```
