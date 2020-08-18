<template>
  <main class="profile" :class="editMode ? 'edit' : ''">
    <div class="container">
      <div class="profile-flex">
        <div class="profile-photo">
          <img :src="localUser.person.photo" :alt="localUser.last_name">
        </div>
        <div class="profile-data">
          <div class="profile-name">
            <input type="text" name="first_name" v-model="localUser.first_name" :readonly="!editMode"
                   class="profile-name__item" :size="localUser.first_name.length - 2"
                   ref="first_name">
            <input type="text" name="last_name" v-model="localUser.last_name" :readonly="!editMode"
                   class="profile-name__item" :size="localUser.last_name.length - 3">
            <button class="profile-name__trigger" @click="editName">
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

export default {
  name: "Profile",
  data() {
    return {
      user: store.getters.getUserInfo,
      localUser: store.getters.getUserInfo,
      editMode: false
    }
  },
  methods: {
    editName() {
      this.editMode = !this.editMode
      this.$refs.first_name.focus()
    }
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
