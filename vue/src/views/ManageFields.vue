<!--
-== @class
ManageFields.vue
-== Page which has a list of field records,
as well as navigation to create field records and import from CSV.

-->

<script setup>
import { getCurrentInstance, useTemplateRef, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import { AgGridVue } from "ag-grid-vue3"; // Vue Data Grid Component

const { proxy } = getCurrentInstance()
const router = useRouter()

function logout() {
  // send data to server
  proxy.$auth.logout()
}

const defaultColDef = ref({
  sortable: true,
  filter: true,
  resizable: true,
  flex: 1,
})

function goToImport() {
  router.push({ name: 'import' })
}

function goToCreate() {
  router.push({ name: 'create' })
}

// Column Definitions: Defines the columns to be displayed.
const colDefs = ref([
  { field: "farm__grower__name", headerName: "Grower", sort: "asc" },
  { field: "farm__grower__street_addr", headerName: "Street Address" },
  { field: "farm__grower__city", headerName: "City" },
  { field: "farm__grower__state", headerName: "State" },
  { field: "farm__grower__zip_code", headerName: "Zip Code" },
  { field: "farm__grower__country", headerName: "Country" },
  { field: "farm__name", headerName: "Farm" },
  { field: "name", headerName: "Field Name" },
  { field: "area", headerName: "Area" },
])

// Row Data: The data to be displayed.
const rowData = ref([])

let getData = axios.get('manage/fields/', proxy.$auth.authHeaders)
  .then(response => {
    rowData.value = response.data
  })
  .catch(error => {
    console.log(error)
  })

function rowClicked(event) {
  let pk = event.data.pk
  console.log(`Clicked row ID ${pk}`)
  router.push({
    name: 'edit',
    params: { 'id': pk } 
  })
}
</script>
<template>
  <div class="manage">
    <div class="actionButtonBar">
      <button @click="goToImport()">Import Records</button>
      <button @click="goToCreate()">Add New Record</button>
      <div class="spacer"></div>
      <button @click="logout()">Log Out</button>
    </div>
    <h1>Manage Fields</h1>
    <ag-grid-vue
      ref="agGrid"
      :rowData="rowData"
      :columnDefs="colDefs"
      :defaultColDef="defaultColDef"
      domLayout="autoHeight"
      style="width: 100%; height: 500px"
      class="ag-theme-quartz"
      @row-clicked="rowClicked"
    >
    </ag-grid-vue>
  </div>
</template>

<style scoped>
.spacer {
  display: inline-block;
  width: 10vw;
}
</style>
