<!--
-== @class
ImportRecords.vue
-== Page which allows a user to import CSV data into the application.

-->

<script setup>
import { getCurrentInstance, useTemplateRef, ref } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()

const { proxy } = getCurrentInstance()
const errors = ref([])
const fileReady = ref(false)
const importFile = useTemplateRef('inputImportFile')
const importData = ref("")

async function prepareFile() {
  const curFiles = importFile.value.files;
  // check if we have 1 file selected
  // validate that it is a CSV
  // read the data from the file
  const file = curFiles.item(0)
  importData.value = await file.text()
  fileReady.value = true
}

async function sendImportData() {
  await axios.post('/manage/import/', importData.value, proxy.$auth.authHeaders)
    .then(response => {
        let data = response.data
        if (data.errors.length > 0) {
          errors.value = [`${data.records_processed} of ${data.records_read} records processed.`]
          errors.value = errors.value.concat(response.data.errors)
        } else {
          router.push({name: 'manage'})
        }
      })
      .catch(error => {
          errors.value = error.response.data
          console.log(error)
      })
}

function cancel() {
  router.push({name: 'manage'})
}
</script>

<template>
  <div class="import">
    <h1>Import Data</h1>
    <div v-if="errors.length > 0">
      <div class="errorBox">
        <div v-for="(err, index) in errors" :key="'err' + index">{{ err }}</div>
      </div>
    </div>
    <div>
      <label for="importFile">CSV File:</label>
      <input type="file"
        id="importFile" name="importFile"
        accept=".csv"
        @input="prepareFile()"
        ref="inputImportFile" />
    </div>
    <div>
      <button :disabled="!fileReady" @click="sendImportData()">Import File</button>
      <button @click="cancel()">Cancel</button>
    </div>
    
  </div>
</template>

<style scoped>
</style>