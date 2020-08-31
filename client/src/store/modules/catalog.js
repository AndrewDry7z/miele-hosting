export default {
    state: {
        catalog: ''
    },
    mutations: {
        setCatalog(state, token) {
            fetch('http://192.168.1.71:8000/api/catalog/', {
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
