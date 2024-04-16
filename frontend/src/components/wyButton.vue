<!--
 * @Author: Younglina younglina0409@outlook.com
 * @Date: 2024-04-15 17:00:46
 * @Description: 
-->
<script setup>
const props = defineProps({
  types: {
    type: String,
    default: ''
  },
  color: {
    type: String,
    default: '',
  },
  disabled: {
    type: Boolean,
    default: false
  }
})
const classs = `btn ${props.types} ${props.color}`
</script>
<template>
  <button :class="classs" :disabled="disabled">
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
    background-color: rgba(255, 255, 255, 0.7);
  }
}

.round {
  width: 100%;
  max-width: 149px;
  padding: 6px 8px;
}

.del {
  border-radius: 50%;
  font-size: 20px;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.blue {
  color: #fff;
  background-color: #38bdf8;
  border: 1px solid #38bdf8;

  &:hover {
    color: #38bdf8;
  }
}

.org {
  color: #fff;
  background-color: #fb923c;
  border: 1px solid #fb923c;

  &:hover {
    color: #fb923c;
  }
}
</style>