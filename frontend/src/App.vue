<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const imageUrl = ref('')
const loading = ref(false)
const ocrResult = ref(null)
const hideText = ref(false)

const handleUpload = (file) => {
  const reader = new FileReader()
  reader.onload = async (e) => {
    const base64 = e.target.result.split(',')[1]
    imageUrl.value = e.target.result
    loading.value = true
    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/ocr`, {
        image: base64
      })
      ocrResult.value = response.data.result
      if(response.data.result.ocr_response?.length){
        ElMessage.success('识别成功')
      }else{
        ElMessage.error('未识别到文字')
      }
    } catch (error) {
      ElMessage.error('识别失败：' + error.message)
    } finally {
      loading.value = false
    }
  }
  console.log(file);
  
  reader.readAsDataURL(file.raw)
  return false
}
</script>

<template>
  <div class="container">
    <div class="upload-section">
      <el-upload
        class="upload-box"
        drag
        action=""
        :auto-upload="false"
        :show-file-list="false"
        :on-change="handleUpload"
      >
        <div class="upload-content">
          <el-icon class="upload-icon"><upload-filled /></el-icon>
          <div class="upload-text">拖拽图片或点击上传 文字OCR识别</div>
        </div>
      </el-upload>
    </div>

    <div v-if="imageUrl" class="preview-section">
      <el-button
      class="toggle-button"
      type="default"
      circle
      @click="hideText = !hideText"
    >
      <el-icon><Hide v-if="hideText" /><View v-else /></el-icon>
    </el-button>
      <div class="image-container">
        <img :src="imageUrl" class="preview-image" />
        <div v-if="ocrResult && ocrResult.ocr_response" class="text-overlay">
          <div
            v-for="(item, index) in ocrResult.ocr_response"
            :key="index"
            class="text-box"
            :style="{
              left: (item.left / ocrResult.width) * 100 + '%',
              top: (item.top / ocrResult.height) * 100 + '%',
              width: ((item.right - item.left) / ocrResult.width) * 100 + '%',
              height: ((item.bottom - item.top) / ocrResult.height) * 100 + '%'
            }"
          >
            <div class="text-content" :class="{ 'box-hidden': hideText }">
              <span class="text">{{ item.text }}</span>
              <span class="confidence">置信度: {{ (item.rate * 100).toFixed(2) }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <el-loading v-model="loading" fullscreen />
  </div>
</template>

<style scoped>
.container {
  position: relative;
  min-width: 600px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
}

.toggle-button {
  position: absolute;
  top: 10px;
  right: -42px;
  z-index: 10;
}
.upload-section {
  margin-bottom: 20px;
}

.upload-box {
  border: 2px dashed #409EFF;
  border-radius: 12px;
  background: rgba(64, 158, 255, 0.1);
  transition: all 0.3s;
}

.upload-box:hover {
  border-color: #79bbff;
  box-shadow: 0 0 20px rgba(64, 158, 255, 0.3);
}

.upload-content {
  padding: 40px 0;
  text-align: center;
  color: #409EFF;
}

.upload-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.upload-text {
  font-size: 16px;
}

.preview-section {
  position: relative;
  margin-top: 20px;
}

.image-container {
  position: relative;
  /* border-radius: 12px; */
  /* overflow: hidden; */
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.3);
}

.preview-image {
  width: 100%;
  display: block;
  border-radius: 12px;
}

.text-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.text-box {
  position: absolute;
  border: 2px solid #409EFF;
  background: rgba(64, 158, 255, 0.2);
  border-radius: 4px;
  padding: 4px;
  transition: all 0.3s;
  opacity: 1;
}

.text-box:hover {
  transform: scale(1.02);
}

.text-content {
  position: absolute;
  bottom: 100%;
  left: 0;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
  white-space: nowrap;
  display: flex;
  flex-direction: column;
  gap: 2px;
  pointer-events: none;
}

.text-box:hover .text-content {
  opacity: 1;
  transition: opacity 0.3s;
}

.toggle-button {
  margin-bottom: 16px;
}

.confidence {
  font-size: 12px;
  color: #909399;
}

.box-hidden {
  opacity: 0;
  transition: opacity 0.3s;
}
.box-delete {
  display: none;
}

.el-button:focus{
  outline: none;
}
</style>
