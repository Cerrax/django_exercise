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
  })

if (!props.createMode) {
  let getFieldRecord = axios.get(`manage/fields/${route.params.id}/`, proxy.$auth.authHeaders)
    .then(response => {
      fieldRecord.value = response.data
    })
    .catch(error => {
      console.log(error)
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
          console.log(error)
      })
  } else {
    await axios.patch(`/manage/fields/${route.params.id}/`, data, proxy.$auth.authHeaders)
      .then(response => {
          router.push({name: 'manage'})
      })
      .catch(error => {
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
        <!-- <SelectField id="grower" name="grower" label="Grower" :items="growerList" ref="selectGrower" /> -->
        <SelectField id="farm" name="farm" label="Farm" :items="farmList" ref="selectFarm" v-model="fieldRecord.farm.pk" />
        <InputField type="text" id="name" name="name" label="Field Name" ref="inputFieldName" v-model="fieldRecord.name" />
        <InputField type="number" id="area" name="area" label="Area (acres)" ref="inputFieldArea" v-model="fieldRecord.area" />
        <div class="actionButtonBar">
            <button @click="submitRecord()">Submit</button>
            <button @click="cancel()">Cancel</button>
            <div class="spacer"></div>
            <button @click="deleteRecord()">Delete</button>
        </div>
    </div>
</template>

<style scoped>
.spacer {
  display: inline-block;
  width: 10vw;
}
</style>