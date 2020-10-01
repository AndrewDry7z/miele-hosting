<template>
  <div class="catalog-item">
    <div class="catalog-item-icons" v-if="$route.name === 'Profile' && this.ownItem">
      <router-link class="catalog-item-icons__item edit" :to="`/edit/${this.id}/`"></router-link>
      <button class="catalog-item-icons__item delete" @click="$emit('delete-item', id)"></button>
    </div>
    <tiny-slider class="catalog-item-files-slider slider" :navAsThumbnails="true"
                 :navContainer="this.previews.length > 1 ? ('#custom-nav' + this.id) : false"
                 :controls="false" :autoHeight="true" :nav="this.previews.length > 1" v-if="this.previews.length > 0">
      <div v-for="(item, index) in this.previews.slice(0, 5)" :key="index" @click="$emit('show-lightbox', item.image)">
        <img :src="item.image" :alt="item.name" class="catalog-item-files-slider__item" loading="lazy">
      </div>
    </tiny-slider>
    <ul class="slider-nav" :id="'custom-nav' + this.id" v-if="previews.length > 1">
      <li v-for="(item, index) in this.previews.slice(0, 5)" :key="index">
        <img :src="item.image" :alt="item.name" class="catalog-item-files-slider__item" loading="lazy">
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
    <button class="catalog-item__button button--red" @click="$emit('item-selected', id)">
      See more
    </button>
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
    ownItem: Boolean
  },
  data() {
    return {
      token: this.$cookies.get('mieletoken'),
      itemToDelete: null,
      showDeleteMessage: true,
      screenWidth: screen.width
    }
  }
}
</script>

<style lang="scss">
@import "../../styles/variables";

.catalog-item {
  display: block;
  border: 1px solid $main-lightgrey;
  padding: 20px;
  position: relative;
  @media screen and (max-width: 600px) {
    content-visibility: auto
  }

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
      .tns-slide-active {
        margin-right: 10px;
        margin-left: -5px;
        height: 250px;
        cursor: zoom-in;
      }

      .catalog-item-files-slider__item {
        height: 250px;
        object-fit: cover;
      }
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
    display: flex!important;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    margin-top: 40px;
    font-weight: 600;
    width: 170px;
    height: 38px;
  }

  &-icons {
    position: absolute;
    right: 0;
    top: 0;
    z-index: 5;

    &__item {
      display: flex;
      align-items: center;
      justify-content: center;
      background: $main-lightgrey;
      border: 8px solid #FFFFFF;
      border-radius: 50%;
      width: 40px;
      height: 40px;
      box-sizing: content-box;

      &.delete {
        &:before {
          content: url("../../assets/images/icons/trash.svg");
        }
      }

      &.edit {
        display: flex;

        &:before {
          display: block;
          content: url("../../assets/images/icons/pencil-black.svg");
        }
      }
    }
  }
}
</style>
