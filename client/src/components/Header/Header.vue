<template>
  <header class="header">
    <div class="container">
      <div class="header-logo">
        <router-link to="/">
          <Logo />
        </router-link>
      </div>
      <div class="header-right">
        <div class="header-user">
          <p class="header-user__name" @click="showProfileActions = !showProfileActions">
            {{ user.first_name }}
          </p>
          <img class="header-user__avatar" :src="this.user.person.photo" :alt="this.user.person.first_name"
               @click="showProfileActions = !showProfileActions">
          <div class="header-user-actions" v-if="showProfileActions">
            <router-link :to="'/profile/' + getActualUserID()" class="header-user-actions__profile"
                         @click="showProfileActions = !showProfileActions">View profile
            </router-link>
            <p class="header-user-actions__logout" @click="logout">Logout</p>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import Logo from "@/components/Logo/Logo";
import CryptoJS from "crypto-js"
import store from "@/store"

export default {
  name: "Header",
  components: {Logo},
  data() {
    return {
      userID: this.$cookies.get('uid'),
      user: store.getters.getUserInfo,
      showProfileActions: false
    }
  },
  methods: {
    logout() {
      this.$cookies.remove('mieletoken')
      this.$router.push('/auth/')
    },
    getActualUserID() {
      let bytes = CryptoJS.AES.decrypt(this.$cookies.get('uid'), 'ID')
      return bytes.toString(CryptoJS.enc.Utf8)
    },
    getUserInfo() {
      fetch(`http://localhost:8000/api/users/${this.getActualUserID()}/`, {
        method: 'GET',
        headers: {
          'Authorization': `Token ${this.$cookies.get('mieletoken')}`
        }
      })
          .then(response => response.json())
          .then(response => {
                this.user = response
                if (!this.user.person.photo) {
                  this.user.person.photo = "/img/default_photo.jpg"
                }
                store.commit('setUserInfo', this.user)
              }
          )
          .catch(error => console.error(error))
    }
  },
  beforeMount() {
    this.getUserInfo()
  }
}
</script>

<style scoped lang="scss">
@import "../../styles/variables";

.header {
  margin-bottom: 50px;

  .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  &-user {
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;

    &__name {
      font-size: 14px;
      cursor: pointer;
    }

    &__avatar {
      margin-left: 16px;
      width: 40px;
      height: 40px;
      object-fit: cover;
      border-radius: 50px;
      padding: 2px;
      border: 2px solid $main-lightgrey;
      cursor: pointer;
    }

    &-actions {
      position: absolute;
      width: 100%;
      top: calc(100% + 20px);
      border: 1px solid $main-lightgrey;
      padding: 10px;
      font-size: 14px;

      &__profile {
        margin-bottom: 10px;
        text-decoration: none;
        color: inherit;
      }

      &__logout {
        cursor: pointer;
      }
    }
  }
}
</style>
