<script>

import Navbar from "@/components/Navbar.vue";

export default {
    name: '',
  components: {Navbar},
    data() {
        return {
        }
    }
}
</script>

<template>
  <div id="app">
    <Navbar></Navbar>
    <router-view />
  </div>
</template>

<style>
</style>