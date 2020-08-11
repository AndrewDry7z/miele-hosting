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
                :title="item.title"
                :article="item.article"
                :description="item.description"
                @item-selected="itemSelected(item.id)"
            />
          </div>
        </div>
        <CatalogTags :token="token"
                     @tag-select="filterByTag($event)"
        />
        <CatalogDetails
            :item="selectedItem"
            @close-details="closeDetails()"
            @overlay-click="overlayClick($event)"
        />
      </div>
    </div>

  </main>
</template>

<script>
import CatalogItem from "./CatalogItem";
import CatalogDetails from "./CatalogDetails";
import CatalogTags from "@/components/Catalog/CatalogTags";

export default {
  name: "Catalog",
  components: {CatalogTags, CatalogDetails, CatalogItem},
  data() {
    return {
      catalog: [],
      selectedItem: null,
      token: '',
      filteredCatalog: []
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
    filterByTag(tag) {
      this.filteredCatalog = []
      for (let item of this.catalog) {
        if (item.tags.some(tagItem => tagItem.id === tag.id)) {
          this.filteredCatalog.push(item)
        }
      }
    }
  },
  created() {
    if (this.$cookies.isKey('mieletoken')) {
      this.token = this.$cookies.get('mieletoken')
      fetch('http://localhost:8000/api/catalog/', {
        method: 'GET',
        headers: {
          'Authorization': `Token ${this.token}`
        }
      })
          .then(response => response.json())
          .then(response => {
                this.catalog = response
                this.filteredCatalog = this.catalog
              }
          )
          .catch(error => console.log(error))
    } else {
      this.$router.push('/auth/')
    }

  }
}
</script>

<style scoped lang="scss">
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
      width: fit-content;
      margin-bottom: 30px;
    }
  }
}

.home {
  &-grid {
    display: grid;
    grid-template-columns: 3fr 1fr;
    column-gap: 30px;

    @media screen and (max-width: 1000px) {
      display: block;
    }
  }
}
</style>