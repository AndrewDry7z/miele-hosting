<template>
  <main class="home">
    <div class="container">
      <router-link to="/add" class="catalog-add-button">
        + Add content
      </router-link>
      <div class="home-grid">
        <div class="catalog">
          <div class="catalog-grid">
            <CatalogItem
                v-for="item in filteredCatalog"
                :key="item.id"
                :id="item.id"
                :title="item.title"
                :article="item.article"
                :description="item.description"
                :previews="item.previews"
                @item-selected="itemSelected(item.id)"
                @show-lightbox="showLightbox($event)" />
          </div>
        </div>
        <CatalogTags :token="token" @tag-select="filterByTag($event)" />
        <CatalogDetails
            v-if="screenWidth > 600"
            :item="selectedItem"
            @close-details="closeDetails()"
            @overlay-click="overlayClick($event)"
            @tag-select="filterByTag($event)"
            @show-lightbox="showLightbox($event)"/>
        <CatalogDetailsMobile
            v-else
            :item="selectedItem"
            @close-details="closeDetails()"
            @overlay-click="overlayClick($event)"
            @tag-select="filterByTag($event)"
            @show-lightbox="showLightbox($event)"/>
        <Lightbox
            v-if="lightboxImage"
            :image="lightboxImage"
            @close-lightbox="closeLightbox()" />
      </div>
    </div>
  </main>
</template>

<script>
import CatalogItem from "./CatalogItem";
import CatalogDetails from "./CatalogDetails";
import CatalogDetailsMobile from "@/components/Catalog/CatalogDetailsMobile";
import CatalogTags from "@/components/Catalog/CatalogTags";
import store from '@/store'
import Lightbox from "@/components/Catalog/Lightbox";

export default {
  name: "Catalog",
  components: {Lightbox, CatalogTags, CatalogDetails, CatalogDetailsMobile, CatalogItem},
  data() {
    return {
      catalog: store.getters.getCatalog,
      selectedItem: null,
      token: this.$cookies.get('mieletoken'),
      filteredCatalog: store.getters.getCatalog,
      selectedTag: store.getters.getSelectedTag,
      screenWidth: screen.width,
      lightboxImage: null
    }
  },
  methods: {
    itemSelected(id) {
      this.selectedItem = this.catalog.find(item => item.id === id)
    },
    closeDetails() {
      this.selectedItem = null
    },
    overlayClick(event) {
      if (event.target.classList.contains('overlay')) {
        this.selectedItem = null
      }
    },
    filterByTag() {
      this.selectedTag = store.getters.getSelectedTag
      if (this.selectedTag) {
        this.filteredCatalog = []
      } else {
        this.filteredCatalog = this.catalog
      }
      for (let item of this.catalog) {
        if (item.tags.some(tagItem => tagItem.id === this.selectedTag)) {
          this.filteredCatalog.push(item)
        }
      }
    },
    showLightbox(image) {
      this.lightboxImage = image
    },
    closeLightbox() {
      this.lightboxImage = null
    }
  },
  created() {
    if (this.$cookies.isKey('mieletoken')) {
      store.commit('setCatalog', this.token)
      this.token = this.$cookies.get('mieletoken')
      this.catalog = store.getters.getCatalog
      this.filteredCatalog = this.catalog
      this.selectedTag = null
    } else {
      this.$router.push('/auth/')
    }

    if (store.getters.getCatalog.length < 1) {
      fetch(`${process.env.VUE_APP_SERVER_URL}/api/catalog/`, {
        method: 'GET',
        headers: {
          'Authorization': `Token ${this.$cookies.get('mieletoken')}`
        }
      })
          .then(response => response.json())
          .then(response => {
                this.catalog = response
                this.filteredCatalog = response
              }
          )
          .catch(error => console.error(error))
    }
  }
}
</script>

<style lang="scss">
@import "~@/styles/_variables.scss";

.catalog {
  &-grid {
    display: grid;
    align-items: stretch;
    grid-template-columns: repeat(auto-fill, minmax(288px, 1fr));
    grid-column-gap: 20px;
    grid-row-gap: 30px;
  }

  &-add {
    &-button {
      display: block;
      padding: 20px 25px;
      background: $main-lightgrey;
      color: $main-black;
      text-decoration: none;
      width: 170px;
      margin-bottom: 30px;
      text-align: center;

      @media screen and (max-width: 600px) {
        width: 100%;
      }
    }
  }
}

.home {
  &-grid {
    display: grid;
    grid-template-columns: 3fr 1fr;
    column-gap: 30px;

    @media screen and (max-width: 1000px) {
      display: flex;
      flex-direction: column-reverse;
    }
  }
}
</style>
