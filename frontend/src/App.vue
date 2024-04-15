<script setup>
import axios from 'axios';
import { ref } from 'vue'
import WyButton from './components/wyButton.vue';

const filesList = ref([])
async function handleFileChange(event) {
  const files = event.target.files
  for (let i = 0; i < files.length; i++) {
    filesList.value.push({
      name: files[i].name,
      uploadProgress: 0,
      file: files[i]
    })
  }
  for (const item of filesList.value) {
    if (item.uploadProgress !== 0) continue
    const formData = new FormData()
    formData.append('file', item.file)
    const res = await axios({
      url: "/convert/jpg2png",
      method: "POST",
      data: formData,
      headers: {
        "Content-Type": "multipart/form-data",
      },
      onUploadProgress: (progressEvent) => {
        item.uploadProgress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
      }
    })
    item.uploadProgress = 101
    item.dataSource = "data:image/png;base64," + res.data.data
    console.log(res);
  }
}
</script>

<template>
  <div id="app">
    <input type="file" ref="file" style="display: none" multiple @change="handleFileChange">
    <span @click="$refs.file.click()">上传</span>
    <div class="file-list">
      <div v-for="file in filesList" class="file-list__item">
        <header class="file-list__header">
          <p>{{ file.name }}</p>
          <WyButton>close</WyButton>
        </header>
        <div class="file-list__mask">
          <p class="file-list__type">PNG</p>
          <div v-if="file.uploadProgress < 101">{{ ~~file.uploadProgress < 100 ? '上传中' : file.uploadProgress === 101
      ? '上传完成' : '转换中' }}</div>
              <img class="file-list__img" :src="file.dataSource" alt="图片">
          </div>
          <footer class="file-list__footer">
            <WyButton round="true">下载</WyButton>
          </footer>
        </div>
      </div>
    </div>
</template>

<style scoped lang="less">
p {
  margin: 0;
  padding: 0;
}

.file-list {
  display: flex;

  &__item {
    width: 196px;
    height: 196px;
    margin-right: 16px;
    position: relative;
    color: #fff;
  }

  &__header,
  &__mask,
  &__img {
    position: absolute;
    width: 100%;
    top: 0;
    left: 0;
  }

  &__mask {
    background-color: rgba(0, 0, 0, 0.2);
    height: 100%;
    z-index: 0;
    padding: 4px;
    box-sizing: border-box;
  }

  &__header {
    font-size: 12px;
    z-index: 1;
    padding: 4px;
  }

  &__footer {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    z-index: 1;
    padding: 4px;
  }

  &__type {
    font-size: 32px;
    letter-spacing: 4px;
    font-weight: bold;
  }

  &__img {
    height: 100%;
  }
}
</style>
