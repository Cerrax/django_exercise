<!--
-== @class
SelectField.vue
-== Component for /<select> HTML tags.

-== **Props:**
@deflist
id: HTML /id attribute of the /<select>
name: HTML /name attribute of the /<select>
label: the string to display within the /<label> of the /<select>
disabled: a boolean which can disable the /<select> when true
v-model: the data which is used in the /value of the /<select>

-== @note
The /v-model expects the data to be a list of objects,
each with a /pk field which it can use to identify the objects.

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
