import getters from './getters.js'
import mutations from './mutations.js'
import actions from './actions.js'

const auth = {
    // namespaced:true,
    state(){
        return {
           jwtToken: null,
           loggedinUserData: null,
           autoLogout: false
        }
    },
    getters,
    mutations,
    actions
}

export default auth