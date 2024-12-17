import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0', // Escucha en todas las interfaces
    port: 5173,
    strictPort: true,
    watch: {
      usePolling: true
    }
  },
});
