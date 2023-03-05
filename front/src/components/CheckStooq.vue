<script setup lang="ts">
import axios from "axios";
import {ref} from "vue";

const mytext = "helloworld"
const wei = ref('untitti')

console.log("test console")
let geta = ref([])

const check_stooq = () => {
  axios.get('api/check_stooq').then(res => {
  })
}
</script>


<template>
  <a href="" @click.prevent="check_stooq">check stooq</a>
</template>


<style scoped>

</style>