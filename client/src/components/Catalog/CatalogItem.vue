<template>
  <div class="catalog-item">
    <tiny-slider class="catalog-item-files-slider slider" :navAsThumbnails="true"
                 :navContainer="this.previews.length > 1 ? ('#custom-nav' + this.id) : false"
                 :controls="false" :nav="this.previews.length > 1" v-if="this.previews.length > 0">
      <div v-for="(item, index) in this.previews.slice(0, 5)" :key="index">
        <img :src="item.image" :alt="item.name" class="catalog-item-files-slider__item">
      </div>
    </tiny-slider>
    <ul class="slider-nav" :id="'custom-nav' + this.id" v-if="previews.length > 1">
      <li v-for="(item, index) in this.previews.slice(0, 5)" :key="index">
        <img :src="item.image" :alt="item.name" class="catalog-item-files-slider__item">
      </li>
    </ul>
    <p class="catalog-item__article grey" v-if="article.length > 0">
      Article: {{ this.article }}
    </p>
    <p class="catalog-item__title" @click="$emit('item-selected', id)">
      {{ this.title }}
    </p>
    <p class="catalog-item__description">
      {{ this.description }}
    </p>
    <button class="button--red catalog-item__button" @click="$emit('item-selected', id)">See more</button>
  </div>
</template>

<script>
import VueTinySlider from 'vue-tiny-slider';

export default {
  name: "CatalogItem",
  components: {
    'tiny-slider': VueTinySlider
  },
  props: {
    id: Number,
    images: Array,
    article: String,
    title: String,
    description: String,
    previews: Array,
  },
  data() {
    return {}
  }
}
</script>

<style lang="scss">
@import "../../styles/variables";

.catalog-item {
  display: block;
  border: 1px solid $main-lightgrey;
  padding: 20px;

  &__article {
    margin: 20px 0 0;
  }

  &__title {
    font-size: 20px;
    line-height: 1.5;
    font-weight: 500;
    margin-top: 20px;
    cursor: pointer;
  }

  &__description {
    margin-top: 17px;
  }

  &-files {
    &-slider {

    }
  }

  .slider-nav {
    display: flex !important;

    li {
      width: 19%;
      margin-right: 5px;
    }
  }

  &__button {
    display: block;
    margin-top: 40px;
    font-weight: 600;
    width: 170px;
    height: 38px;
  }
}
</style>
