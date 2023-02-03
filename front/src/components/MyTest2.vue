<script setup lang="ts">
import axios from "axios";
import {ref} from "vue";
let companies = ref()
axios.get("api/index.json")
</script>
<template>

</template>

<style scoped>

</style>