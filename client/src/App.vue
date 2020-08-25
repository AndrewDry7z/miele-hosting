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
import Header from "./components/Header/Header"
import Footer from "@/components/Footer/Footer"
import store from '@/store'

export default {
  data() {
    return {
      hasToken: this.$cookies.isKey('mieletoken')
    }
  },
  methods: {
    redirectToAuthPage() {
      if (!this.hasToken) {
        this.$router.push('/auth/')
      } else {

      }
    }
  },
  components: {Footer, Header},
  beforeUpdate() {
    this.hasToken = this.$cookies.isKey('mieletoken')
  },
  created() {
    this.redirectToAuthPage()
    store.commit('setCatalog', this.$cookies.get('mieletoken'))
  }
}
</script>
