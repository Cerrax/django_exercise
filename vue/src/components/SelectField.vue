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
  label: {
    type: String,
    required: false,
  },
  disabled: {
    type: Boolean,
    default: false
  },
  items: {
	default: []
  },
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
    <select :id="id" :name="name" v-model="value">
		<option disabled value="">---</option>
		<option v-for="item in items" :key="item.pk" :value="item.pk">
			{{ item.name }}
		</option>
	</select>
  </div>
</template>

<style scoped>
</style>
