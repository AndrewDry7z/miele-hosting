<template>
  <main class="catalog-add">
    <div class="container">
      <h1 class="catalog-add__title">
        Add files
      </h1>
      <form class="catalog-add-form" @submit.prevent="addCatalogItemFormSubmit()" enctype="multipart/form-data">
        <p class="catalog-add-form__heading">
          Upload preview
        </p>
        <div class="catalog-add-form-flex">
          <div class="catalog-add-form-file">
            <label class="dragndrop-area" ref="fileform" for="fileInput" v-cloak @drop.prevent="addPreview"
                   @dragover.prevent v-if="screenWidth > 600">
              Drag and Drop here <br />
              or <br />
              <span>Browse files</span>
              <img src="../../assets/images/drag-n-drop.svg"
                   class="dragndrop-area__image"
                   alt="Drag N Drop Files Here">
            </label>
            <label class="dragndrop-area" ref="fileform" for="fileInput" v-cloak @drop.prevent="addPreview"
                   @dragover.prevent v-else>
              <span>Upload previews</span>
              <img src="../../assets/images/drag-n-drop.svg"
                   class="dragndrop-area__image"
                   alt="Drag N Drop Files Here">
            </label>
            <input type="file" id="fileInput" name="files[]" hidden multiple accept="image/jpeg, image/png" class="fileInput"
                   @change="clickAddPreview($event)">
            <ul class="dragndrop-previews" v-if="previews.length > 0">
              <li v-for="(image, index) in previews" :key="index" class="dragndrop-previews-item">
                <img :src="showPreview(image)" :alt="image.name" class="dragndrop-previews-item__image">
                <button @click="removeFile(image)" title="Remove" class="dragndrop-previews-item__remove"></button>
              </li>
              <li class="dragndrop-previews-item">
                <label for="fileInput" class="dragndrop-previews-item__add">+</label>
              </li>
            </ul>
          </div>
          <fieldset class="catalog-add-form-inputs">
            <p>
              <label for="title">Title</label>
              <input id="title" type="text" name="title" placeholder="Add Text Title" required
                     v-model="formData.title">
            </p>
            <p>
              <label for="description">Description</label>
              <textarea name="description" id="description" rows="10" placeholder="Add Text Description"
                        v-model="formData.description"></textarea>
            </p>

            <div class="catalog-add-form-flex">
              <p class="half">
                <label for="article">Choose Article</label>
                <input type="text" name="article" id="article" placeholder="Add Article" v-model="formData.article">
              </p>
              <p class="half">
                <label for="tagsInput">Choose tag</label>
                <input list="tagsList" id="tagsInput"
                       name="tags" placeholder="No Tag"
                       v-model="tagInput"
                       @change="selectTag()"
                />
                <datalist id="tagsList">
                  <option v-for="tag of this.tags"
                          :key="tag.id"
                          :data-value="tag.id">
                    {{ tag.name }}
                  </option>
                </datalist>
              </p>
            </div>

            <div class="catalog-add-form-tags" v-if="selectedTags.length > 0">
              <div class="catalog-add-form-tags-item" v-for="(tag, index) of selectedTags" :key="index">
                {{ tag }}
                <span class="catalog-add-form-tags-item__close" @click="$delete(selectedTags, index)"></span>
              </div>
            </div>

            <div class="catalog-add-form-buttons">
              <button type="submit" class="button--red catalog-add-form__button">
                Save
              </button>

              <label role="button" class="button--grey catalog-add-form__button">
                + Add files
                <input type="file" multiple hidden @change="clickAddFiles($event)">
              </label>

              <div class="catalog-add-form__goback">
                <span id="or">or </span>
                <router-link to="/" class="catalog-add-form__cancel">Cancel</router-link>
              </div>
            </div>
            <ul class="files-preview">
              <li v-for="(file, index) in files" :key="index">
                {{ file.name }}
                <button @click="removeFile(file)" title="Remove">X</button>
              </li>
            </ul>
          </fieldset>
        </div>
      </form>
    </div>
    <aside class="overlay" v-if="showMessage">
      <section class="message">
        <span class="message__icon" :class="error ? 'false' : 'true'"></span>
        <h3 class="message__text" v-if="error">Something went wrong, try again later</h3>
        <h3 class="message__text" v-else>This file was uploaded successfully</h3>
        <router-link to="/" class="message__button button--red">Continue</router-link>
      </section>
    </aside>
  </main>
</template>

<script>
import store from '@/store'

export default {

  name: "CatalogAdd",
  components: {},
  data() {
    return {
      tags: [],
      selectedTags: [],
      tagInput: null,
      previews: [],
      files: [],
      formData: {
        title: '',
        description: '',
        article: '',
        owner: null
      },
      newItemID: null,
      token: null,
      showMessage: false,
      error: false,
      screenWidth: null
    }
  },
  methods: {
    selectTag() {
      if (!this.selectedTags.includes(this.tagInput)) {
        this.selectedTags.push(this.tagInput)
        this.tagInput = null
      }
    },
    showPreview(image) {
      let preview = URL.createObjectURL(image)
      return preview
    },
    addPreview(e) {
      let droppedImages = e.dataTransfer.files;
      if (!droppedImages) return;
      ([...droppedImages]).forEach(f => {
        this.previews.push(f);
      });
    },
    clickAddPreview(event) {
      let selectedImages = event.target.files;
      if (!selectedImages) return;
      ([...selectedImages]).forEach(f => {
        this.previews.push(f);
      });
    },
    clickAddFiles(event) {
      let selectedFiles = event.target.files;
      if (!selectedFiles) return;
      ([...selectedFiles]).forEach(f => {
        this.files.push(f);
      });
    },
    removeFile(file) {
      this.previews = this.previews.filter(f => {
        return f != file;
      });
      this.files = this.files.filter(f => {
        return f != file;
      });
    },
    addTags() {
      let existingTagNames = []

      for (let tag of this.tags) {
        existingTagNames.push(tag.name)
      }

      let newTagNamesArray = this.selectedTags.filter(name => !existingTagNames.includes(name))
      let vm = this

      //adding new tags
      new Promise((resolve) => {
        let upload = async function (item) {
          let response = await fetch(`${process.env.VUE_APP_SERVER_URL}/api/tags/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Token ${vm.token}`
            },
            body: JSON.stringify({
              name: item,
              catalog_items: [vm.newItemID]
            })
          })
              .catch(error => {
                console.error(error)
                this.error = true
              })
          return await response.json()
        }
        for (let newTagName of newTagNamesArray) {
          upload(newTagName)
              .then(response => console.log(response));
          // todo: check if database still locked after host on production
        }
        resolve();
      })
          .then(() => {
            //updating existing tags
            const existingSelectedTagNamesArray = this.selectedTags.filter(name => existingTagNames.includes(name))
            const upload = async function (item, id) {
              let response = await fetch(`${process.env.VUE_APP_SERVER_URL}/api/tags/${id}/`, {
                method: 'PATCH',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Token ${vm.token}`
                },
                body: JSON.stringify({
                  catalog_items: item
                })
              })
                  .catch(error => console.error(error))
              return await response.json()
            }
            for (let tag of this.tags) {
              if (existingSelectedTagNamesArray.includes(tag.name)) {
                tag.catalog_items.push(vm.newItemID)
                upload(tag.catalog_items, tag.id)
                    .then(response => console.log(response));
              }
            }
          })
    },
    uploadPreviews() {
      let token = this.token
      let newItemID = this.newItemID
      let headers = new Headers()
      headers.append("Authorization", `Token ${token}`);
      const upload = async function (image) {
        let formdata = new FormData();
        formdata.append("catalog_item", newItemID)
        formdata.append("image", image)
        let response = await fetch(`${process.env.VUE_APP_SERVER_URL}/api/previews/`, {
          method: 'POST',
          headers: headers,
          body: formdata,
          redirect: 'follow'
        })
        return await response.json()
      }
      for (let image of this.previews.reverse()) {
        upload(image).then(response => console.log(response))
      }
    },
    uploadFiles() {
      let token = this.token
      let newItemID = this.newItemID
      let headers = new Headers()
      headers.append("Authorization", `Token ${token}`);
      const upload = async function (file) {
        let formdata = new FormData();
        formdata.append("catalog_item", newItemID)
        formdata.append("file", file)
        let response = await fetch(`${process.env.VUE_APP_SERVER_URL}/api/files/`, {
          method: 'POST',
          headers: headers,
          body: formdata,
          redirect: 'follow'
        })
        return await response.json()
      }
      for (let file of this.files) {
        upload(file).then(response => console.log(response))
      }
    },
    addCatalogItemFormSubmit() {
      this.token = this.$cookies.get('mieletoken')
      fetch(`${process.env.VUE_APP_SERVER_URL}/api/catalog/`, {
        method: 'POST',
        redirect: "follow",
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${this.token}`,
        },
        body: JSON.stringify({
          title: this.formData.title,
          description: this.formData.description,
          article: this.formData.article,
          tags: [],
          files: [],
          previews: [],
          owner: this.owner
        })
      })
          .then(response => response.json())
          .then(response => {
            this.newItemID = response.id
            store.commit('setCatalog', this.token)
          })
          .then(() => {
            this.addTags()
          })
          .then(() => {
            this.uploadPreviews()
          })
          .then(() => {
            this.uploadFiles()
            //todo: fix cyrillic names error
          })
          .then(() => {
            this.showMessage = true
            store.commit('setCatalog', this.token)
          })
          .catch(error => {
            console.error(error)
            this.error = true
          })
    }
  },
  created() {
    this.token = this.$cookies.get('mieletoken')
    this.owner = store.getters.getUserInfo.id
    this.showMessage = false
    this.error = false
    this.screenWidth = screen.width
    fetch(`${process.env.VUE_APP_SERVER_URL}/api/tags/`, {
      method: 'GET',
      headers: {
        'Authorization': `Token ${this.token}`
      }
    })
        .then(response => response.json())
        .then(response => this.tags = response)
        .catch(error => console.error(error))
  }
}
</script>

<style scoped lang="scss">
@import "../../styles/variables";

.catalog {
  &-add {
    &__title {
      font-size: 40px;
      font-weight: 500;
    }

    &-form {
      border-top: 1px solid $main-lightgrey;
      padding-top: 70px;
      margin-top: 30px;

      @media screen and (max-width: 600px) {
        padding-top: 30px;
      }

      &__heading {
        font-size: 20px;
      }

      &-flex {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;

        @media screen and (max-width: 1000px) {
          flex-direction: column;
        }

        .half {
          width: 48%;

          @media screen and (max-width: 1000px) {
            width: 100%;
          }
        }
      }

      &-file {
        width: 48%;

        @media screen and (max-width: 1000px) {
          width: 100%;
        }
      }

      &-inputs {
        border: none;
        padding: 0;
        width: 48%;

        @media screen and (max-width: 1000px) {
          width: 99%;
        }
      }

      label {
        display: block;
        margin-bottom: 20px;
        margin-top: 30px;
        font-size: 20px;
      }

      input, textarea {
        background: $main-lightgrey;
        width: 100%;
        padding-left: 20px;
      }

      input {
        height: 50px;
      }

      textarea {
        height: 120px;
        padding: 20px;
      }

      &__button {
        font-size: 15px;
        font-weight: 600;
        width: 200px;

        @media screen and (max-width: 1000px) {
          width: 100%;
        }
      }

      &__cancel {
        text-decoration: none;
        color: $main-black;
      }

      #or {
        margin-left: 30px;
        color: $main-grey;
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

      &-file {
        position: relative;
      }

      &-buttons {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        margin-top: 50px;

        @media screen and (max-width: 1000px) {
          display: block;
        }

        label {
          margin: 0 0 0 15px;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          font-size: 15px;
          width: 200px;

          @media screen and (max-width: 1000px) {
            width: 100%;
            margin: 15px 0;
          }
        }
      }
    }

    .dragndrop {
      position: relative;

      &-area {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        min-height: 600px;
        border: 2px dashed #C4C4C4;
        text-align: center;
        color: #bdbdbd;
        font-size: 20px;

        @media screen and (max-width: 1000px) {
          min-height: unset;
          padding: 30px;
        }

        span {
          color: $main-red;
        }

        &__image {
          margin-top: 70px;
          width: 50%;
        }
      }

      &__input {
        position: absolute;
        opacity: 0;
      }

      &-previews {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr 1fr;
        gap: 16px;

        &-item {
          position: relative;
          display: block;

          &__image {
            height: 90px;
            object-fit: cover;
          }

          &__remove {
            position: absolute;
            top: 2px;
            right: 2px;
            background: #ffffff;
            height: 20px;
            width: 20px;
            display: block;
            border-radius: 50%;
            box-shadow: 0 0 0 1px $main-lightgrey;

            &:before {
              content: '\2715';
              color: $main-black;
            }
          }

          &__add {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
            margin: 0;
            cursor: pointer;
            background: $main-lightgrey;
            font-size: 36px;
          }
        }
      }
    }

    .dragndrop-area {
      transition-duration: .6s;

      &:hover {
        background: $main-lightgrey;
      }
    }

    .fileInput {
      position: absolute;
      opacity: 0;
      top: 100px;
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

}
</style>
