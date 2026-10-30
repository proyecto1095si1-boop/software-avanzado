import { useTacticalStore } from "../store";

const GROUPS = [
  "stations",
  "visual",
  "starlink",
  "weather",
  "gps-ops",
  "science",
  "active",
];

export function SidePanel() {
  const {
    satellites,
    cameras,
    aois,
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
            {selectedSatellite.speed_km_s != null && (
              <div className="detail-row">
                <span className="k">Velocidad</span>
                <span className="v">{selectedSatellite.speed_km_s.toFixed(2)} km/s</span>
              </div>
            )}
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
              <span className="k">Estado</span>
              <span className="v">{selectedCamera.status}</span>
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
          <div className="detail-empty">
            Selecciona un satélite, cámara o zona de interés en el mapa.
          </div>
        )}
      </div>
    </aside>
  );
}
