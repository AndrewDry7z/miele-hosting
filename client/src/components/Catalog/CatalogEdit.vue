<template>
  <main class="catalog-edit">
    <div class="container">
      <h1 class="catalog-edit__title">
        Edit file
      </h1>
      <p class="catalog-edit__heading">
        Previews
      </p>
      <form class="catalog-edit-flex" @submit="updateCatalogItem">
        <div class="catalog-edit-previews">
          <div class="catalog-edit-previews-big">
            <img :src="previewImages[this.activeImageIndex].url
                ? previewImages[this.activeImageIndex].url
                : previewImages[this.activeImageIndex]"
                 alt="Preview" class="catalog-edit-previews-big__image">
            <div class="catalog-edit-previews-big-buttons">
              <label class="catalog-edit-previews-big-buttons__item" role="button" for="replacePreview">
                <input type="file" id="replacePreview" hidden accept="image/jpeg, image/png"
                       @change="replacePreview($event, activeImageIndex)">
                <img src="../../assets/images/icons/photo.svg" alt="Delete this preview" title="Delete this preview">
              </label>
              <button class="catalog-edit-previews-big-buttons__item" type="button"
                      @click="deletePreview(previewImages[activeImageIndex])">
                <img src="../../assets/images/icons/trash.svg" alt="Delete this preview" title="Delete this preview">
              </button>
            </div>
          </div>
          <ul class="catalog-edit-previews-list" v-if="previewImages.length > 0">
            <li class="catalog-edit-previews-list-item" v-for="(item, index) of previewImages" :key="index"
                @click="activeImageIndex = index">
              <img :src="item.url ? item.url : item" alt="" class="catalog-edit-previews-list-item__image">
              <button class="catalog-edit-previews-list-item__remove"></button>
            </li>
            <li class="catalog-edit-previews-list-item">
              <input type="file" id="fileInput" hidden multiple accept="image/jpeg, image/png"
                     @change="showNewImages($event)">
              <label for="fileInput" class="catalog-edit-previews-list-item__add">+</label>
            </li>
          </ul>
        </div>
        <div class="catalog-edit-data">
          <label class="catalog-edit-data__item">
            Title
            <input type="text" class="catalog-edit-data__input" v-model="item.title" required>
          </label>
          <label class="catalog-edit-data__item">
            Description
            <textarea class="catalog-edit-data__textarea" v-model="item.description"></textarea>
          </label>
          <div class="catalog-edit-data--50">
            <label class="catalog-edit-data__item">
              Choose article
              <input type="text" class="catalog-edit-data__input" v-model="item.article">
            </label>
            <label class="catalog-edit-data__item">
              Choose tag
              <input type="text" list="tagsList" class="catalog-edit-data__input" v-model="tagInput"
                     placeholder="No tag" @change="selectTag()">
              <datalist id="tagsList">
                <option v-for="tag of this.tagsList"
                        :key="tag.id"
                        :data-value="tag.id">
                  {{ tag.name }}
                </option>
              </datalist>
            </label>
          </div>
          <div class="catalog-edit-tags" v-if="selectedTags.length > 0">
            <div class="catalog-edit-tags-item" v-for="(tag, index) of this.selectedTags" :key="index">
              {{ tag }}
              <span class="catalog-edit-tags-item__close" @click="$delete(selectedTags, index)"></span>
            </div>
          </div>
          <div class="catalog-edit-buttons">
            <button class="button--red catalog-edit-buttons__item" type="submit">
              Save
            </button>

            <label role="button" class="button--grey catalog-edit-buttons__item">
              + Add files
              <input type="file" multiple hidden @change="clickAddFiles($event)">
            </label>

            <div class="catalog-edit-goback">
              <span id="or">or </span>
              <router-link to="/" class="catalog-edit-goback__link">Cancel</router-link>
            </div>
          </div>
          <ul class="files-preview" v-if="files.length > 0">
            <li v-for="(file, index) in files" :key="index">
              {{ file.name ? file.name : file.title }}
              ({{ file.file_size ? formatBytes(file.file_size) : formatBytes(file.size) }})
              <button @click="removeFile(file)" title="Remove" type="button">X</button>
            </li>
          </ul>
        </div>
      </form>
    </div>
    <aside class="overlay" v-if="showMessage">
      <section class="message">
        <span class="message__icon" :class="error ? 'false' : 'true'"></span>
        <h3 class="message__text" v-if="error">Something went wrong, try again later</h3>
        <h3 class="message__text" v-else>Successfully updated</h3>
        <router-link :to="`/profile/${this.owner}/`" class="message__button button--red">Continue</router-link>
      </section>
    </aside>
  </main>
</template>

<script>
import store from "@/store"

export default {
  name: "CatalogEdit",
  data() {
    return {
      token: null,
      item: {},
      initialItem: {},
      catalog: store.getters.getCatalog,
      tagInput: '',
      tagsList: [],
      tagNamesList: [],
      selectedTags: [],
      initialSelectedTagNames: [],
      activeImageIndex: 0,
      previewImages: [],
      showedPreviews: [],
      files: [],
      newFiles: [],
      showMessage: false,
      error: false,
      owner: null
    }
  },
  methods: {
    selectTag() {
      if (!this.selectedTags.includes(this.tagInput)) {
        this.selectedTags.push(this.tagInput)
        this.tagInput = null
      }
    },
    deletePreview() {
      this.$delete(this.previewImages, this.activeImageIndex)
      if (this.activeImageIndex === this.previewImages.length) {
        this.activeImageIndex--
      }
    },
    replacePreview(event, index) {
      Array.prototype.insert = function (index, item) {
        this.splice(index, 0, item);
      };

      this.$delete(this.previewImages, index)
      let image = event.target.files[0]
      let url = URL.createObjectURL(image)
      if (!this.showedPreviews.includes(image)) {
        this.previewImages.insert(index, {url: url, file: image})
        this.showedPreviews.push(image)
      }
    },
    removeFile(file) {
      this.files = this.files.filter(f => {
        return f != file;
      });
    },
    showNewImages(event) {
      let newImages = event.target.files;
      if (!newImages) return;
      ([...newImages]).forEach(image => {
        if (!this.previewImages.includes(image)) {
          let url = URL.createObjectURL(image)
          if (!this.showedPreviews.includes(image)) {
            this.previewImages.push({url: url, file: image})
            this.showedPreviews.push(image)
          }
        }
      });
    },
    clickAddFiles(event) {
      let selectedFiles = event.target.files
      if (!selectedFiles) return
      ([...selectedFiles]).forEach(f => {
        this.files.push(f);
      });
      ([...selectedFiles]).forEach(f => {
        if (!this.newFiles.includes(f)) {
          this.newFiles.push(f);
        }
      })
    },
    formatBytes(bytes, decimals = 2) {
      if (bytes === 0) return '0 Bytes';

      const k = 1024;
      const dm = decimals < 0 ? 0 : decimals;
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

      const i = Math.floor(Math.log(bytes) / Math.log(k));

      return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    },
    updateFiles() {
      let filesToDelete = this.initialItem.files.filter(file => !this.files.includes(file))
      let vm = this
      let headers = new Headers()
      headers.append('Authorization', `Token ${vm.token}`)

      const deleteFile = async function (id) {
        let response = await fetch(`${process.env.VUE_APP_SERVER_URL}/api/files/${id}/`, {
          method: 'DELETE',
          headers: headers
        })
            .catch(error => console.error(error))
        return await response.json()
      }
      const uploadFiles = async function (file, id) {
        let formData = new FormData()
        formData.append('file', file)
        formData.append('catalog_item', id)
        let response = await fetch(`${process.env.VUE_APP_SERVER_URL}/api/files/`, {
          method: 'POST',
          headers: headers,
          body: formData
        })
            .catch(error => console.error(error))
        return await response.json()
      }

      if (filesToDelete.length > 0) {
        for (let file of filesToDelete) {
          deleteFile(file.id)
        }
      }

      for (let file of this.newFiles) {
        uploadFiles(file, this.item.id)
      }
      this.newFiles = []
    },
    updateTags() {
      let vm = this
      let headers = new Headers()
      headers.append('Authorization', `Token ${this.token}`)
      let newTags = this.selectedTags.filter(tag => !this.tagNamesList.includes(tag))
      let tagsToUpdate = this.selectedTags.filter(tag => !this.initialSelectedTagNames.includes(tag))
      tagsToUpdate = tagsToUpdate.filter(tagName => !newTags.includes(tagName))
      let tagsToDeleteObj = this.initialItem.tags.filter(tag => !this.selectedTags.includes(tag.name))

      const removeItemFromTagsItemList = async function (tag, itemId) {
        let customHeaders = headers
        let formData = new FormData()
        let catalogItems = tag.catalog_items.filter(id => id !== itemId)
        formData.append('catalog_items', catalogItems)
        let method = 'PATCH'
        if (catalogItems.length < 1) {
          method = 'DELETE'
        }
        let response = await fetch(`${process.env.VUE_APP_SERVER_URL}/api/tags/${tag.id}/`, {
          method: method,
          headers: customHeaders,
          body: formData
        })
        return await response.json()
      }

      const addNewTags = async function (tagName, itemID) {
        let formData = new FormData()
        formData.append('name', tagName)
        formData.append('catalog_items', [itemID])

        let response = await fetch(`${process.env.VUE_APP_SERVER_URL}/api/tags/`, {
          method: 'POST',
          headers: headers,
          body: formData
        })
            .catch(error => console.error(error))
        return await response.json()
      }

      const updateExistingTags = async function (tagName, itemID) {
        let updTagObj = vm.tagsList.filter(tag => tag.name === tagName)[0]
        updTagObj.catalog_items.push(itemID)
        let response = await fetch(`${process.env.VUE_APP_SERVER_URL}/api/tags/${updTagObj.id}/`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${vm.token}`
          },
          body: JSON.stringify(updTagObj)
        })
            .catch(error => console.error(error))
        return await response.json()
      }

      for (let tag of tagsToDeleteObj) {
        removeItemFromTagsItemList(tag, this.item.id)
      }

      for (let tag of newTags) {
        addNewTags(tag, this.item.id)
      }

      for (let tag of tagsToUpdate) {
        if (!this.initialSelectedTagNames.includes(tag.name)) {
          updateExistingTags(tag, this.item.id)
        }
      }
    },
    updatePreviews() {
      let newPreviews = this.previewImages.filter(item => typeof item === 'object')
      let previewsToDelete = this.initialItem.previews.filter(tag => !this.previewImages.includes(tag.image))

      let headers = new Headers()
      headers.append('Authorization', `Token ${this.token}`)

      const uploadNewPreview = async function (image, itemID) {
        let formData = new FormData()
        formData.append('image', image)
        formData.append('catalog_item', itemID)
        let response = await fetch(`${process.env.VUE_APP_SERVER_URL}/api/previews/`, {
          method: 'POST',
          headers: headers,
          body: formData
        })
            .catch(error => console.error(error))
        return await response.json()
      }

      const deletePreview = async function (itemID) {
        let response = await fetch(`${process.env.VUE_APP_SERVER_URL}/api/previews/${itemID}/`, {
          method: 'DELETE',
          headers: headers,
        })
            .catch(error => console.error(error))
        return await response.json()
      }

      for (let preview of newPreviews) {
        uploadNewPreview(preview.file, this.item.id)
      }

      for (let preview of previewsToDelete) {
        deletePreview(preview.id)
      }
    },
    updateCatalogItem(event) {
      event.preventDefault()
      let formData = new FormData()
      let headers = new Headers()

      formData.append('title', this.item.title)
      formData.append('description', this.item.description)
      formData.append('article', this.item.article)

      headers.append("Authorization", `Token ${this.token}`);

      fetch(`${process.env.VUE_APP_SERVER_URL}/api/catalog/${this.item.id}/`, {
        method: 'PATCH',
        headers: headers,
        body: formData,
        redirect: 'follow'
      })
          .then(() => {
            this.updateFiles()
          })
          .then(() => {
            this.updateTags()
          })
          .then(() => {
            this.updatePreviews()
          })
          .then(() => {
            store.commit('setCatalog', this.token)
          })
          .then(() => {
            this.showMessage = true
          })
          .catch(error => {
            console.error(error)
          })
    }
  }
  ,
  created() {
    this.token = this.$cookies.get('mieletoken')
    this.item = this.catalog.filter(item => item.id.toString() === this.$route.params.id)[0]
    this.initialItem = this.item
    store.commit('setTagsList', this.$cookies.get('mieletoken'))
    this.tagsList = store.getters.getTagsList
    this.owner = store.getters.getUserInfo.id
    this.showMessage = false
    this.error = false
    for (let tag of this.item.tags) {
      this.selectedTags.push(tag.name)
      this.initialSelectedTagNames.push(tag.name)
    }
    for (let tag of this.tagsList) {
      this.tagNamesList.push(tag.name)
    }
    for (let preview of this.item.previews) {
      this.previewImages.push(preview.image)
    }
    for (let file of this.item.files) {
      this.files.push(file)
    }
  }
  ,
  beforeDestroy() {
    store.commit('setCatalog', this.token)
  }
}
</script>

<style scoped lang="scss">
@import "../../styles/variables";

.catalog-edit {
  &__title {
    font-size: 40px;
    font-weight: 500;
    padding-bottom: 30px;
    margin-bottom: 70px;
    border-bottom: 1px solid #E9E9E9;

    @media screen and (max-width: 1000px) {
      margin-bottom: 30px;
    }
  }

  &-buttons {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    margin-top: 50px;

    @media screen and (max-width: 1000px) {
      flex-direction: column;
      margin-bottom: 50px;
    }

    &__item {
      font-size: 15px;
      font-weight: 600;
      width: 200px;

      @media screen and (max-width: 1000px) {
        width: 100%;
        margin: 10px 0;
      }
    }

    label {
      display: flex;
      align-items: center;
      justify-content: center;
      margin-left: 16px;
      margin-right: 30px;
      cursor: pointer;

      @media screen and (max-width: 1000px) {
        margin: 10px 0;
      }
    }
  }

  &-goback {
    &__link {
      text-decoration: none;
      color: inherit;
    }

    #or {
      color: $main-grey;
    }
  }

  &__heading {
    margin-bottom: 30px;
    font-size: 20px;
  }

  &-data {

    &__item {
      font-size: 20px;
      margin-bottom: 30px;
      display: block;
      width: 100%;
    }

    &__input {
      display: block;
      width: 100%;
      font-size: 15px;
      background: $main-lightgrey;
      padding-left: 20px;
      margin-top: 20px;
      height: 50px;
    }

    &__textarea {
      display: block;
      background: $main-lightgrey;
      width: 100%;
      height: 120px;
      padding: 20px;
      font-size: 15px;
      margin-top: 20px;
    }

    &--50 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      width: 100%;
      gap: 30px;
    }
  }

  &-tags {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    margin-top: 30px;

    &-item {
      display: flex;
      align-items: center;
      margin-right: 10px;
      padding: 0 15px;
      border: 1px solid $main-lightgrey;
      border-radius: 4px;
      height: 30px;
      color: #000;
      font-size: 11px;

      &__close {
        cursor: pointer;
        margin-left: 12px;

        &:after {
          content: "\2715";
          font-size: 14px;
        }
      }
    }
  }

  &-flex {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 70px;

    @media screen and (max-width: 1000px) {
      display: block;
    }
  }

  &-previews {

    &-big {
      position: relative;
      display: flex;
      justify-content: center;
      align-items: center;
      transition-duration: .3s;

      &:before {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
        position: absolute;
        content: url("~@/assets/images/icons/zoom-in.svg");
        top: 0;
        left: 0;
        z-index: 1;
        background: rgba(0, 0, 0, .5);
        cursor: pointer;
        opacity: 0;
        transition-duration: .3s;
      }

      &:hover {
        &:before {
          opacity: 1;
        }
      }

      &-buttons {
        position: absolute;
        top: 10px;
        right: 10px;
        z-index: 2;

        &__item {
          cursor: pointer;
          display: flex;
          justify-content: center;
          align-items: center;
          width: 40px;
          height: 40px;
          background: $main-lightgrey;
          border-radius: 50%;
          border: 8px solid #fff;
          box-sizing: content-box;
          box-shadow: 0 0 0 1px $main-lightgrey;
          margin-bottom: 4px;
        }
      }
    }

    &-list {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr 1fr 1fr;
      gap: 15px;
      margin-top: 25px;

      @media screen and (max-width: 1000px) {
        grid-template-columns: 1fr 1fr 1fr 1fr;
      }

      &-item {
        cursor: pointer;
        height: 90px;

        &__image {
          height: 100%;
          width: 100%;
          object-fit: cover;
        }

        &__add {
          height: 90px;
          width: 100%;
          display: flex;
          background: $main-lightgrey;
          justify-content: center;
          align-items: center;
          cursor: pointer;
          font-size: 40px;
        }
      }
    }
  }

  .overlay {
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(40, 40, 40, 0.5);

    .message {
      padding: 50px;
      background: #ffffff;
      text-align: center;
      max-width: 540px;

      &__icon {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 44px;
        width: 44px;
        border: 2px solid #000;
        border-radius: 50%;
        margin: 0 auto 24px;

        &:before {
          font-size: 34px;
          font-weight: 300;
        }

        &.true {
          &:before {
            content: '\2714';
          }
        }

        &.false {
          &:before {
            content: '\2715';
          }
        }
      }

      &__text {
        font-size: 28px;
        font-weight: 600;
      }

      &__button {
        width: 210px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 15px;
        font-weight: 600;
        text-decoration: none;
        margin: 55px auto 0;
      }
    }
  }
}
</style>
