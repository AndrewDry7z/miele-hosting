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
    padding-top: 40px;
    padding-bottom: 40px;
    border-top: 1px solid $main-lightgrey;

    @media screen and (max-width: 600px) {
      justify-content: space-between;
    }
  }

  &__immer-besser {
    margin-right: 45px;
    width: auto;

    @media screen and (max-width: 600px) {
      width: 75px;
      margin-right: 0;
    }
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
