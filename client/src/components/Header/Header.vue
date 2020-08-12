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
            {{ user.first_name }} {{ user.last_name }}
          </p>
          <img class="header-user__avatar" src="../../assets/images/default_photo.jpg" alt=""
               @click="showProfileActions = !showProfileActions">
          <div class="header-user-actions" v-if="showProfileActions">
            <p class="header-user-actions__profile">View profile</p>
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

export default {
  name: "Header",
  components: {Logo},
  data() {
    return {
      userID: this.$cookies.get('uid'),
      user: '',
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
      fetch(`https://miele-hosting.herokuapp.com/api/users/${this.getActualUserID()}/`, {
        method: 'GET',
        headers: {
          'Authorization': `Token ${this.$cookies.get('mieletoken')}`
        }
      })
          .then(response => response.json())
          .then(response => {
                this.user = response
              }
          )
          .catch(error => console.log(error))
    }
  },
  created() {
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
        cursor: pointer;
      }

      &__logout {
        cursor: pointer;
      }
    }
  }
}
</style>
