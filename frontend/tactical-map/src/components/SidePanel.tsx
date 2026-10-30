import { useTacticalStore } from "../store";

const GROUPS = [
  "stations",
  "visual",
  "military",
  "starlink",
  "weather",
  "gps-ops",
  "science",
  "active",
];

function fmtTime(iso: string) {
  try {
    return new Date(iso).toISOString().replace("T", " ").slice(11, 16);
  } catch {
    return iso;
  }
}

export function SidePanel() {
  const {
    satellites,
    cameras,
    aois,
    alerts,
    passes,
    showSatellites,
    showCameras,
    showAOIs,
    satelliteGroup,
    selectedSatellite,
    selectedCamera,
    selectedAOI,
    toggleSatellites,
    toggleCameras,
    toggleAOIs,
    setSatelliteGroup,
  } = useTacticalStore();

  return (
    <aside className="side">
      <div className="side-section">
        <h3>Capas</h3>
        <div className="layer-row">
          <label>
            <input type="checkbox" checked={showSatellites} onChange={toggleSatellites} />
            <span className="swatch sat" />
            Satélites
          </label>
          <span className="layer-count">{satellites.length}</span>
        </div>
        <div className="layer-row">
          <label>
            <input type="checkbox" checked={showCameras} onChange={toggleCameras} />
            <span className="swatch cam" />
            Cámaras
          </label>
          <span className="layer-count">{cameras.length}</span>
        </div>
        <div className="layer-row">
          <label>
            <input type="checkbox" checked={showAOIs} onChange={toggleAOIs} />
            <span className="swatch" style={{ background: "#3d9eff" }} />
            Zonas (AOI)
          </label>
          <span className="layer-count">{aois.length}</span>
        </div>
      </div>

      <div className="side-section">
        <h3>Grupo orbital</h3>
        <select
          className="select-group"
          value={satelliteGroup}
          onChange={(e) => setSatelliteGroup(e.target.value)}
        >
          {GROUPS.map((g) => (
            <option key={g} value={g}>
              {g}
            </option>
          ))}
        </select>
      </div>

      <div className="side-section alerts-section">
        <h3>
          Alertas ahora{" "}
          {alerts.length > 0 && <span className="alert-badge">{alerts.length}</span>}
        </h3>
        {alerts.length === 0 ? (
          <div className="detail-empty">Sin cruces activos</div>
        ) : (
          <ul className="alert-list">
            {alerts.slice(0, 8).map((a) => (
              <li key={a.id} className={`alert-item severity-${a.severity}`}>
                <div className="alert-title">{a.title}</div>
                <div className="alert-meta">{a.altitude_km.toFixed(0)} km · {a.severity}</div>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="side-section alerts-section">
        <h3>
          Pases próximos{" "}
          {passes.length > 0 && <span className="alert-badge" style={{ background: "#3d9eff" }}>{passes.length}</span>}
        </h3>
        {passes.length === 0 ? (
          <div className="detail-empty">Sin pases en la ventana</div>
        ) : (
          <ul className="alert-list">
            {passes.slice(0, 10).map((p, i) => (
              <li key={`${p.norad_id}-${p.aoi_id}-${i}`} className={`alert-item severity-${p.priority}`}>
                <div className="alert-title">
                  {p.satellite_name} → {p.aoi_name}
                </div>
                <div className="alert-meta">
                  {fmtTime(p.enter_utc)}–{fmtTime(p.exit_utc)} UTC · {Math.round(p.duration_s / 60)} min
                  {p.ongoing ? " · EN CURSO" : ""}
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="detail">
        <h3>Detalle</h3>
        {selectedSatellite && (
          <>
            <div className="detail-name">{selectedSatellite.name}</div>
            <div className="detail-row">
              <span className="k">NORAD</span>
              <span className="v">{selectedSatellite.norad_id ?? "—"}</span>
            </div>
            <div className="detail-row">
              <span className="k">Lat / Lon</span>
              <span className="v">
                {selectedSatellite.latitude.toFixed(4)}°, {selectedSatellite.longitude.toFixed(4)}°
              </span>
            </div>
            <div className="detail-row">
              <span className="k">Altitud</span>
              <span className="v">{selectedSatellite.altitude_km.toFixed(1)} km</span>
            </div>
          </>
        )}
        {selectedCamera && (
          <>
            <div className="detail-name">{selectedCamera.name}</div>
            <div className="detail-row">
              <span className="k">Tipo</span>
              <span className="v">{selectedCamera.type}</span>
            </div>
            <div className="detail-row">
              <span className="k">Ubicación</span>
              <span className="v">
                {[selectedCamera.city, selectedCamera.country].filter(Boolean).join(", ") || "—"}
              </span>
            </div>
          </>
        )}
        {selectedAOI && (
          <>
            <div className="detail-name">{selectedAOI.name}</div>
            <div className="detail-row">
              <span className="k">Prioridad</span>
              <span className="v">{selectedAOI.priority}</span>
            </div>
            {selectedAOI.description && (
              <div className="detail-row">
                <span className="k">Notas</span>
                <span className="v">{selectedAOI.description}</span>
              </div>
            )}
          </>
        )}
        {!selectedSatellite && !selectedCamera && !selectedAOI && (
          <div className="detail-empty">Selecciona un activo en el mapa.</div>
        )}
      </div>
    </aside>
  );
}
