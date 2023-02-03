<script setup lang="ts">
import HelloWorld from './components/HelloWorld.vue'
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
      <li><a href="http://localhost:8000/admin/">管理サイト</a></li>
      <li><a href="/api/index.json" @click.prevent="clicked">index.json</a></li>
    </ul>
  </nav>
  <div v-html="txt" style="width: 640px; height: 480px;"></div>
  <MyTest/>
  <HelloWorld msg="unti vue"/>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
