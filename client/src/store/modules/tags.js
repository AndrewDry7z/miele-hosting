export default {
    state: {
        chosenTag: null,
        tagsList: ''
    },
    mutations: {
        selectTag(state, tagId) {
            state.chosenTag = tagId
        },
        resetTag(state) {
            state.chosenTag = null
        },
        setTagsList(state, token) {
            fetch(`${process.env.VUE_APP_SERVER_URL}/api/tags/`, {
                method: 'GET',
                headers: {
                    'Authorization': `Token ${token}`
                }
            })
                .then(response => response.json())
                .then(response => state.tagsList = response)
                .catch(error => console.error(error))
        }
    },
    actions: {
        selectTag(context) {
            context.commit('selectTag')
        },
        resetTag(context) {
            context.commit('resetTag')
        },
        setTagsList(context) {
            context.commit('setTagsList')
        }
    },
    getters: {
        getSelectedTag(state) {
            return state.chosenTag
        },
        getTagsList(state) {
            return state.tagsList
        }
    }
}
