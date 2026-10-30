import { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";
import { useTacticalStore } from "../store";
import type { SatellitePosition, Camera, AOI } from "../types";

const SAT_SOURCE = "satellites";
const CAM_SOURCE = "cameras";
const AOI_SOURCE = "aois";
const TRACK_SOURCE = "track";

function satsToGeoJSON(sats: SatellitePosition[]) {
  return {
    type: "FeatureCollection" as const,
    features: sats.map((s) => ({
      type: "Feature" as const,
      properties: {
        name: s.name,
        norad_id: s.norad_id ?? "",
        altitude_km: s.altitude_km,
        speed_km_s: s.speed_km_s ?? 0,
      },
      geometry: {
        type: "Point" as const,
        coordinates: [s.longitude, s.latitude],
      },
    })),
  };
}

function camsToGeoJSON(cams: Camera[]) {
  return {
    type: "FeatureCollection" as const,
    features: cams.map((c) => ({
      type: "Feature" as const,
      properties: {
        id: c.id,
        name: c.name,
        type: c.type,
        status: c.status,
        city: c.city ?? "",
        country: c.country ?? "",
      },
      geometry: {
        type: "Point" as const,
        coordinates: [c.longitude, c.latitude],
      },
    })),
  };
}

function aoisToGeoJSON(aois: AOI[]) {
  return {
    type: "FeatureCollection" as const,
    features: aois.map((a) => ({
      type: "Feature" as const,
      properties: {
        id: a.id,
        name: a.name,
        description: a.description ?? "",
        priority: a.priority,
        color: a.color,
      },
      geometry: {
        type: "Polygon" as const,
        coordinates: [a.coordinates],
      },
    })),
  };
}

function trackToGeoJSON(segments: number[][][] | undefined) {
  if (!segments?.length) {
    return { type: "FeatureCollection" as const, features: [] };
  }
  return {
    type: "FeatureCollection" as const,
    features: segments.map((coords) => ({
      type: "Feature" as const,
      properties: {},
      geometry: {
        type: "LineString" as const,
        coordinates: coords,
      },
    })),
  };
}

export function MapCanvas() {
  const mapRef = useRef<maplibregl.Map | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const satellites = useTacticalStore((s) => s.satellites);
  const cameras = useTacticalStore((s) => s.cameras);
  const aois = useTacticalStore((s) => s.aois);
  const track = useTacticalStore((s) => s.track);
  const showSatellites = useTacticalStore((s) => s.showSatellites);
  const showCameras = useTacticalStore((s) => s.showCameras);
  const showAOIs = useTacticalStore((s) => s.showAOIs);
  const showTrack = useTacticalStore((s) => s.showTrack);
  const selectSatellite = useTacticalStore((s) => s.selectSatellite);
  const selectCamera = useTacticalStore((s) => s.selectCamera);
  const selectAOI = useTacticalStore((s) => s.selectAOI);

  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;

    const map = new maplibregl.Map({
      container: containerRef.current,
      style: {
        version: 8,
        sources: {
          basemap: {
            type: "raster",
            tiles: ["https://basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png"],
            tileSize: 512,
            attribution: "© CARTO",
          },
        },
        layers: [{ id: "basemap", type: "raster", source: "basemap" }],
      },
      center: [0, 20],
      zoom: 1.4,
      attributionControl: false,
    });

    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");

    map.on("load", () => {
      map.addSource(AOI_SOURCE, { type: "geojson", data: aoisToGeoJSON([]) });
      map.addSource(TRACK_SOURCE, { type: "geojson", data: trackToGeoJSON([]) });
      map.addSource(SAT_SOURCE, { type: "geojson", data: satsToGeoJSON([]) });
      map.addSource(CAM_SOURCE, { type: "geojson", data: camsToGeoJSON([]) });

      map.addLayer({
        id: "aois-fill",
        type: "fill",
        source: AOI_SOURCE,
        paint: { "fill-color": ["get", "color"], "fill-opacity": 0.18 },
      });
      map.addLayer({
        id: "aois-line",
        type: "line",
        source: AOI_SOURCE,
        paint: {
          "line-color": ["get", "color"],
          "line-width": 2,
          "line-opacity": 0.85,
        },
      });

      map.addLayer({
        id: "track-line",
        type: "line",
        source: TRACK_SOURCE,
        paint: {
          "line-color": "#5ce1a8",
          "line-width": 2,
          "line-opacity": 0.75,
          "line-dasharray": [2, 1],
        },
      });

      map.addLayer({
        id: "satellites-circle",
        type: "circle",
        source: SAT_SOURCE,
        paint: {
          "circle-radius": 5,
          "circle-color": "#5ce1a8",
          "circle-stroke-width": 1,
          "circle-stroke-color": "#0a0e14",
          "circle-opacity": 0.9,
        },
      });

      map.addLayer({
        id: "cameras-circle",
        type: "circle",
        source: CAM_SOURCE,
        paint: {
          "circle-radius": 6,
          "circle-color": "#f0a050",
          "circle-stroke-width": 1.5,
          "circle-stroke-color": "#0a0e14",
          "circle-opacity": 0.95,
        },
      });

      map.on("click", "satellites-circle", (e) => {
        const f = e.features?.[0];
        if (!f) return;
        const p = f.properties;
        selectSatellite({
          name: p?.name ?? "",
          norad_id: p?.norad_id,
          latitude: (f.geometry as GeoJSON.Point).coordinates[1],
          longitude: (f.geometry as GeoJSON.Point).coordinates[0],
          altitude_km: p?.altitude_km ?? 0,
          speed_km_s: p?.speed_km_s,
          timestamp_utc: new Date().toISOString(),
        });
      });

      map.on("click", "cameras-circle", (e) => {
        const f = e.features?.[0];
        if (!f) return;
        const p = f.properties;
        selectCamera({
          id: p?.id ?? "",
          name: p?.name ?? "",
          latitude: (f.geometry as GeoJSON.Point).coordinates[1],
          longitude: (f.geometry as GeoJSON.Point).coordinates[0],
          type: p?.type ?? "other",
          status: p?.status ?? "unknown",
          city: p?.city,
          country: p?.country,
        });
      });

      map.on("click", "aois-fill", (e) => {
        const f = e.features?.[0];
        if (!f) return;
        const p = f.properties;
        const coords = (f.geometry as GeoJSON.Polygon).coordinates[0] as number[][];
        selectAOI({
          id: p?.id ?? "",
          name: p?.name ?? "",
          description: p?.description,
          coordinates: coords,
          color: p?.color ?? "#3d9eff",
          priority: p?.priority ?? "normal",
        });
      });

      ["satellites-circle", "cameras-circle", "aois-fill"].forEach((layer) => {
        map.on("mouseenter", layer, () => {
          map.getCanvas().style.cursor = "pointer";
        });
        map.on("mouseleave", layer, () => {
          map.getCanvas().style.cursor = "";
        });
      });
    });

    mapRef.current = map;
    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, [selectSatellite, selectCamera, selectAOI]);

  useEffect(() => {
    const map = mapRef.current;
    if (!map?.getSource(SAT_SOURCE)) return;
    (map.getSource(SAT_SOURCE) as maplibregl.GeoJSONSource).setData(
      satsToGeoJSON(showSatellites ? satellites : [])
    );
  }, [satellites, showSatellites]);

  useEffect(() => {
    const map = mapRef.current;
    if (!map?.getSource(CAM_SOURCE)) return;
    (map.getSource(CAM_SOURCE) as maplibregl.GeoJSONSource).setData(
      camsToGeoJSON(showCameras ? cameras : [])
    );
  }, [cameras, showCameras]);

  useEffect(() => {
    const map = mapRef.current;
    if (!map?.getSource(AOI_SOURCE)) return;
    (map.getSource(AOI_SOURCE) as maplibregl.GeoJSONSource).setData(
      aoisToGeoJSON(showAOIs ? aois : [])
    );
  }, [aois, showAOIs]);

  useEffect(() => {
    const map = mapRef.current;
    if (!map?.getSource(TRACK_SOURCE)) return;
    const segments = showTrack && track ? track.segments : [];
    (map.getSource(TRACK_SOURCE) as maplibregl.GeoJSONSource).setData(
      trackToGeoJSON(segments)
    );
  }, [track, showTrack]);

  return <div ref={containerRef} className="map-wrap" />;
}
