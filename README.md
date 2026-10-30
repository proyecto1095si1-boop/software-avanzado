# SOFTWARE AVANZADO

**Sistema ISR en tiempo real — cuadro de mando táctico unificado**

## Arranque

```bash
docker compose up --build
# Panel http://localhost:5173 · API http://localhost:8000/docs
```

## Capacidades (v0.8)

| Módulo | Qué hace |
|--------|----------|
| Space Domain | TLE + SGP4/skyfield → posiciones LIVE |
| Ground track | Traza orbital al seleccionar un satélite |
| Clasificación | military / recon / nav / weather / station… |
| Alertas | Satélite **ahora** dentro de AOI |
| Pases | Predicción de entradas/salidas sobre AOI |
| Surface OSINT | Cámaras públicas |
| AOI | Zonas estratégicas (BA, Malvinas, Gibraltar, Panamá, Suez, Ormuz, Taiwán…) |
| Docker | Backend + panel de un comando |

### Flujo táctico en el panel

1. Elegí grupo (`stations`, `military`, `starlink`…)
2. Mapa LIVE de satélites + cámaras + polígonos AOI
3. **Click en satélite** → traza orbital + categoría + interés alto
4. Alertas actuales y pases próximos en el lateral

### API útil

- `GET /satellite/track/{group}/{norad_id}` — traza
- `GET /satellite/classified/{group}` — posiciones + categoría
- `GET /satellite/passes?hours=6` — pases
- `GET /alerts/check` — cruces actuales
- `WS /ws/satellite/positions` — stream

**Clasificación:** Uso privado / desarrollo interno
