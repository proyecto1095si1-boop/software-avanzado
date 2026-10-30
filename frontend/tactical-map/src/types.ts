export interface SatellitePosition {
  name: string;
  norad_id?: string;
  latitude: number;
  longitude: number;
  altitude_km: number;
  speed_km_s?: number;
  timestamp_utc: string;
}

export interface Camera {
  id: string;
  name: string;
  latitude: number;
  longitude: number;
  url?: string | null;
  type: string;
  status: string;
  country?: string | null;
  city?: string | null;
  source?: string | null;
  notes?: string | null;
}

export interface AOI {
  id: string;
  name: string;
  description?: string | null;
  coordinates: number[][];
  color: string;
  priority: string;
}

export interface PositionsMessage {
  type: "positions" | "error";
  group?: string;
  count?: number;
  timestamp_utc?: string;
  satellites?: SatellitePosition[];
  detail?: string;
}

export type ConnectionStatus = "connecting" | "live" | "reconnecting" | "offline";
