import { useEffect, useRef } from "react";
import { MapCanvas } from "./components/MapCanvas";
import { SidePanel } from "./components/SidePanel";
import { useTacticalStore } from "./store";
import {
  fetchCameras,
  fetchAOIs,
  fetchAlerts,
  fetchPasses,
  positionsWebSocketUrl,
} from "./api";
import type { PositionsMessage } from "./types";

export default function App() {
  const {
    connection,
    lastUpdate,
    satellites,
    cameras,
    aois,
    alerts,
    passes,
    satelliteGroup,
    setSatellites,
    setCameras,
    setAOIs,
    setAlerts,
    setPasses,
    setConnection,
  } = useTacticalStore();

  const wsRef = useRef<WebSocket | null>(null);
  const retryRef = useRef<number>(0);

  useEffect(() => {
    fetchCameras()
      .then(setCameras)
      .catch((err) => console.error("cameras", err));
    fetchAOIs()
      .then(setAOIs)
      .catch((err) => console.error("aoi", err));
  }, [setCameras, setAOIs]);

  // Alertas (cada 15s) + pases (cada 5 min)
  useEffect(() => {
    let cancelled = false;

    async function refreshAlerts() {
      try {
        const list = await fetchAlerts(satelliteGroup, 200);
        if (!cancelled) setAlerts(list);
      } catch (err) {
        console.error("alerts", err);
      }
    }

    async function refreshPasses() {
      try {
        const list = await fetchPasses(satelliteGroup, 6, 25);
        if (!cancelled) setPasses(list);
      } catch (err) {
        console.error("passes", err);
      }
    }

    refreshAlerts();
    refreshPasses();
    const aId = window.setInterval(refreshAlerts, 15000);
    const pId = window.setInterval(refreshPasses, 5 * 60 * 1000);
    return () => {
      cancelled = true;
      clearInterval(aId);
      clearInterval(pId);
    };
  }, [satelliteGroup, setAlerts, setPasses]);

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
          /* ignore */
        }
      };

      ws.onclose = () => {
        setConnection("offline");
        if (closed) return;
        const delay = Math.min(10000, 1500 * Math.pow(1.5, retryRef.current));
        retryRef.current += 1;
        timer = window.setTimeout(connect, delay);
      };

      ws.onerror = () => ws.close();
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
          {alerts.length > 0 && (
            <span className="header-alerts">{alerts.length} alertas</span>
          )}
          <span>Grupo: {satelliteGroup}</span>
        </div>
      </header>

      <div className="main">
        <MapCanvas />
        <SidePanel />
      </div>

      <footer className="statusbar">
        <span>
          SAT <strong>{satellites.length}</strong>
          {" · "}
          CAM <strong>{cameras.length}</strong>
          {" · "}
          AOI <strong>{aois.length}</strong>
          {" · "}
          ALT <strong>{alerts.length}</strong>
          {" · "}
          PAS <strong>{passes.length}</strong>
        </span>
        <span>
          UTC{" "}
          <strong>
            {lastUpdate
              ? new Date(lastUpdate).toISOString().replace("T", " ").slice(0, 19)
              : "—"}
          </strong>
        </span>
      </footer>
    </div>
  );
}
