import getters from './getters.js'
import mutations from './mutations.js'
import actions from './actions.js'

const csd = {
    namespaced : true,
    state(){
        return {
            phoneLoggedIn: [],
            phoneLoggedOut:[],
            agentPhoneLogsDetails:[] 
        }
    },
    getters,
    mutations,
    actions
}

export default csd