<template>
  <main class="auth">
    <section class="auth-flex">
      <div class="auth-flex-image" v-if="screenWidth > 1200">
        <picture>
          <source srcset="../../assets/images/auth_bg@2x.webp"
                  type="image/webp">
          <img src="../../assets/images/auth_bg@2x.jpg" alt="Auth">
        </picture>
      </div>
      <div class="auth-flex-content">
        <div class="wrapper" :class="loginMode ? 'login' : ''">
          <h1 class="auth__title" v-if="loginMode">Sign in</h1>
          <h1 class="auth__title" v-else>Sign up to</h1>
          <div class="auth-error" v-if="showAuthError">
            <p>Authentication failed.</p>
            <p>The e-mail or password you entered is incorrect.</p>
          </div>
          <form class="auth-form" @submit.prevent="loginMode ? login() : register()">
            <div class="auth-form-grid">
              <div v-if="!loginMode">
                <label for="fullname">Full name</label>
                <input type="text" id="fullname" placeholder="Full name" class="auth-form__input"
                       required v-model="input.fullname">
              </div>
              <div v-if="!loginMode">
                <label for="phone">Phone</label>
                <input type="text" id="phone" placeholder="Phone" class="auth-form__input"
                       required v-model="input.phone">
              </div>
              <div>
                <label for="email">Email address</label>
                <input type="email" id="email" autocomplete="username" placeholder="E-mail" class="auth-form__input"
                       required v-model="input.email">
              </div>
              <div>
                <label for="password">Password</label>
                <input type="password" autocomplete="current-password" minlength="" id="password"
                       :placeholder="loginMode ? '' : '6+ characters'"
                       class="auth-form__input"
                       required v-model="input.password">
              </div>
            </div>

            <router-link class="auth-form__forgot" to="#" v-if="loginMode">Forgot password?</router-link>
            <div class="auth-form__checkbox" v-else>
              <input type="checkbox" name="agree" id="agree" required>
              <label for="agree">I agree to <a href="#">Miele Terms</a> and <a href="#">Privacy Policy</a>.</label>
            </div>
            <button class="auth-form__submit button--red" v-if="loginMode">Sign In</button>
            <button class="auth-form__submit button--red" v-else>Create Account</button>
          </form>
          <div class="auth__changeMode" v-if="loginMode">
            Not a member? <span @click="toggleLoginMode">Sign up now</span>
          </div>
          <div class="auth__changeMode" v-else>
            Already a member? <span @click="toggleLoginMode">Sign In</span>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import CryptoJS from 'crypto-js'

export default {
  name: "Auth",
  data() {
    return {
      input: {
        email: null,
        password: null,
        fullname: null,
        phone: null
      },
      screenWidth: null,
      showAuthError: false,
      loginMode: true,
      token: null
    }
  },
  created() {
    if (this.$cookies.isKey('mieletoken')) {
      this.$router.push('/')
    }
  },
  methods: {
    login() {
      fetch(`https://miele-hosting.herokuapp.com/auth/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: this.input.email,
          password: this.input.password
        })
      })
          .then(response => response.json())
          .then(response => {
            this.token = response.token
            let userIdEncrypted = CryptoJS.AES.encrypt(response.user.id.toString(), "ID").toString()
            this.$cookies.set('uid', userIdEncrypted, '30d')
            this.$cookies.set('mieletoken', response.token, "30d")
          })
          .then(() => {
            if (this.token === undefined) {
              this.showAuthError = true
            } else {
              this.$router.push('/')
            }
          })
    },
    register() {
      fetch(`https://miele-hosting.herokuapp.com/api/users/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: this.input.email,
          password: this.input.password,
          email: this.input.email,
          first_name: this.input.fullname,
          person: {
            phone: this.input.phone,
            skype: null,
            photo: null,
            country: null
          }
        })
      })
          .then(() => {
            this.login()
          })
    },
    getWindowWidth() {
      this.screenWidth = screen.width
    },
    toggleLoginMode() {
      this.loginMode = !this.loginMode
    }
  },
  mounted() {
    this.getWindowWidth()
  }
}
</script>

<style scoped lang="scss">
@import "../../styles/variables";

.auth {
  &-flex {
    display: flex;

    &-image {
      width: 50%;
      z-index: -1;
      @media screen and (max-width: 1200px) {
        display: none;
      }

      img {
        width: 100%;
        min-height: 100vh;
        object-fit: cover;
      }
    }

    &-content {
      width: 50%;
      padding: 140px;

      @media screen and (max-width: 1200px) {
        width: 100%;
        padding: 40px;
      }

    }
  }

  &__title {
    font-size: 40px;
    font-weight: 600;
    margin-bottom: 45px;
  }

  &-form {
    &-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      grid-column-gap: 15px;
      grid-row-gap: 15px;
      border: none;
      padding: 0;
    }

    label {
      display: block;
      margin-bottom: 10px;
    }

    &__input {
      display: block;
      background: $main-lightgrey;
      height: 40px;
      padding-left: 20px;
      width: 100%;
    }

    &__submit {
      height: 38px;
      margin-top: 30px;
    }

    &__forgot {
      text-decoration: none;
      color: $main-blue;
    }

    &__checkbox {
      display: flex;
      align-items: center;
      margin-top: 15px;

      input {
        margin: 0 5px 0 0;
      }

      label {
        margin: 0;
        color: $main-darkgrey;

        a {
          text-decoration: none;
          color: $main-blue;
        }
      }
    }
  }

  .wrapper {
    max-width: 455px;


    &.login {
      max-width: 350px;
    }
  }

  &-error {
    margin-bottom: 50px;
    padding: 20px;
    border: 2px solid $main-red
  }

  &__changeMode {
    margin-top: 35px;
    padding-top: 30px;
    border-top: 1px solid $main-lightgrey;
    color: $main-grey;

    span {
      color: $main-blue;
      cursor: pointer;
    }
  }
}

</style>
