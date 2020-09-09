<template>
  <aside class="catalog-tags">
    <h2 class="catalog-tags__heading">
      Popular tags
    </h2>
    <div class="catalog-tags-list">
      <span class="catalog-tags-list__item" :class="$store.getters.getSelectedTag === tag.id ? 'active' : ''"
            v-for="(tag, index) of this.tags" :key="index" :data-tag="'tag' + tag.id"
            @click="$store.commit('selectTag', tag.id)">
        {{ tag.name }}
      </span>
    </div>
    <button class="button--red catalog-tags__reset" @click="resetTags()" v-if="selectedTag">Reset</button>
  </aside>
</template>

<script>
import store from '@/store'

export default {
  props: {
    token: String
  },
  name: "CatalogTags",
  data() {
    return {
      tags: null,
      selectedTag: null
    }
  },
  methods: {
    selectTag(tagID) {
      this.selectedTag = tagID
      store.commit('selectTag', tagID)
      this.$emit('tag-select', tagID)
    },
    resetTags() {
      store.commit('resetTag')
      this.selectedTag = null
      for (let item of document.querySelectorAll('.catalog-tags-list__item')) {
        item.classList.remove('active')
        this.$emit('tag-select', '')
      }
    }
  },
  created() {
    fetch('http://localhost:8000/api/tags/', {
      method: 'GET',
      headers: {
        'Authorization': `Token ${this.token}`
      }
    })
        .then(response => response.json())
        .then(response => this.tags = response)
        .catch(error => console.error(error))

    this.resetTags()
  },
  computed: {
    chosenTag() {
      return store.getters.getSelectedTag
    }
  },
  watch: {
    chosenTag(newValue) {
      this.selectTag(newValue)
    }
  },

}
</script>

<style scoped lang="scss">
@import "../../styles/variables";

.catalog-tags {
  &__heading {
    font-size: 28px;
    margin-bottom: 30px;
  }

  &-list {
    display: flex;
    flex-wrap: wrap;

    &__item {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 10px;
      border-radius: 4px;
      border: 1px solid $main-lightgrey;
      margin-right: 10px;
      margin-bottom: 10px;
      transition-duration: .2s;
      cursor: pointer;

      &.active {
        background: $main-red;
        color: #ffffff;
        border: none;
        cursor: default;
      }
    }
  }

  &__reset {
    margin-top: 30px;
    height: 38px;
    font-weight: 600;
  }
}
</style>
