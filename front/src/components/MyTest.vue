<template>
  <h1>testあああ</h1>
</template>

<script setup lang="ts">
import axios from "axios";

window.onload = () => {
  console.log("test console")
  axios.get("api/index.json").then(res => {
    console.log(res)
    console.log(res.data.user)
    const testname = res.data.user
  })
}
</script>

<style scoped>

</style>