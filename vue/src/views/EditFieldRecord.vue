<!--
-== @class
EditFieldRecord.vue
-== Page which provides inputs to
view, create, edit, and delete field records.

-== **Props:**
@deflist
createMode: a boolean indicating if the form is for creating a new record,
            or editing/deleting an existing record

-->

<script setup>
import InputField from '@/components/InputField.vue'
import SelectField from '@/components/SelectField.vue'
import { getCurrentInstance, useTemplateRef, ref } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()

const props = defineProps({
  createMode: {
    type: Boolean,
    default: false
  },
})

const { proxy } = getCurrentInstance()
const errors = ref([])
const farmList = ref([])
const fieldRecord = ref({
  pk: null,
  version: null,
  name: "",
  area: 0.0,
  farm: {pk: null},
})

let getFarms = axios.get('manage/farms/', proxy.$auth.authHeaders)
  .then(response => {
    farmList.value = response.data
  })
  .catch(error => {
    console.log(error)
    errors.value = ["Unable to retrieve the list of farms."]
  })

if (!props.createMode) {
  let getFieldRecord = axios.get(`manage/fields/${route.params.id}/`, proxy.$auth.authHeaders)
    .then(response => {
      fieldRecord.value = response.data
    })
    .catch(error => {
      console.log(error)
      errors.value = ["Unable to retrieve field record."]
    })
}

async function submitRecord() {
  let data = {
    pk: fieldRecord.value.pk,
    version: fieldRecord.value.version,
    name: fieldRecord.value.name,
    area: fieldRecord.value.area,
    farm_id: fieldRecord.value.farm.pk,
  }
  if (props.createMode) {
    await axios.post('/manage/fields/', data, proxy.$auth.authHeaders)
    .then(response => {
          router.push({name: 'manage'})
      })
      .catch(error => {
          errors.value = error.response.data
          console.log(error)
      })
  } else {
    await axios.patch(`/manage/fields/${route.params.id}/`, data, proxy.$auth.authHeaders)
      .then(response => {
          router.push({name: 'manage'})
      })
      .catch(error => {
          errors.value = error.response.data
          console.log(error)
      })
  }
}

async function deleteRecord() {
  await axios.delete(`manage/fields/${route.params.id}/`, proxy.$auth.authHeaders)
    .then(response => {
        router.push({name: 'manage'})
    })
    .catch(error => {
        console.log(error)
    })
}

function cancel() {
  router.push({name: 'manage'})
}
</script>

<template>
    <div class="edit">
        <h1 v-if="props.createMode">New Field Record</h1>
        <h1 v-else>Edit Field Record</h1>
        <div v-if="errors.length > 0">
            <div class="errorBox">
            <div v-for="(err, index) in errors" :key="'err' + index">{{ err }}</div>
          </div>
        </div>
        <!-- <SelectField id="grower" name="grower" label="Grower" :items="growerList" ref="selectGrower" /> -->
        <SelectField id="farm" name="farm" label="Farm" :items="farmList" ref="selectFarm" v-model="fieldRecord.farm.pk" />
        <InputField type="text" id="name" name="name" label="Field Name" ref="inputFieldName" v-model="fieldRecord.name" />
        <InputField type="number" id="area" name="area" label="Area (acres)" ref="inputFieldArea" v-model="fieldRecord.area" />
        <div class="actionButtonBar">
            <button @click="submitRecord()">Submit</button>
            <button @click="cancel()">Cancel</button>
            <div class="spacer"></div>
            <button @click="deleteRecord()" v-if="!props.createMode">Delete</button>
        </div>
    </div>
</template>

<style scoped>
.spacer {
  display: inline-block;
  width: 10vw;
}
</style>