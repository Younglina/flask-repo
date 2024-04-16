<script setup>
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';
import { ref } from 'vue'
import WyButton from './components/wyButton.vue';

const tabs = [
  { label: 'JPG转PNG', value: 'jpg2png', covertType: 'png' },
  { label: 'PNG转JPG', value: 'png2jpg', covertType: 'jpg' },
  { label: 'PDF转JPG', value: 'pdf2jpg', covertType: 'jpg' },
  { label: 'PDF转PNG', value: 'pdf2png', covertType: 'png' },
]
const currnetTab = ref(tabs[0])
const uuid = ref(uuidv4())

const filesList = ref([])

async function handleFileChange(event) {
  const files = event.target.files || event.dataTransfer.files
  for (let i = 0; i < files.length; i++) {
    filesList.value.push({
      name: files[i].name,
      showname: files[i].name.length > 7 ? `${files[i].name.slice(0, 3)}...${files[i].name.slice(files[i].name.lastIndexOf('.') - 3)}` : files[i].name,
      uploadProgress: 0,
      file: files[i]
    })
  }
  for (const item of filesList.value) {
    if (item.uploadProgress !== 0) continue
    const formData = new FormData()
    formData.append('file', item.file)
    formData.append('uuid', uuid.value)
    const res = await axios({
      url: `/convert/${currnetTab.value.value}`,
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
  }
}
function handleTabChange(tab) {
  currnetTab.value = tab
  document.getElementById('inputFile').value = ''
  filesList.value = []
}
function handleDownload(file) {
  const base64Data = file.dataSource;
  const fileName = file.name.slice(0, file.name.lastIndexOf('.') + 1) + currnetTab.value.covertType;
  const link = document.createElement('a');
  link.href = base64Data;
  link.download = fileName;
  link.click();
}
function handleDrop(e) {
  e.preventDefault();
  handleFileChange(e)
}

function handleDragover(e) {
  e.preventDefault();
}

</script>

<template>
  <div id="app">
    <ul class="tabs">
      <li v-for="item in tabs" :key="item.value" @click="handleTabChange(item)"
        :class="{ 'active': currnetTab.value === item.value }">{{ item.label }}</li>
    </ul>

    <div class="file-wrapper">
      <input type="file" id="inputFile" ref="inputFile" style="display: none" multiple @change="handleFileChange">
      <div class="file-opts">
        <WyButton types="round" @click="$refs.inputFile.click()" color="blue">上传</WyButton>
        <WyButton types="round" @click="$refs.inputFile.click()" color="org">清空</WyButton>
      </div>
      <div class="file-list-wrapper">
        <div v-if="filesList.length === 0" class="file-drop" @dragover="handleDragover" @drop="handleDrop">
          <p>可拖拽文件上传</p>
        </div>
        <ul class="file-list">
          <li v-for="file in filesList" class="file-list__item">
            <header class="file-list__header">
              <p>{{ file.showname }}</p>
              <WyButton types="del">×</WyButton>
            </header>
            <div class="file-list__mask">
              <p class="file-list__type">PNG</p>
              <div v-if="file.uploadProgress < 101">{{ ~~file.uploadProgress < 100 ? '上传中' : file.uploadProgress === 101
        ? '上传完成' : '转换中' }}</div>
                  <img class="file-list__img" :src="file.dataSource" alt="图片">
              </div>
              <footer class="file-list__footer">
                <WyButton types="round" @click="handleDownload(file)">下载</WyButton>
              </footer>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style lang="less">
html,
body {
  height: 100%;
  margin: 0;
}

p,
ul,
li {
  margin: 0;
  padding: 0;
}

ul {
  list-style: none;
}

#app {
  height: 100%;
  width: 100%;
  max-width: 960px;
  margin: 0 auto;
}

.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

.tabs {
  display: flex;
  font-size: 12px;
  color: #000000;
  font-weight: 500;

  li {
    background-color: #bae6fd;
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
    padding: 4px 8px;
    margin-right: 4px;
    cursor: pointer;
  }

  li.active,
  li:hover {
    font-weight: 700;
    background-color: #e0f2fe;
    box-shadow: -6px -4px 8px -5px #bae6fd, 6px -4px 8px -5px #e0f2fe;
  }
}

.file-wrapper {
  box-shadow: 0px 2px 16px -2px #bae6fd;
  padding: 24px 12px;
}

.file-opts {
  .flex-center;

  button {
    margin-right: 8px;
  }
}

.file-drop {
  .flex-center;
  margin: 12px 0;
  height: 196px;
  color: #7dd3fc;
  font-weight: bold;
  border: 1px dashed currentColor;
  border-radius: 8px;
}

.file-list {
  display: flex;
  margin: 12px 0;
  height: 196px;

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
    .flex-center;
    background-color: rgba(0, 0, 0, 0.2);
    height: 100%;
    z-index: 0;
    box-sizing: border-box;
    border-radius: 12px;
  }

  &__img {
    filter: brightness(0.5);
    height: 100%;
    border-radius: 12px;
  }

  &__header {
    .flex-center;
    justify-content: space-between;
    font-size: 12px;
    z-index: 1;
    padding: 8px;
    box-sizing: border-box;
  }

  &__footer {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    z-index: 1;
    padding: 8px;
    box-sizing: border-box;
    text-align: center;
  }

  &__type {
    font-size: 42px;
    letter-spacing: 4px;
    font-weight: bold;
    z-index: 1;
  }

}
</style>
