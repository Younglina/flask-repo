<script setup>
import { v4 as uuidv4 } from 'uuid';
import { ref, onMounted } from 'vue'
import WyButton from './wyButton.vue';

const props = defineProps({
  message: {
    type: String,
    default: 'message'
  }
})
const emit = defineEmits(['close'])
const id = ref('')
let removeFun = null
onMounted(() => {
  id.value = uuidv4()
  startTimer()
})

function startTimer(ms = 3000) {
  clearTimeout(removeFun)
  removeFun = setTimeout(() => {
    const message = document.getElementById(id.value)
    if (message) {
      message.remove()
      emit('close')
    }
  }, ms)
}

function clearTimer() {
  clearTimeout(removeFun)
}
</script>
<template>
  <Teleport to="body">
    <div :id="id" class="message-wrapper" @mouseenter="clearTimer" @mouseleave="startTimer(3000)">
      <div class="message">
        <p>{{ message }}</p>
        <WyButton types="del" @click="startTimer(0)">×</WyButton>
      </div>
    </div>
  </Teleport>
</template>
<style scoped lang='less'>
.message-wrapper {
  position: absolute;
  z-index: 999;
  top: -24px;
  left: 50%;
  transform: translateX(-50%);
  animation: slideDown 0.5s forwards;

  .message {
    color: var(--color-black);
    background-color: var(--color-white);
    border: 1px solid var(--color-blue-200);
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 12px;
    font-weight: 500;
    display: flex;
    align-items: center;
    justify-content: space-between;

    >p {
      margin-right: 20px;
    }
  }
}

@keyframes slideDown {
  0% {
    top: -24px;
    opacity: 0;
  }

  100% {
    top: 24px;
    opacity: 1;
  }
}
</style>