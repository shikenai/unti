<script setup lang="ts">
const unti = () => {
  console.log('untitititi')
}
</script>
<template>
  <div class="main">
    <div class="left_bar">
    <a href="" class="btn" @click="unti">Button</a>
    </div>
    <div class="drawing">
    </div>
  </div>
</template>

<style scoped>

.main {
  display: flex;
}

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
</style>