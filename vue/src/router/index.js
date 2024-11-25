import { createRouter, createWebHistory } from 'vue-router'
import ManageFields from '@/views/ManageFields.vue'

// Login
// ManageFields
// FieldRecord
// Import Records
// (optional) Manage Growers
// (optional) Manage Farms

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { 
      path: '/',
      name: 'manage',
      component: ManageFields
    },
  ],
})

export default router
