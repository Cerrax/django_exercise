import '@/assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'
import VueAxios from 'vue-axios'

import App from '@/App.vue'
import router from '@/router'

import { useAuthStore } from "@/stores/auth"

const app = createApp(App)

app.use(createPinia())
app.config.globalProperties.$auth = useAuthStore() // Make the store globally accessible

app.use(router)

app.use(VueAxios, axios)
axios.defaults.withCredentials = true
axios.defaults.baseURL = 'http://localhost:8000/'

app.mount('#app')
