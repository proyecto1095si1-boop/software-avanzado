import type { Camera, SatellitePosition } from "./types";

const BASE = ""; // proxy de Vite en dev

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

export async function fetchPositions(
  group: string = "stations",
  limit?: number
): Promise<{ count: number; timestamp_utc?: string; satellites: SatellitePosition[] }> {
  const q = new URLSearchParams();
  if (limit) q.set("limit", String(limit));
  const res = await fetch(`${BASE}/satellite/positions/${group}?${q.toString()}`);
  if (!res.ok) throw new Error(`positions ${res.status}`);
  return res.json();
}

export function positionsWebSocketUrl(
  group: string = "stations",
  interval: number = 5,
  limit?: number
): string {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const host = window.location.host;
  const q = new URLSearchParams({ group, interval: String(interval) });
  if (limit) q.set("limit", String(limit));
  return `${protocol}//${host}/ws/satellite/positions?${q.toString()}`;
}
