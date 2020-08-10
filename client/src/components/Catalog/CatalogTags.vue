<template>
  <section class="catalog-tags">
    <h2 class="catalog-tags__heading">
      Popular tags
    </h2>
    <div class="catalog-tags-list">
      <div class="catalog-tags-list__item" v-for="(tag, index) of this.tags" :key="index" ref="tag"
           @click="selectTag(tag, index)">
        {{ tag.name }}
      </div>
    </div>

  </section>
</template>

<script>
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
    selectTag(tag, index) {
      for (let item of document.querySelectorAll('.catalog-tags-list__item')) {
        item.classList.remove('active')
      }
      this.selectedTag = tag
      this.$refs.tag[index].classList.add('active')
      this.$emit('tag-select', tag)
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
        .catch(error => console.log(error))
  }
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

}
</style>
