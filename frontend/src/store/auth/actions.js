// import API from '../../api.js'
import API from '../../api_awssam.js'
let timer
export default {
    async loginUser(context,payload){
        const response =  await fetch(API.login,{
            method: 'POST',
            body: JSON.stringify(payload)
            
        })
         
        const data = await response.json() 
        console.log('jwt' in data)
        if(!response.ok ){
          
            const error = new Error('Invalid Extension or Password.Please Try again.')
            throw error
        }

        if(!('jwt' in data)){
            console.log('Error')
            const error = new Error('Invalid Extension or Password.Please Try again.')
            throw error
        }
        const expiresIn = 86400 * 1000
        const expirationDate = +new Date().getTime() + expiresIn
    
      
        const decodeJwt = JSON.parse(window.atob(data.jwt.split('.')[1]))
        const jwtToken =  data.jwt
        const loggedinUserData = decodeJwt.data

        localStorage.setItem('token', jwtToken)
        localStorage.setItem('loggedinUserData', JSON.stringify(loggedinUserData))
        localStorage.setItem('tokenExpiration', expirationDate)

        timer = setTimeout(function(){
            context.dispatch('autLogout')
        },expiresIn)

        context.commit('setUser',{jwtToken,loggedinUserData})
   
    },
    checkIfCurrentLogin(context){
        const jwtToken = localStorage.getItem('token')
        const loggedinUserData = JSON.parse(localStorage.getItem('loggedinUserData'))
        const tokenExpiration = localStorage.getItem('tokenExpiration')
        
        const expiresIn = +tokenExpiration - new Date().getTime()
        console.log(expiresIn)
        if(expiresIn < 0){
           return
        }

        //otherwise refresh the token 
        //implement later


        timer = setTimeout(function(){
            context.dispatch('autLogout')
        },expiresIn)

        if(jwtToken && loggedinUserData){
            context.commit('setUser',{jwtToken,loggedinUserData})
        }

        
    },
    logoutUser(context){
        localStorage.removeItem('token')
        localStorage.removeItem('loggedinUserData')
        localStorage.removeItem('tokenExpiration')

        clearTimeout(timer)

        context.commit('setUser' ,{
            jwtToken: null,
            loggedinUserData: null
        })
    },
    autoLogout(context){
        context.dispatch('logoutUser')
        context.commit('autoLogout')
    }
}