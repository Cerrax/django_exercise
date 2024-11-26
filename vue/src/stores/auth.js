import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const username = ref("")
  const loginErrors = ref([])
  const authenticated = ref(false)
  const authHeaders = ref({ withCredentials: true })

  async function login(username, password) {
    let data = { 
      username: username, 
      password: password 
    }
    await axios.post('core/login/', data, this.authHeaders)
    .then(response => {
      this.username = username
      this.authenticated = true
      let cookieValue = null
      let csrfToken = null;
      if (document.cookie && document.cookie !== '') {
        cookieValue = document.cookie
        const cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim()
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, 10) === ('csrftoken=')) {
            csrfToken = decodeURIComponent(cookie.substring(10));
            break;
          }
        }
      }
      this.authHeaders = {
        headers: {
          'X-CSRFToken': csrfToken,
        },
      }
      this.loginErrors = []
    })
    .catch(error => {
      this.username = ""
      this.authenticated = false
      this.authHeaders = {}
      console.log(error)
      this.loginErrors = error.response.data
    })
  }

  async function logout() {
    await axios.get('core/logout/', this.authHeaders)
    this.username = ""
    this.authenticated = false
    this.authHeaders = {}
    this.loginErrors = []
  }

  return { username, authenticated, authHeaders, login, logout }
})