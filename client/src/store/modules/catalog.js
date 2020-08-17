export default {
    state: {
        catalog: ''
    },
    mutations: {
        setCatalog(state, object) {
            state.catalog = object
        }
    },
    actions: {
        setCatalog(context) {
            context.commit('setCatalog')
        },
    },
    getters: {
        getCatalog(state) {
            return state.catalog
        }
    }
}
