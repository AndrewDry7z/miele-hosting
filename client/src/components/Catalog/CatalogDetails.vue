<template>
  <div class="overlay" v-if="this.item" @click="overlayClick($event)">
    <aside class="catalog-details">
      <button class="catalog-details__close" @click="$emit('close-details'); owner = null" />
      <div class="catalog-details-content">
        <div class="catalog-details-content-left">
          <div class="catalog-details-preview">
            <tiny-slider class="catalog-item-files-slider slider"
                         :navAsThumbnails="true"
                         :navContainer="this.item.previews.length > 1 ? ('#custom-nav-detail') : false"
                         :controls="false"
                         :autoHeight="true"
                         :nav="this.item.previews.length > 1">
              <div v-for="(item, index) in this.item.previews.slice(0, 5)" :key="index">
                <img :src="item.image" :alt="item.name" class="catalog-details-preview-slider__item">
              </div>
            </tiny-slider>
            <ul class="slider-nav" id="custom-nav-detail" v-if="this.item.previews.length > 1">
              <li v-for="(item, index) in this.item.previews.slice(0, 5)" :key="index">
                <img :src="item.image" :alt="item.name" class="catalog-item-files-slider__item">
              </li>
            </ul>
          </div>
          <div class="catalog-details-owner" v-if="owner">
            <p class="catalog-details-owner__heading grey">Owner</p>
            <router-link :to="'/profile/' + this.item.owner" class="catalog-details-owner-person">
              <img :src="this.owner.person.photo" :alt="this.owner.first_name"
                   class="catalog-details-owner-person__photo">
              <p class="catalog-details-owner-person__name">
                {{ this.owner.first_name }}
              </p>
            </router-link>
          </div>
          <div class="catalog-details-tags">
          <span class="catalog-details-tags__item"
                v-for="tag of this.item.tags"
                :key="tag.id" @click="chooseTag(tag.id)">
            {{ tag.name }}
          </span>
          </div>
        </div>
        <div class="catalog-details-content-right">
          <p class="catalog-details__article grey" v-if="this.item.article.length > 0">
            Article: {{ this.item.article }}
          </p>
          <p class="catalog-details__title">
            {{ this.item.title }}
          </p>
          <p class="catalog-details__description">
            {{ this.item.description }}
          </p>
          <ul class="catalog-details-files" v-if="item.files.length > 0">
            <li v-for="(file, index) in item.files" :key="index" class="catalog-details-files__item">
              <p v-if="file.name.length > 0">{{ file.name }} {{ formatBytes(file.file_size) }}</p>
              <p v-else>File {{ file.title }} {{ formatBytes(file.file_size) }}</p>
              <a :href="file.file" class="button button--red">Download</a>
            </li>
          </ul>
        </div>
      </div>
    </aside>
  </div>
</template>

<script>
import VueTinySlider from 'vue-tiny-slider';
import store from '@/store'

export default {
  components: {'tiny-slider': VueTinySlider},
  data() {
    return {
      owner: null,
      serverUrl: process.env.VUE_APP_SERVER_URL
    }
  },
  props: {
    item: Object
  },
  methods: {
    getItemsOwner(id) {
      fetch(`${process.env.VUE_APP_SERVER_URL}/api/users/${id}/`, {
        method: 'GET',
        headers: {
          'Authorization': `Token ${this.$cookies.get('mieletoken')}`
        }
      })
          .then(response => response.json())
          .then(response => {
                this.owner = response
                if (!this.owner.person.photo) {
                  this.owner.person.photo = "/img/default_photo.jpg"
                }
              }
          )
          .catch(error => console.error(error))
    },
    formatBytes(bytes, decimals = 2) {
      if (bytes === 0) return '0 Bytes';

      const k = 1024;
      const dm = decimals < 0 ? 0 : decimals;
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

      const i = Math.floor(Math.log(bytes) / Math.log(k));

      return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    },
    chooseTag(tagID) {
      this.owner = null
      store.commit('selectTag', tagID)
      this.$emit('tag-select', tagID)
      this.$emit('close-details');

      if (this.$route.name !== 'Home') {
        this.$router.push('/')
        store.commit('selectTag', tagID)
      }
    },
    overlayClick(event) {
      if (event.target.classList.contains('overlay')) {
        this.$emit('overlay-click', event)
        this.owner = null
      } else {
        return false
      }
    }
  },
  beforeUpdate() {
    if ((this.item) && (!this.owner)) {
      this.getItemsOwner(this.item.owner)
    }
  },
  name: "CatalogDetails"
}
</script>

<style scoped lang="scss">
@import "../../styles/variables";

.overlay {
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  background: rgba(30, 30, 30, 0.6);
  z-index: 10;
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

  @media screen and (max-width: 600px) {
    width: 100%;
    padding: 4vw;
  }


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
    display: flex;

    &-left {
      width: 50%;
      padding: 0 20px 0 0;
    }

    &-right {
      width: 50%;
      padding: 0 0 0 20px;
    }
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

  .slider-nav {
    display: flex !important;

    li {
      width: 19%;
      margin-right: 5px;
    }
  }

  &-preview {
    width: 70%;

    &-slider {
      &__item {
        padding-left: 1px;
        margin-left: -1px;
        width: 100%;
      }
    }
  }

  &-owner {
    margin-top: 40px;
    padding-bottom: 25px;
    border-bottom: 1px solid $main-lightgrey;

    &__heading {
      display: flex;

      &:after {
        content: '';
        border-bottom: 1px solid $main-lightgrey;
        width: 88%;
        margin-left: auto;
        display: block;
      }
    }

    &-person {
      display: flex;
      align-items: center;
      margin-top: 20px;
      text-decoration: none;

      &__photo {
        width: 40px;
        height: 40px;
        object-fit: cover;
        border-radius: 50%;
        padding: 2px;
        border: 1px solid $main-lightgrey;
        margin-right: 16px;
      }

      &__name {
        font-size: 15px;
        font-weight: 600;
        color: $main-black;
      }
    }
  }

  &-files {
    &__item {
      display: grid;
      gap: 10px;
      grid-template-columns: 2fr 1fr;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 20px;

      .button {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 170px;
        height: 38px;
        font-weight: 600;
        text-decoration: none;
      }
    }
  }
}
</style>
