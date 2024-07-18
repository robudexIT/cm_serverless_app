export default {
    getPhoneStatus(state,payload){
        if(payload.phone == 'loggedin'){
            state.phoneLoggedIn = payload.data
        }else if(payload.phone == 'loggedout'){
            state.phoneLoggedOut = payload.data
        }
       
    },
    mutagentPhoneLogsDetails(state,payload){
        state.agentPhoneLogsDetails = payload
    }
}