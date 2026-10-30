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
    showSatellites,
    showCameras,
    satelliteGroup,
    selectedSatellite,
    selectedCamera,
    toggleSatellites,
    toggleCameras,
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
              <span className="k">Lat</span>
              <span className="v">{selectedSatellite.latitude.toFixed(4)}°</span>
            </div>
            <div className="detail-row">
              <span className="k">Lon</span>
              <span className="v">{selectedSatellite.longitude.toFixed(4)}°</span>
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
              <span className="k">ID</span>
              <span className="v">{selectedCamera.id}</span>
            </div>
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
            <div className="detail-row">
              <span className="k">Lat / Lon</span>
              <span className="v">
                {selectedCamera.latitude.toFixed(3)}, {selectedCamera.longitude.toFixed(3)}
              </span>
            </div>
          </>
        )}
        {!selectedSatellite && !selectedCamera && (
          <div className="detail-empty">
            Selecciona un satélite o una cámara en el mapa para ver el detalle.
          </div>
        )}
      </div>
    </aside>
  );
}
