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
  font-weight: bold;
  color: var(--color-black);
  background-color: var(--color-white);
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
  color: var(--color-white);
  background-color: var(--color-blue);
  border: 1px solid var(--color-blue);

  &:hover {
    color: var(--color-blue);
  }
}

.org {
  color: var(--color-white);
  background-color: var(--color-org);
  border: 1px solid var(--color-org);

  &:hover {
    color: var(--color-org);
  }
}

.gray {
  color: var(--color-white);
  background-color: var(--color-gray);
  border: 1px solid var(--color-gray);

  &:hover {
    color: var(--color-gray);
  }
}
</style>