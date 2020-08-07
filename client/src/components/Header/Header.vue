<template>
  <header class="header">
    <div class="container">
      <div class="header-logo">
        <router-link to="/">
          <Logo />
        </router-link>
      </div>
      <div class="header-right">
        <p @click="logout()">Logout</p>
      </div>
    </div>
  </header>
</template>

<script>
import Logo from "@/components/Logo/Logo";

export default {
  name: "Header",
  components: {Logo},
  methods: {
    logout() {
      this.$cookies.remove('mieletoken')
      this.$router.push('/auth/')
    }
  }
}
</script>

<style scoped lang="scss">
.header {
  margin-bottom: 50px;

  .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style>
