export default {
    setUser(state, payload){
        //data: {extension: "6336", name: "Rogmer Bulaclac", position: "1", blended: "0", calltype: "collection"
        // const decodeJwt = JSON.parse(window.atob(payload.jwt.split('.')[1]))
        state.jwtToken =  payload.jwtToken
        state.loggedinUserData = payload.loggedinUserData
        state.autoLogout = false

    },
    setAutoLogout(state){
        state.autoLogout = true
    }
}