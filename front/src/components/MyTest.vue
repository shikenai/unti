<script setup lang="ts">
import axios from "axios";
import {ref} from "vue";

const mytext = "helloworld"
const wei = ref('untitti')

console.log("test console")
let geta = ref()
axios.get("api/index.json").then(res => {
  console.log(res)
  console.log(res.data.user)
  geta.value = ref(res.data.user)
})
</script>


<template>
  <h1>testあああ</h1>
  <h6>{{ mytext }}</h6>
  <h4>{{ wei }}</h4>
  <h4>{{ geta }}</h4>
</template>


<style scoped>

</style>