import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      '/api': {//获取路径中包含了api的请求
        target: 'http://127.0.0.1:8080',//游学计划

        // target: 'http://127.0.0.1:4523/m1/4475535-4122005-default',//我的
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')//将路径中的api替换为空
      }
    }
  }
})
