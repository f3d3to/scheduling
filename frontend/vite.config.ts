import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify';
import { fileURLToPath, URL } from 'url';

export default defineConfig({
  plugins: [
    vue(),
    vuetify({ autoImport: true }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '@components': fileURLToPath(new URL('./src/components', import.meta.url)),
      '@common': fileURLToPath(new URL('./src/components/common', import.meta.url)),
      '@layout': fileURLToPath(new URL('./src/components/layout', import.meta.url)),
      '@views': fileURLToPath(new URL('./src/components/views', import.meta.url)),
      '@cruds': fileURLToPath(new URL('./src/components/views/cruds', import.meta.url)),
      '@dashboards': fileURLToPath(new URL('./src/components/views/dashboards', import.meta.url)),
      '@forms': fileURLToPath(new URL('./src/components/forms', import.meta.url)),
      '@planes': fileURLToPath(new URL('./src/components/views/planes', import.meta.url)),
      '@planificador': fileURLToPath(new URL('./src/components/views/planificador', import.meta.url)),
      '@planificadorDetalle': fileURLToPath(new URL('./src/components/views/planificador/detalles', import.meta.url)),
      '@timer': fileURLToPath(new URL('./src/components/views/timer', import.meta.url)),
      '@router': fileURLToPath(new URL('./src/router', import.meta.url)),
      '@services': fileURLToPath(new URL('./src/services', import.meta.url)),
      '@plugins': fileURLToPath(new URL('./src/plugins', import.meta.url)),
      '@composables': fileURLToPath(new URL('./src/composables', import.meta.url)),
      '@store': fileURLToPath(new URL('./src/store', import.meta.url)),
    },
  },
  optimizeDeps: {
    include: ['d3'],
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
    watch: {
      usePolling: true,
    },
  },
});