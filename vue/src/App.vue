<!--
-== @class
App
-== Main entrypoint component for the Vue3 web application.

-== This application has the following global properties available:
 @deflist
 $auth: the Authentication store ( /useAuthStore )
-->
<script setup>
import { RouterView } from 'vue-router'
import Login from '@/views/Login.vue'
</script>

<template>
  <RouterView v-if="$auth.authenticated" />
  <Login v-else />
</template>

<style scoped>
</style>
