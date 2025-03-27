// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import compression from 'vite-plugin-compression'

export default defineConfig({
  base: '/',
  plugins: [
    vue(),
    compression({
      algorithm: 'gzip',
      ext: '.gz',
      deleteOriginFile: false // 保留原始文件
    })
  ],
  build: {
    assetsInlineLimit: 4096 // 小于4kb的资源自动转为base64
  }
})