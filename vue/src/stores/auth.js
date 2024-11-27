//-== @h2
// Authentication
//-== /src/stores/auth.js

import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  //-== @class
  // useAuthStore()
  //-== State store for user authentication.
  // @attributes
  // username: username of the currently logged in user or /null
  // authenticated: a boolean indicating if authentication succeeded
  // loginErrors: a list of errors when logging in fails
  // authHeaders: authentication config needed for API calls

  const username = ref("")
  const loginErrors = ref([])
  const authenticated = ref(false)
  const authHeaders = ref({ withCredentials: true })

  //-== @method
  async function login(username, password) {
    //-== Make an API call to authenicate a user.
    // If successful, the store is updated to reflect authentication.
    // If failed, the store populates /loginErrors with error messages from the server.

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

  //-== @method
  async function logout() {
    //-== Make an API call to log out a user.
    // Resets all authentication data in the store.

    await axios.get('core/logout/', this.authHeaders)
    this.username = ""
    this.authenticated = false
    this.authHeaders = {}
    this.loginErrors = []
  }

  return { username, authenticated, authHeaders, loginErrors, login, logout }
})