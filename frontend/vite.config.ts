import tailwindcss from "@tailwindcss/vite";
import basicSsl from "@vitejs/plugin-basic-ssl";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import path from "path"


export default defineConfig({
  plugins: [tailwindcss(), react(), basicSsl()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },

  
  server: {
    https: {},
    proxy: {
      "/api/v1": {
        target: "http://127.0.0.1:4010",
        changeOrigin: true,
        secure: true,
        followRedirects: true
      }
    }
  }
});
