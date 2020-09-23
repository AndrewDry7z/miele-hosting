<template>
  <div id="app">
    <Header v-if="hasToken" />
    <router-view />
    <Footer v-if="hasToken" />
  </div>
</template>

<script>
import Header from "./components/Header/Header"
import Footer from "@/components/Footer/Footer"
import store from '@/store'

export default {
  data() {
    return {
      hasToken: this.$cookies.isKey('mieletoken'),
      token: this.$cookies.get('mieletoken')
    }
  },
  methods: {
    redirectToAuthPage() {
      if ((!this.hasToken) && (this.$router.currentRoute.name !== 'Auth')) {
        this.$router.push('/auth/')
      }
    },
    getData() {
      if (this.hasToken) {
        store.commit('setCatalog', this.token)
        store.commit('setTagsList', this.token)
      }
    }
  },
  components: {Footer, Header},
  beforeUpdate() {
    this.hasToken = this.$cookies.isKey('mieletoken')
  },
  created() {
    this.redirectToAuthPage()
    this.getData()
  },
  watch: {
    '$route'(to, from) {
      if ((to !== from) && (this.hasToken) && (to !== '/auth/')) {
        store.commit('setCatalog', this.token)
      }
    }
  }
}
</script>
