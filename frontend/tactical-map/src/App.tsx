import { useEffect, useRef } from "react";
import { MapCanvas } from "./components/MapCanvas";
import { SidePanel } from "./components/SidePanel";
import { useTacticalStore } from "./store";
import { fetchCameras, positionsWebSocketUrl } from "./api";
import type { PositionsMessage } from "./types";

export default function App() {
  const {
    connection,
    lastUpdate,
    satellites,
    cameras,
    satelliteGroup,
    setSatellites,
    setCameras,
    setConnection,
  } = useTacticalStore();

  const wsRef = useRef<WebSocket | null>(null);
  const retryRef = useRef<number>(0);

  // Load cameras once
  useEffect(() => {
    fetchCameras()
      .then(setCameras)
      .catch((err) => console.error("cameras", err));
  }, [setCameras]);

  // WebSocket for satellites — reconnects when group changes
  useEffect(() => {
    let closed = false;
    let timer: number | undefined;

    function connect() {
      if (closed) return;
      setConnection(retryRef.current > 0 ? "reconnecting" : "connecting");

      const url = positionsWebSocketUrl(satelliteGroup, 5, 200);
      const ws = new WebSocket(url);
      wsRef.current = ws;

      ws.onopen = () => {
        retryRef.current = 0;
        setConnection("live");
      };

      ws.onmessage = (ev) => {
        try {
          const msg: PositionsMessage = JSON.parse(ev.data);
          if (msg.type === "positions" && msg.satellites) {
            setSatellites(msg.satellites, msg.timestamp_utc);
          }
        } catch {
          /* ignore parse errors */
        }
      };

      ws.onclose = () => {
        setConnection("offline");
        if (closed) return;
        const delay = Math.min(10000, 1500 * Math.pow(1.5, retryRef.current));
        retryRef.current += 1;
        timer = window.setTimeout(connect, delay);
      };

      ws.onerror = () => {
        ws.close();
      };
    }

    connect();

    return () => {
      closed = true;
      if (timer) clearTimeout(timer);
      wsRef.current?.close();
      wsRef.current = null;
    };
  }, [satelliteGroup, setSatellites, setConnection]);

  const statusLabel =
    connection === "live"
      ? "LIVE"
      : connection === "connecting"
        ? "CONECTANDO"
        : connection === "reconnecting"
          ? "RECONECTANDO"
          : "OFFLINE";

  return (
    <div className="app">
      <header className="header">
        <div className="header-title">
          Software Avanzado
          <span>Cuadro de Mando Táctico</span>
        </div>
        <div className="header-meta">
          <span>
            <span className={`status-dot ${connection}`} />
            {statusLabel}
          </span>
          <span>Grupo: {satelliteGroup}</span>
        </div>
      </header>

      <div className="main">
        <MapCanvas />
        <SidePanel />
      </div>

      <footer className="statusbar">
        <span>
          Satélites: <strong>{satellites.length}</strong>
          {" · "}
          Cámaras: <strong>{cameras.length}</strong>
        </span>
        <span>
          Última actualización:{" "}
          <strong>
            {lastUpdate
              ? new Date(lastUpdate).toISOString().replace("T", " ").slice(0, 19) + " UTC"
              : "—"}
          </strong>
        </span>
      </footer>
    </div>
  );
}
