<template>
  <aside class="overlay">
    <div class="lightbox">
      <span class="lightbox__close" @click="$emit('close-lightbox')"></span>
      <img class="lightbox__image" :src="this.image" alt="">
    </div>
  </aside>
</template>

<script>
export default {
  name: "Lightbox",
  props: {
    image: String
  }
}
</script>

<style scoped lang="scss">
@import "~@/styles/_variables.scss";

.overlay {
  display: flex;
  align-items: center;
  justify-content: center;
}

.lightbox {
  position: relative;
  max-width: 90%;
  max-height: 90vh;

  &__image {
    max-height: 88vh;
    width: auto;
  }

  &__close {
    position: absolute;
    right: -30px;
    top: -30px;
    line-height: 1;
    cursor: pointer;

    &:before {
      content: '\2715';
      color: #ff503e;
      font-size: 36px;
      text-shadow: 0 0 1px #000;
    }
  }
}
</style>
