export default {
    state: {
        userInfo: ''
    },
    mutations: {
        setUserInfo(state, object) {
            state.userInfo = object
        }
    },
    actions: {
        setUserInfo(context) {
            context.commit('setUserInfo')
        },
    },
    getters: {
        getUserInfo(state) {
            return state.userInfo
        }
    }
}
