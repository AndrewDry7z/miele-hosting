<template>
  <div class="overlay" v-if="this.item" @click="$emit('overlay-click', $event)">
    <aside class="catalog-details">
      <button class="catalog-details__close" @click="$emit('close-details')" />
      <router-link to="/">
        <Logo class="catalog-details__logo" />
      </router-link>
      <div class="catalog-details-content">
        <p class="catalog-details__article grey" v-if="this.item.article.length > 0">
          Article: {{ this.item.article }}
        </p>
        <p class="catalog-details__title">
          {{ this.item.title }}
        </p>
        <p class="catalog-details__description">
          {{ this.item.description }}
        </p>
        <div class="catalog-details-tags">
          <span class="catalog-details-tags__item"
                v-for="tag of this.item.tags"
                :key="tag.id">
            {{ tag.name }}
          </span>
        </div>
      </div>
    </aside>
  </div>
</template>

<script>
import Logo from "@/components/Logo/Logo";

export default {
  components: {Logo},
  props: {
    item: Object
  },
  name: "CatalogDetails"
}
</script>

<style scoped lang="scss">
.overlay {
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  background: rgba(30, 30, 30, 0.8);
}

.catalog-details {
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  height: 100%;
  top: 0;
  right: 0;
  width: 63%;
  background: #ffffff;
  padding: 0 100px;


  &__close {
    position: absolute;
    right: 30px;
    top: 10px;

    &:before {
      content: '\2715';
      font-size: 30px;
      color: #bdbdbd;
    }
  }

  &__logo {
    height: fit-content;
    width: fit-content;
    position: absolute;
    left: 100px;
    top: 0;
  }

  &-content {
    width: 100%;
  }

  &__article {
    font-size: 13px;
  }

  &__title {
    font-size: 28px;
    font-weight: 600;
    margin: 20px 0 25px;
  }

  &-tags {
    margin-top: 30px;

    &__item {
      display: inline-block;
      padding: 7px;
      border: 0.75px solid #E9E9E9;
      box-sizing: border-box;
      border-radius: 4px;
      margin-right: 10px;
      cursor: pointer;
    }
  }
}
</style>
