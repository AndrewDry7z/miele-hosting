export default {
    state: {
        chosenTag: null
    },
    mutations: {
        selectTag(state, tagId) {
            state.chosenTag = tagId
        },
        resetTag(state) {
            state.chosenTag = null
        }
    },
    actions: {
        selectTag(context) {
            context.commit('selectTag')
        },
        resetTag(context) {
            context.commit('resetTag')
        }
    },
    getters: {
        getSelectedTag(state) {
            return state.chosenTag
        }
    }
}
