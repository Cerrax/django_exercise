<!--
-== @class
InputField.vue
-== Component for /<input> HTML tags.

-== **Props:**
@deflist
id: HTML /id attribute of the /<input>
name: HTML /name attribute of the /<input>
type: HTML /type attribute of the /<input>
label: the string to display within the /<label> of the /<input>
disabled: a boolean which can disable the /<input> when true
v-model: the data which is used in the /value of the /<input>

-->

<script setup>
import { ref } from 'vue'

const props = defineProps({
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
  disabled: {
    type: Boolean,
    default: false
  }
})

const value = defineModel()
const isDisabled = ref(props.disabled)

defineExpose({
  value,
  isDisabled,
})
</script>

<template>
  <div class="input-field">
    <label v-if="label" :for="id" >{{ label }}: </label>
    <input :type="type" :id="id" :name="name" v-model="value" :disabled="isDisabled"/>
  </div>
</template>

<style scoped>
</style>
