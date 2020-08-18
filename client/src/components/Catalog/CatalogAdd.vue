<template>
  <main class="catalog-add">
    <div class="container">
      <h1 class="catalog-add__title">
        Add files
      </h1>
      <form class="catalog-add-form" @submit.prevent="addFileFormSubmit()" enctype="multipart/form-data">
        <p class="catalog-add-form__heading">
          Upload files
        </p>
        <div class="catalog-add-form-flex">
          <div class="catalog-add-form-file">
            <label class="dragndrop-area" ref="fileform" for="fileInput" v-cloak @drop.prevent="addFile"
                   @dragover.prevent>
              Drag and Drop here <br />
              or <br />
              <span>Browse files</span>
              <img src="../../assets/images/drag-n-drop.svg"
                   class="dragndrop-area__image"
                   alt="Drag N Drop Files Here">
            </label>
            <input type="file" id="fileInput" name="files[]" multiple class="fileInput" @change="clickAddFile($event)">
            <ul class="dragndrop-preview">
              <li v-for="(file, index) in files" :key="index">
                {{ file.name }}
                <button @click="removeFile(file)" title="Remove">X</button>
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

            <div class="catalog-add-form-tags">
              <div class="catalog-add-form-tags-item" v-for="(tag, index) of selectedTags" :key="index">
                {{ tag }}
                <span class="catalog-add-form-tags-item__close" @click="$delete(selectedTags, index)"></span>
              </div>
            </div>

            <button type="submit" class="button--red catalog-add-form__button">
              + Add files
            </button>
            <span id="or">or </span>
            <router-link to="/" class="catalog-add-form__cancel">Cancel</router-link>
          </fieldset>
        </div>
      </form>
    </div>
  </main>
</template>

<script>

export default {

  name: "CatalogAdd",
  components: {},
  data() {
    return {
      tags: [],
      selectedTags: [],
      tagInput: null,
      files: [],
      formData: {
        title: '',
        description: '',
        article: '',
        owner: 1
      },
      token: this.$cookies.get('mieletoken')
    }
  },
  methods: {
    selectTag() {
      this.selectedTags.push(this.tagInput)
      this.tagInput = null
    },
    addFile(e) {
      let droppedFiles = e.dataTransfer.files;
      if (!droppedFiles) return;
      ([...droppedFiles]).forEach(f => {
        this.files.push(f);
      });
    },
    clickAddFile(event) {
      let droppedFiles = event.target.files;
      if (!droppedFiles) return;
      ([...droppedFiles]).forEach(f => {
        this.files.push(f);
      });
    },
    removeFile(file) {
      this.files = this.files.filter(f => {
        return f != file;
      });
    },
    addFileFormSubmit() {
      this.token = this.$cookies.get('mieletoken')
      fetch(`http://localhost:8000/api/catalog/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${this.token}`
        },
        body: JSON.stringify({
          title: this.formData.title,
          description: this.formData.description,
          article: this.formData.article,
          tags: this.selectedTags,
          files: this.files,
          owner: this.formData.owner
        })
      })
          .then(response => response.json())
          .then(response => console.log(response))
          .catch(error => console.log(error))
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

.catalog {
  &-add {
    &-form {
      border-top: 1px solid $main-lightgrey;
      padding-top: 70px;
      margin-top: 30px;

      &__heading {
        font-size: 20px;
      }

      &-flex {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;

        .half {
          width: 48%;
        }
      }

      &-file {
        width: 48%;
      }

      &-inputs {
        border: none;
        padding: 0;
        width: 48%;
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
        margin-top: 50px;
        font-size: 15px;
        font-weight: 600;
        display: inline-block;
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

        span {
          color: $main-red;
        }

        &__image {
          margin-top: 70px;
        }
      }

      &__input {
        position: absolute;
        opacity: 0;
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
  }

}
</style>
