export default {

    getJwtToken(state){
        return state.jwtToken
    },
    getLoggedinUserData(state){
       // {extension: "6336", name: "Rogmer Bulaclac", position: "1", blended: "0", calltype: "collection"
        return state.loggedinUserData
    },
    hasToken(state){
        return !!state.jwtToken
    },
    getAutoLogoutStatus(state){
        return state.autoLogout
    }
}