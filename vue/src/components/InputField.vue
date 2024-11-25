<script setup>
import { ref } from 'vue'

defineProps({
  id: {
    type: String,
    required: true,
  },
  name: {
    type: String,
    required: true,
  },
  type: {
    type: String,
    required: true,
  },
  label: {
    type: String,
    required: false,
  },
})

const value = ref("")

defineExpose({
  value,
})
</script>

<template>
  <div class="input-field">
    <label v-if="label" :for="id" >{{ label }}</label>
    <input :type="type" :id="id" :name="name" v-model="value" />
  </div>
</template>

<style scoped>
</style>
