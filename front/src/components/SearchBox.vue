<script setup lang="ts">
import axios from "axios";
import {ref} from "vue";

let companies = ref({"keyword":"key","coms": <object>[]})
const get_brand = axios.get("api/get_brand_list.json").then(res=>{
  // console.log(res.data)
  // console.log(typeof res.data)
  companies.value.coms = res.data
})

// console.log(companies.value.keyword)
companies.value.keyword = "unti"
// companies.value.coms = {"unticom1": 1, "unticom2": 2}
console.log(companies.value.coms)
// console.log(companies.value.coms)
</script>
<template>
  <div class="left_bar">
    <input type="text" v-model="companies">
    <table>
            <tr v-for="c in companies">
              <td v-text="c.code"></td>
            </tr>
    </table>
  </div>
  <div class="drawing">

  </div>
</template>

<style scoped>
.left_bar {
  width: 150px;
  padding-top: 5px;
  border: solid black 1px;
  min-height: 800px;
}

.drawing {
  border: solid black 1px;
  min-height: 800px;
}

input {
  width: 130px;
}
</style>