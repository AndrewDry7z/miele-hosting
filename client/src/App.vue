<template>
  <div id="app">
    <Header v-if="hasToken" />
    <router-view />
    <Footer v-if="hasToken" />
  </div>
</template>

<style lang="scss">
</style>
<script>
import Header from "./components/Header/Header";
import Footer from "@/components/Footer/Footer";

export default {
  data() {
    return {
      hasToken: this.$cookies.isKey('mieletoken')
    }
  },
  components: {Footer, Header},
  beforeUpdate() {
    this.hasToken = this.$cookies.isKey('mieletoken')
  }
}
</script>
