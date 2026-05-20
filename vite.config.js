import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  return {
    plugins: [react()],
    server: {
      proxy: {
        '/api/lava': {
          target: 'https://api.lava.so/v1',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api\/lava/, ''),
          headers: {
            'Authorization': `Bearer ${env.LAVA_API_KEY}`,
          },
        },
      },
    },
  }
})
