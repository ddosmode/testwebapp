import path from "path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      react: path.resolve(__dirname, "./node_modules/react"),
      "react/jsx-runtime": path.resolve(__dirname, "./node_modules/react/jsx-runtime"),
      "react/jsx-dev-runtime": path.resolve(__dirname, "./node_modules/react/jsx-dev-runtime"),
      "react-dom": path.resolve(__dirname, "./node_modules/react-dom"),
      "react-dom/client": path.resolve(__dirname, "./node_modules/react-dom/client"),
    },
  },
  optimizeDeps: {
    exclude: ['react', 'react-dom', '@testing-library/react'],
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/health': 'http://backend:8000',
      '/database': 'http://backend:8000',
      '/catalog': 'http://backend:8000',
      '/orders': 'http://backend:8000',
      '/payments': 'http://backend:8000',
      '/locations': 'http://backend:8000',
      '/legal': 'http://backend:8000',
      '/api': 'http://backend:8000',
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test-setup.ts',
    deps: {
      inline: ['@testing-library/react', 'react', 'react-dom'],
    },
  },
});
