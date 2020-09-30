export default {
    state: {
        catalog: ''
    },
    mutations: {
        setCatalog(state, token) {
            fetch(`${process.env.VUE_APP_SERVER_URL}/api/catalog/`, {
                method: 'GET',
                headers: {
                    'Authorization': `Token ${token}`
                }
            })
                .then(response => response.json())
                .then(response => {
                        state.catalog = response
                    }
                )
                .catch(error => console.error(error))
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
