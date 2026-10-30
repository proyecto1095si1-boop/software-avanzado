import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const backend = "http://localhost:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/satellite": backend,
      "/cameras": backend,
      "/aoi": backend,
      "/alerts": backend,
      "/system": backend,
      "/health": backend,
      "/docs": backend,
      "/openapi.json": backend,
      "/ws": {
        target: "ws://localhost:8000",
        ws: true,
      },
    },
  },
});
