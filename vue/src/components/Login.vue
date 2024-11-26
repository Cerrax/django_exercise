<script setup>
import InputField from '@/components/InputField.vue'
import { getCurrentInstance, useTemplateRef, ref } from 'vue'

const { proxy } = getCurrentInstance()
const inputUser = useTemplateRef('inputUser')
const inputPass = useTemplateRef('inputPass')

function attemptLogin() {
  // send data to server
  proxy.$auth.login(inputUser.value.value, inputPass.value.value)
}
</script>

<template>
  <div class="login">
    <h1 class="centeredFlex"><img id="splashLogo" src="@/assets/logo_w_name.png"/>Login</h1>
    <InputField type="text" id="username" name="username" label="Username" ref="inputUser" />
    <InputField type="password" id="password" name="password" label="Password" ref="inputPass" />
    <button @click="attemptLogin()">Submit</button>
  </div>
</template>

<style scoped>
#splashLogo {
  height: 4rem;
}

.centeredFlex {
  display:flex;
  align-items: center;
}
</style>
