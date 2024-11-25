<script setup>
import { RouterView } from 'vue-router'
import Login from '@/components/Login.vue'
</script>

<template>
  <RouterView v-if="$auth.authenticated" />
  <Login v-else />
</template>

<style scoped>
</style>
