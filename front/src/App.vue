<script setup lang="ts">
import MyTest from "./components/MyTest.vue";
import axios from "axios";
import {ref} from "vue";

const txt = ref<string>("dummy2")
const clicked = () => {
  axios.get("/api/index.json").then(res => {
    console.log(res)
    txt.value = res.data
  })
}
</script>

<template>
  <nav>
    <ul>
      <li><a href="">home</a></li>
      <li><a href="http://localhost:8000/admin/">管理サイト</a></li>
      <li><a href="/api/index.json" @click.prevent="clicked">index.json</a></li>
    </ul>
  </nav>
  <div id="left"></div>
  <div v-if="txt !=='dummy2'" v-html="txt" style="width: 640px; height: 480px;"></div>
  <MyTest/>
  <!--  <HelloWorld msg="unti vue"/>-->
</template>

<style scoped>
nav ul {
    margin: 0;
    padding: 0;
    height: 40px;
    background-color: red;
}
#left{
  background-color: #3dbfb8;
  width: 100px;
}
</style>
