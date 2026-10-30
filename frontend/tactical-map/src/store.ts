import { create } from "zustand";
import type { Camera, SatellitePosition, ConnectionStatus, AOI, Alert } from "./types";

interface TacticalState {
  satellites: SatellitePosition[];
  cameras: Camera[];
  aois: AOI[];
  alerts: Alert[];
  lastUpdate: string | null;
  connection: ConnectionStatus;
  satelliteGroup: string;

  showSatellites: boolean;
  showCameras: boolean;
  showAOIs: boolean;

  selectedSatellite: SatellitePosition | null;
  selectedCamera: Camera | null;
  selectedAOI: AOI | null;

  setSatellites: (sats: SatellitePosition[], timestamp?: string) => void;
  setCameras: (cams: Camera[]) => void;
  setAOIs: (aois: AOI[]) => void;
  setAlerts: (alerts: Alert[]) => void;
  setConnection: (status: ConnectionStatus) => void;
  setSatelliteGroup: (group: string) => void;
  toggleSatellites: () => void;
  toggleCameras: () => void;
  toggleAOIs: () => void;
  selectSatellite: (sat: SatellitePosition | null) => void;
  selectCamera: (cam: Camera | null) => void;
  selectAOI: (aoi: AOI | null) => void;
}

export const useTacticalStore = create<TacticalState>((set) => ({
  satellites: [],
  cameras: [],
  aois: [],
  alerts: [],
  lastUpdate: null,
  connection: "offline",
  satelliteGroup: "stations",

  showSatellites: true,
  showCameras: true,
  showAOIs: true,

  selectedSatellite: null,
  selectedCamera: null,
  selectedAOI: null,

  setSatellites: (sats, timestamp) =>
    set({
      satellites: sats,
      lastUpdate: timestamp ?? new Date().toISOString(),
    }),
  setCameras: (cams) => set({ cameras: cams }),
  setAOIs: (aois) => set({ aois }),
  setAlerts: (alerts) => set({ alerts }),
  setConnection: (status) => set({ connection: status }),
  setSatelliteGroup: (group) => set({ satelliteGroup: group }),
  toggleSatellites: () => set((s) => ({ showSatellites: !s.showSatellites })),
  toggleCameras: () => set((s) => ({ showCameras: !s.showCameras })),
  toggleAOIs: () => set((s) => ({ showAOIs: !s.showAOIs })),
  selectSatellite: (sat) =>
    set({ selectedSatellite: sat, selectedCamera: null, selectedAOI: null }),
  selectCamera: (cam) =>
    set({ selectedCamera: cam, selectedSatellite: null, selectedAOI: null }),
  selectAOI: (aoi) =>
    set({ selectedAOI: aoi, selectedSatellite: null, selectedCamera: null }),
}));
