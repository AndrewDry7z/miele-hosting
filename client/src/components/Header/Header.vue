<template>
  <header class="header">
    <div class="container">
      <div class="header-logo">
        <router-link to="/">
          <Logo />
        </router-link>
      </div>
      <div class="header-right">
        <div class="header-user" v-if="user">
          <p class="header-user__name" @click="showProfileActions = !showProfileActions">
            {{ user.first_name }}
          </p>
          <img class="header-user__avatar" :src="user.person.photo" :alt="user.person.first_name"
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
    clickOutside() {
      window.addEventListener('click', event => {
        if (event.target.parentNode) {
          if (!event.target.parentNode.classList.contains('header-user')) {
            this.showProfileActions = false
          }
        }
      })
    },
    getActualUserID() {
      let bytes = CryptoJS.AES.decrypt(this.$cookies.get('uid'), 'ID')
      return bytes.toString(CryptoJS.enc.Utf8)
    },
    getUserInfo() {
      fetch(`${process.env.VUE_APP_SERVER_URL}/api/users/${this.getActualUserID()}/`, {
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
  created() {
    this.clickOutside()
  },
  beforeMount() {
    this.getUserInfo()
  },
  watch: {
    '$route'(to, from) {
      if (to !== from) {
        this.showProfileActions = false
      }
    }
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

    @media screen and (max-width: 600px) {
      justify-content: center;
      position: relative;
    }
  }

  &-right {
    @media screen and (max-width: 600px) {
      position: absolute;
      right: 5px;
    }
  }

  &-user {
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;

    &__name {
      font-size: 14px;
      cursor: pointer;
      @media screen and (max-width: 600px) {
        display: none;
      }
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
      width: 180px;
      top: calc(100% + 20px);
      border: 1px solid $main-lightgrey;
      padding: 10px;
      font-size: 14px;
      background: #ffffff;
      z-index: 10;

      @media screen and (max-width: 600px) {
        width: 250px;
      }

      &__profile {
        margin-bottom: 10px;
        text-decoration: none;
        color: inherit;

        @media screen and (max-width: 600px) {
          margin-bottom: 20px;
          display: block;
        }
      }

      &__logout {
        cursor: pointer;
      }
    }
  }
}
</style>
