<template>
  <main class="profile" :class="editMode ? 'edit' : ''" v-if="localUser">
    <div class="container">
      <div class="profile-flex">
        <div class="profile-photo">
          <img :src="localUser.person.photo" :alt="localUser.first_name" class="profile-photo__image">
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
            <select name="country" v-else class="profile-country__list" ref="select" v-model="localUser.person.country"
                    @change="selectCountry">
              <option v-for="(item, index) of this.countriesList" :value="item.id" :key="index">
                {{ item.countryname }}
              </option>
            </select>
          </div>
          <div class="profile-name">
            <input type="text" name="first_name" v-model="localUser.first_name" :readonly="!editMode"
                   class="profile-name__item" :size="localUser.first_name.length - 2"
                   ref="first_name">
            <button class="profile-name__trigger" @click="editName" v-if="isOwnPage()">
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
    </div>
  </main>
</template>

<script>
import store from '@/store'
import CryptoJS from "crypto-js";

export default {
  name: "Profile",
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
      currentCountry: ''
    }
  },
  methods: {
    editName() {
      this.editMode = !this.editMode
      this.$refs.first_name.focus()
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
        fetch(`http://localhost:8000/api/users/${this.$route.params.id}/`, {
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
            .catch(error => console.log(error))
      }
    },
    uploadPhoto(event) {
      let body = this.localUser
      body.person.photo = event.target.files[0] || event.dataTransfer.files
      fetch(`http://localhost:8000/api/users/${this.getActualUserID()}/update_user/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Authorization': `Token ${this.$cookies.get('mieletoken')}`
        },
        body: JSON.stringify(body)
      })
          .then(response => response.json())
          .then(response => {
                this.getUserInfo()
              }
          )
          .catch(error => console.log(error))
    },
    updateUserInfo() {
      fetch(`http://localhost:8000/api/person/${this.getActualUserID()}/`, {
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
          .catch(error => console.log(error))
      fetch(`http://localhost:8000/api/users/${this.getActualUserID()}/`, {
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
                console.log(response)
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
          .catch(error => console.log(error))
    },
    getCountriesList() {
      fetch(`http://localhost:8000/api/countries/`, {
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
          .catch(error => console.log(error))
    },
  },
  created() {
    this.getUserInfo()
    this.getCountriesList()
  }

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
    max-width: 230px;
    position: relative;

    &__image {
      border-radius: 50%;
      padding: 10px;
      border: 5px solid $main-lightgrey;
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
}
</style>
