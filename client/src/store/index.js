import Vue from 'vue'
import Vuex from 'vuex'
import user from "./modules/user"
import catalog from "./modules/catalog";
import tag from "./modules/tag"
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        user,
        catalog,
        tag
    },
    plugins: [createPersistedState()],
})
