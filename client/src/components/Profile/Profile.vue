<template>
  <main class="profile" :class="editMode ? 'edit' : ''" v-if="localUser">
    <div class="container">
      <div class="profile-flex">
        <div class="profile-photo">
          <img :src="localUser.person.photo" :alt="localUser.first_name">
        </div>
        <div class="profile-data">
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
      editMode: false
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
    }
  },
  beforeMount() {
    this.getUserInfo()
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
    align-items: center;
  }

  &-photo {
    margin-right: 100px;
    border-radius: 50%;
    max-width: 230px;

    img {
      border-radius: 50%;
      padding: 10px;
      border: 5px solid $main-lightgrey;
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
}
</style>
