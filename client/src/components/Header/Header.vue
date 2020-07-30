<template>
  <header class="header">
    <div class="container">
      <div class="header-logo">
        <router-link to="/">
          <Logo />
        </router-link>
      </div>
    </div>
  </header>
</template>

<script>
import Logo from "@/components/Logo/Logo";

export default {
  name: "Header",
  components: {Logo}
}
</script>

<style scoped>

</style>
