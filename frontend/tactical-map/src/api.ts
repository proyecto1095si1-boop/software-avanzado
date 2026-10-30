import type { Camera, SatellitePosition, AOI, Alert, Pass } from "./types";

const BASE = "";

export interface TrackResponse {
  name: string;
  norad_id?: string;
  segments: number[][][];
  point_count: number;
  classification?: { category: string; tags: string[]; high_interest: boolean };
}

export async function fetchCameras(params?: {
  country?: string;
  type?: string;
  bbox?: string;
}): Promise<Camera[]> {
  const q = new URLSearchParams();
  if (params?.country) q.set("country", params.country);
  if (params?.type) q.set("type", params.type);
  if (params?.bbox) q.set("bbox", params.bbox);
  const res = await fetch(`${BASE}/cameras?${q.toString()}`);
  if (!res.ok) throw new Error(`cameras ${res.status}`);
  const data = await res.json();
  return data.cameras ?? [];
}

export async function fetchAOIs(): Promise<AOI[]> {
  const res = await fetch(`${BASE}/aoi`);
  if (!res.ok) throw new Error(`aoi ${res.status}`);
  const data = await res.json();
  return data.aois ?? [];
}

export async function fetchAlerts(group = "stations", limit = 200): Promise<Alert[]> {
  const q = new URLSearchParams({ group, limit: String(limit) });
  const res = await fetch(`${BASE}/alerts/check?${q.toString()}`);
  if (!res.ok) throw new Error(`alerts ${res.status}`);
  const data = await res.json();
  return data.alerts ?? [];
}

export async function fetchPasses(
  group = "stations",
  hours = 6,
  maxSats = 25
): Promise<Pass[]> {
  const q = new URLSearchParams({
    group,
    hours: String(hours),
    max_sats: String(maxSats),
  });
  const res = await fetch(`${BASE}/satellite/passes?${q.toString()}`);
  if (!res.ok) throw new Error(`passes ${res.status}`);
  const data = await res.json();
  return data.passes ?? [];
}

export async function fetchTrack(
  group: string,
  noradOrName: string
): Promise<TrackResponse> {
  const res = await fetch(
    `${BASE}/satellite/track/${encodeURIComponent(group)}/${encodeURIComponent(noradOrName)}`
  );
  if (!res.ok) throw new Error(`track ${res.status}`);
  return res.json();
}

export function positionsWebSocketUrl(
  group = "stations",
  interval = 5,
  limit?: number
): string {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const host = window.location.host;
  const q = new URLSearchParams({ group, interval: String(interval) });
  if (limit) q.set("limit", String(limit));
  return `${protocol}//${host}/ws/satellite/positions?${q.toString()}`;
}
