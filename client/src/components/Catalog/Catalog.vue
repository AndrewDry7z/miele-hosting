<template>
  <div class="catalog">
    <div class="catalog-grid">
      <CatalogItem
          v-for="item in catalog"
          :key="item.id"
          :title="item.title"
          :article="item.article"
          :description="item.description"
          @item-selected="itemSelected(item.id)"
      />
    </div>

    <CatalogDetails
        :item="selectedItem"
        @close-details="closeDetails()"
        @overlay-click="overlayClick($event)"
    />
  </div>
</template>

<script>
import CatalogItem from "./CatalogItem";
import CatalogDetails from "./CatalogDetails";

export default {
  name: "Catalog",
  components: {CatalogDetails, CatalogItem},
  data() {
    return {
      catalog: [],
      selectedItem: null
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
    }
  },
  created() {
    fetch('http://192.168.1.70:8000/api/catalog/', {
      method: 'GET',
      headers: {
        'Authorization': 'Token ac7afdd227809142e41fd109ce2bcbe4c2e01e4d'
      }
    })
        .then(response => response.json())
        .then(response => this.catalog = response)
        .catch(error => console.log(error))
  }
}
</script>

<style scoped lang="scss">
.catalog {
  &-grid {
    display: grid;
    align-items: stretch;
    grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
    grid-column-gap: 20px;
    grid-row-gap: 30px;
  }
}
</style>
