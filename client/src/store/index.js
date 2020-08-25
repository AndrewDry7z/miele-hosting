import Vue from 'vue'
import Vuex from 'vuex'
import user from "./modules/user"
import catalog from "./modules/catalog";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        user,
        catalog
    },
    plugins: [createPersistedState()],
})
