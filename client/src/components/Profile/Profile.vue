<template>
  <main class="profile" :class="editMode ? 'edit' : ''" v-if="localUser">
    <div class="container">
      <div class="profile-flex">
        <div class="profile-photo">
          <img :src="this.localUser.person.photo" :alt="localUser.first_name" class="profile-photo__image">
          <label for="uploadPhoto" class="profile-photo-upload" v-if="isOwnPage()">
            <input type="file" accept="image/jpeg, image/png" class="profile-photo-upload__input" id="uploadPhoto"
                   @change="uploadPhoto($event)">
          </label>
        </div>
        <div class="profile-data">
          <div class="profile-error" v-if="this.error">
            {{ error.errorText }}
          </div>
          <div class="profile-country">
            <img :src="this.currentCountry.flag" :alt="this.currentCountry.code" class="profile-country__flag"
                 v-if="!editMode">
            <div class="profile-country__name grey" v-if="!editMode">
              {{ this.currentCountry.countryname }}
            </div>
            <select name="country" v-else class="profile-country__list" ref="select" v-model="localUser.person.country">
              <option v-for="(item, index) of this.countriesList" :value="item.id" :key="index">
                {{ item.countryname }}
              </option>
            </select>
          </div>
          <div class="profile-name">
            <input type="text" name="first_name" v-model="localUser.first_name" :readonly="!editMode"
                   class="profile-name__item" :size="localUser.first_name.length - 2"
                   ref="first_name">
            <button class="profile-name__trigger" @click="editUserInfo" v-if="isOwnPage()">
              <img src="../../assets/images/icons/pencil-black.svg" alt="Edit">
            </button>
          </div>
          <div class="profile-contacts">
            <label class="profile-contacts-item">
              E-mail address:
              <input type="email" class="profile-contacts-item__input" v-model="localUser.email"
                     :size="localUser.email.length" :readonly="!editMode">
            </label>
            <label class="profile-contacts-item">
              Phone:
              <input type="tel" class="profile-contacts-item__input" v-model="localUser.person.phone"
                     :readonly="!editMode">
            </label>
            <label class="profile-contacts-item">
              Skype:
              <input type="text" class="profile-contacts-item__input" v-model="localUser.person.skype"
                     :readonly="!editMode">
            </label>
          </div>
          <button class="button--red" @click="updateUserInfo()" v-if="editMode">Save</button>
        </div>
      </div>
      <div class="profile-files">
        <h2 class="profile-files__title" v-if="this.catalogFilteredByUser.length < 1">No files yet</h2>
        <h2 class="profile-files__title" v-else-if="isOwnPage()">My files</h2>
        <h2 class="profile-files__title" v-else>Files</h2>
        <div class="catalog-grid">
          <CatalogItem
              v-for="item in catalogFilteredByUser"
              :key="item.id"
              :id="item.id"
              :title="item.title"
              :article="item.article"
              :description="item.description"
              :previews="item.previews"
              @item-selected="itemSelected(item.id)"
          />
        </div>
      </div>
      <CatalogDetails
          :item="selectedItem"
          @close-details="closeDetails()"
          @overlay-click="overlayClick($event)"
      />
    </div>
  </main>
</template>

<script>
import store from '@/store'
import CryptoJS from "crypto-js";
import CatalogItem from "@/components/Catalog/CatalogItem";
import CatalogDetails from "@/components/Catalog/CatalogDetails";

export default {
  name: "Profile",
  components: {CatalogDetails, CatalogItem},
  data() {
    return {
      user: null,
      localUser: null,
      editMode: false,
      error: {
        isError: false,
        errorText: ''
      },
      countriesList: '',
      currentCountry: '',
      selectedItem: null,
      catalog: store.getters.getCatalog,
      catalogFilteredByUser: null
    }
  },
  methods: {
    editUserInfo() {
      this.editMode = !this.editMode
      this.$refs.first_name.focus()
      this.localUser = this.user
    },
    getActualUserID() {
      let bytes = CryptoJS.AES.decrypt(this.$cookies.get('uid'), 'ID')
      return bytes.toString(CryptoJS.enc.Utf8)
    },
    isOwnPage() {
      return (this.$route.params.id === this.getActualUserID())
    },
    getUserInfo() {
      if (this.isOwnPage()) {
        this.user = store.getters.getUserInfo
        this.localUser = this.user
      } else {
        fetch(`http://192.168.1.71:8000/api/users/${this.$route.params.id}/`, {
          method: 'GET',
          headers: {
            'Authorization': `Token ${this.$cookies.get('mieletoken')}`
          }
        })
            .then(response => response.json())
            .then(response => {
                  this.localUser = response
                  if (!this.localUser.person.photo) {
                    this.localUser.person.photo = "/img/default_photo.jpg"
                  }
                }
            )
            .catch(error => console.error(error))
      }
    },
    uploadPhoto(event) {
      let newPhoto = event.target.files[0] || event.dataTransfer.files
      fetch(`http://192.168.1.71:8000/api/person/${this.getActualUserID()}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Token ${this.$cookies.get('mieletoken')}`,
        },
        body: {
          photo: newPhoto
        }
      })
          .then(response => response.json())
          .then(response => {
                console.log(newPhoto)
                console.log(response)
                this.getUserInfo()
              }
          )
          .catch(error => console.error(error))
    },
    updateUserInfo() {
      fetch(`http://192.168.1.71:8000/api/person/${this.getActualUserID()}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${this.$cookies.get('mieletoken')}`
        },
        body: JSON.stringify({
          phone: this.localUser.phone,
          skype: this.localUser.skype,
          country: this.localUser.country
        })
      })
          .catch(error => console.error(error))
      fetch(`http://192.168.1.71:8000/api/users/${this.getActualUserID()}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${this.$cookies.get('mieletoken')}`
        },
        body: JSON.stringify({
          first_name: this.localUser.first_name,
          email: this.localUser.email
        })
      })
          .then((response) => {
                switch (response.status) {
                  case 400:
                    this.error.isError = true
                    this.error.errorText = 'Data you entered is not valid'
                    break;
                  case 500:
                    this.error.isError = true
                    this.error.errorText = 'Server internal error. Please try again later'
                    break;
                  case 200:
                    this.error.isError = false
                    this.editMode = false
                    store.commit('setUserInfo', this.localUser)
                    this.getUserInfo()
                    this.getCountriesList()
                    break;
                  default:
                    this.error.isError = true
                    this.error.errorText = `Something is wrong. Code ${response.status}. Please contact site admin`
                }
              }
          )
          .catch(error => console.error(error))
    },
    getCountriesList() {
      fetch(`http://192.168.1.71:8000/api/countries/`, {
        method: 'GET',
        headers: {
          'Authorization': `Token ${this.$cookies.get('mieletoken')}`
        }
      })
          .then(response => response.json())
          .then(response => {
                this.countriesList = response
                this.currentCountry = this.countriesList.filter(item => item.id === this.localUser.person.country)[0]
              }
          )
          .catch(error => console.error(error))
    },
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
    filterCatalogByUser() {
      this.catalogFilteredByUser = this.catalog.filter(item => item.owner.id.toString() === this.$route.params.id)
    }
  },
  created() {
    this.getUserInfo()
    this.getCountriesList()
    this.filterCatalogByUser()
  },
  watch: {
    '$route.params.id': function () {
      this.getUserInfo()
      this.filterCatalogByUser()
    }
  },
}
</script>

<style scoped lang="scss">
@import "../../styles/variables";

.profile {
  &.edit {
    .profile-name__item {
      border-bottom: 1px solid $main-darkgrey;
    }

    .profile-contacts-item {
      border-color: $main-darkgrey;
    }
  }

  &-flex {
    display: flex;
    align-items: flex-start;
  }

  &-photo {
    margin-right: 100px;
    border-radius: 50%;
    width: 230px;
    height: 230px;
    position: relative;

    &__image {
      border-radius: 50%;
      padding: 10px;
      border: 5px solid $main-lightgrey;
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    &-upload {
      position: absolute;
      right: 0;
      bottom: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;

      &:after {
        content: url("../../assets/images/icons/pencil-white.svg");
        background: $main-red;
        padding: 16px;
        border: 10px solid #fff;
        border-radius: 50%;
        height: 70px;
        width: 70px;
        cursor: pointer;
      }

      &__input {
        opacity: 0;
        position: absolute;
        z-index: -1;
      }
    }
  }

  &-name {
    margin-bottom: 50px;

    &__item {
      display: inline-block;
      font-size: 40px;
      border-bottom: 1px solid transparent;

      &:first-child {
        margin-right: 20px;
      }
    }

    &__trigger {
      margin-left: 20px;
    }
  }

  &-contacts {
    &-item {
      display: block;
      padding-bottom: 12px;
      margin-bottom: 20px;
      border-bottom: 1px solid $main-lightgrey;
      width: 450px;

      &__input {
        width: 290px;
        display: inline-block;
        margin-left: auto;
      }
    }
  }

  &-country {
    display: flex;
    margin-bottom: 16px;

    &__flag {
      width: 16px;
      border-radius: 50%;
      border: 2px solid $main-lightgrey;
      margin-right: 10px;
    }

    &__name {
    }
  }

  &-files {
    &__title {
      font-size: 28px;
      margin-bottom: 30px;
    }
  }
}
</style>