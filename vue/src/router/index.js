//-== @h2
// Router Configuration
//-== /src/router/index.js

//-== **Available Routes:**
// @deflist
// /fields: manage fields page ( /ManageFields.vue )
// /fields/create: create new field page ( /EditFieldRecord.vue )
// /fields/id: edit/delete field page ( /EditFieldRecord.vue )
// /fields/import: import CSV data ( /ImportRecords.vue )

import { createRouter, createWebHistory } from 'vue-router'
import ManageFields from '@/views/ManageFields.vue'
import EditFieldRecord from '@/views/EditFieldRecord.vue'
import ImportRecords from '@/views/ImportRecords.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { 
      alias: '/',
      path: '/fields',
      name: 'manage',
      component: ManageFields,
    },
    {
      path: '/fields/create',
      name: 'create',
      component: EditFieldRecord,
      props: { createMode: true },
    },
    {
      path: '/fields/:id',
      name: 'edit',
      component: EditFieldRecord,
    },
    {
      path: '/fields/import',
      name: 'import',
      component: ImportRecords,
    },
  ],
})

export default router
