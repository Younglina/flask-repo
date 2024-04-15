<!--
 * @Author: Younglina younglina0409@outlook.com
 * @Date: 2024-04-15 17:00:46
 * @Description: 
-->
<script setup>
const props = defineProps({
  round: false,
})
const classs = `btn ${props.round ? 'btn-round' : ''}`
</script>
<template>
  <button :class="classs">
    <slot></slot>
  </button>
</template>
<style scoped lang='less'>
button {
  border: none;
  background-color: #fff;
  border-radius: 4px;
  cursor: pointer;
  padding: 2px;

  &:hover {
    background-color: rgba(255, 255, 255, 0.5);
  }
}

.btn-round {
  width: 100%;
  padding: 8px;
}
</style>