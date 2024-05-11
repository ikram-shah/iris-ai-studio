<template>
  <div id="app">
    <NavigationBar />
    <router-view />
  </div>
</template>

<script setup>
import NavigationBar from "./components/NavigationBar.vue";
</script>

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
