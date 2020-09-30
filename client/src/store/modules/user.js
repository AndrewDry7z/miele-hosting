export default {
    state: {
        userInfo: ''
    },
    mutations: {
        setUserInfo(state, object) {
            state.userInfo = object
        },
        updateUserInfo(state, [token, id]) {
            fetch(`${process.env.VUE_APP_SERVER_URL}/api/users/${id}/`, {
                method: 'GET',
                headers: {
                    'Authorization': `Token ${token}`
                }
            })
                .then(response => response.json())
                .then(response => {
                        state.userInfo = response
                    }
                )
                .catch(error => console.error(error))
        }
    },
    actions: {
        setUserInfo(context) {
            context.commit('setUserInfo')
        },
        updateUserInfo(context) {
            context.commit('updateUserInfo')
        }
    },
    getters: {
        getUserInfo(state) {
            return state.userInfo
        }
    }
}
