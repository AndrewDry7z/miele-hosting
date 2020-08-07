<template>
  <footer class="footer">
    <div class="container">
      <img
          src="~@/assets/images/immer-besser.png"
          srcset="~@/assets/images/immer-besser@2x.png 2x"
          loading="lazy"
          alt="Immer Besser"
          class="footer__immer-besser"
      >
      <p class="footer__text">
        System support: <a href="mailto:digital@miele.ru">digital@miele.ru</a>
      </p>
    </div>

  </footer>
</template>

<script>
export default {
  name: "Footer"
}
</script>

<style scoped lang="scss">
@import "../../styles/variables";

.footer {
  margin-top: 40px;

  .container {
    display: flex;
    align-items: center;
    padding: 40px 0;
    border-top: 1px solid $main-lightgrey;
  }

  &__immer-besser {
    margin-right: 45px;
    width: fit-content;
  }

  &__text {
    color: #939598;

    a {
      color: inherit;
      text-decoration: none;
    }
  }
}
</style>
