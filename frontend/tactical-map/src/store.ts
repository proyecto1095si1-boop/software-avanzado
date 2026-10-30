import { create } from "zustand";
import type { Camera, SatellitePosition, ConnectionStatus } from "./types";

interface TacticalState {
  // Data
  satellites: SatellitePosition[];
  cameras: Camera[];
  lastUpdate: string | null;
  connection: ConnectionStatus;
  satelliteGroup: string;

  // Layers
  showSatellites: boolean;
  showCameras: boolean;

  // Selection
  selectedSatellite: SatellitePosition | null;
  selectedCamera: Camera | null;

  // Actions
  setSatellites: (sats: SatellitePosition[], timestamp?: string) => void;
  setCameras: (cams: Camera[]) => void;
  setConnection: (status: ConnectionStatus) => void;
  setSatelliteGroup: (group: string) => void;
  toggleSatellites: () => void;
  toggleCameras: () => void;
  selectSatellite: (sat: SatellitePosition | null) => void;
  selectCamera: (cam: Camera | null) => void;
}

export const useTacticalStore = create<TacticalState>((set) => ({
  satellites: [],
  cameras: [],
  lastUpdate: null,
  connection: "offline",
  satelliteGroup: "stations",

  showSatellites: true,
  showCameras: true,

  selectedSatellite: null,
  selectedCamera: null,

  setSatellites: (sats, timestamp) =>
    set({
      satellites: sats,
      lastUpdate: timestamp ?? new Date().toISOString(),
    }),
  setCameras: (cams) => set({ cameras: cams }),
  setConnection: (status) => set({ connection: status }),
  setSatelliteGroup: (group) => set({ satelliteGroup: group }),
  toggleSatellites: () => set((s) => ({ showSatellites: !s.showSatellites })),
  toggleCameras: () => set((s) => ({ showCameras: !s.showCameras })),
  selectSatellite: (sat) => set({ selectedSatellite: sat, selectedCamera: null }),
  selectCamera: (cam) => set({ selectedCamera: cam, selectedSatellite: null }),
}));
