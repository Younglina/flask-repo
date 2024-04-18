<script setup>
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';
import { reactive, ref } from 'vue'
import WyButton from './components/wyButton.vue';
import message from './components/message.vue';

const tabs = [
  { label: 'JPG转PNG', value: 'jpg2png' },
  { label: 'PNG转JPG', value: 'png2jpg' },
  { label: 'PDF转JPG', value: 'pdf2jpg' },
  { label: 'PDF转PNG', value: 'pdf2png' },
]
const uuid = uuidv4()
const pageData = reactive({
  currnetTab: tabs[0],
  filesList: [],
  downloadCount: 0,
  showMessage: false,
  messageTxt: '',
})

const inputFile = ref()

async function handleFileChange(event) {
  let files = Array.from(event.target.files || event.dataTransfer.files)
  console.log(files);
  const fileLen = files.length
  let accetpType = pageData.currnetTab.value.split('2')[0]
  if (accetpType === 'jpg') {
    accetpType = ['jpg', 'jpeg']
  }
  files = files.filter(f => accetpType.includes(f.type.split('/')[1]))
  files.map(f => {
    pageData.filesList.push({
      name: f.name,
      showname: f.name.length > 7 ? `${f.name.slice(0, 3)}...${f.name.slice(f.name.lastIndexOf('.') - 3)}` : f.name,
      uploadProgress: 0,
      file: f
    })
  })
  if (fileLen !== files.length) {
    pageData.showMessage = true
    pageData.messageTxt = '已过滤不符合格式的文件'
  }
  for (const item of pageData.filesList) {
    if (item.uploadProgress !== 0) continue
    const formData = new FormData()
    formData.append('file', item.file)
    formData.append('uuid', uuid)
    try {
      const res = await axios({
        url: `/api/convert/${pageData.currnetTab.value}`,
        method: "POST",
        data: formData,
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (progressEvent) => {
          item.uploadProgress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        }
      })
      item.uploadProgress = 1000
      item.dataSource = "data:image/png;base64," + res.data.data
      downloadCount.value++
    } catch (e) {
      item.uploadProgress = 101
    } finally {
      inputFile.value.value = ''
    }
  }
}
function handleTabChange(tab) {
  if (tab) {
    pageData.currnetTab = tab
  }
  inputFile.value.value = ''
  pageData.filesList = []
}
function handleDownload(file) {
  const base64Data = file.dataSource;
  const fileName = file.name.slice(0, file.name.lastIndexOf('.') + 1) + pageData.currnetTab.value.split('2')[1];
  const link = document.createElement('a');
  link.href = base64Data;
  link.download = fileName;
  link.click();
}
function downloadAll() {
  axios({
    url: `/api/downloadAll/${pageData.currnetTab.value}`,
    method: "get",
    responseType: 'blob',
    params: uuid
  }).then(res => {
    const blob = new Blob([res.data], { type: 'application/zip' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${pageData.currnetTab.value}.zip`);
    link.click();
  })
}
function handleDel(file) {
  pageData.filesList = pageData.filesList.filter(item => item.name !== file.name)
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
  <div id="convert-app">
    <ul class="tabs">
      <li v-for="item in tabs" :key="item.value" @click="handleTabChange(item)"
        :class="{ 'active': pageData.currnetTab.value === item.value }">{{ item.label }}</li>
    </ul>

    <div class="file-wrapper">
      <input type="file" id="inputFile" ref="inputFile" style="display: none" multiple @change="handleFileChange">
      <div class="file-opts">
        <WyButton types="round" @click="$refs.inputFile.click()" color="blue">上传</WyButton>
        <WyButton types="round" @click="handleTabChange()" color="org">清空</WyButton>
      </div>
      <div class="file-list-wrapper">
        <div v-if="pageData.filesList.length === 0" class="file-drop" @dragover="handleDragover" @drop="handleDrop">
          <p>可拖拽文件上传</p>
        </div>
        <ul v-else class="file-list">
          <li v-for="file in pageData.filesList" class="file-list__item">
            <header class="file-list__header">
              <p>{{ file.showname }}</p>
              <WyButton types="del" @click="handleDel(file.name)">×</WyButton>
            </header>
            <div class="file-list__mask">
              <p v-if="file.dataSource" class="file-list__type">PNG</p>
              <div v-if="file.uploadProgress !== 1000">
                {{ ~~file.uploadProgress < 100 ? '上传中' : (file.uploadProgress === 101 ? '上传失败' : '转换中') }} </div>
                  <img v-if="file.dataSource" class="file-list__img" :src="file.dataSource" alt="图片">
              </div>
              <footer class="file-list__footer">
                <WyButton types="round" @click="handleDownload(file)">下载</WyButton>
              </footer>
          </li>
        </ul>
      </div>
      <div class="file-downloadall">
        <WyButton types="round" @click="downloadAll" color="gray" :disabled="pageData.filesList.length === 0">
          <span class="file-count">{{ pageData.downloadCount }}</span>
          <span>全部下载</span>
        </WyButton>
      </div>
    </div>
  </div>
  <message v-if="pageData.showMessage" @close="pageData.showMessage = false" :message="pageData.messageTxt" />
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

#convert-app {
  height: 100%;
  width: 100%;
  max-width: 960px;
  margin: 0 auto;
  padding: 49px 12px;
}

.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

.tabs {
  display: flex;
  font-size: 12px;
  color: var(--color-black);
  font-weight: 500;

  li {
    background-color: var(--color-blue-200);
    border: 1px solid var(--color-blue-50);
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
    padding: 4px 8px;
    margin-right: 4px;
    cursor: pointer;
  }

  li.active,
  li:hover {
    font-weight: 700;
    background-color: var(--color-blue-100);
    box-shadow: 0px -4px 14px -5px var(--color-blue-100);
  }
}

.file-wrapper {
  box-shadow: 0px 5px 16px -2px var(--color-blue-200);
  border: 1px solid var(--color-blue-50);
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
  color: var(--color-blue);
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
    color: var(--color-white);
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

.file-downloadall {
  text-align: center;

  .btn {
    position: relative;
  }

  .file-count {
    position: absolute;
    top: -7px;
    right: -7px;
    border: 2px solid var(--color-white);
    border-radius: 50%;
    width: 16px;
    height: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    background-color: var(--color-gray);
    color: var(--color-white);
  }
}
</style>
