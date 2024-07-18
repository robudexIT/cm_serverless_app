// import API from '../../api.js'
import API from '../../api_awssam.js'
import store from '../index.js'
export default {
   async fetchPhoneStatus(context,payload){
        let phoneApi;
        const token = store.getters.getJwtToken
        
        console.log(payload.phone)
        if(payload.phone == 'loggedin'){
            phoneApi = API.agents.phoneLoggedIn
        }else if(payload.phone == 'loggedout'){
            phoneApi = API.agents.phoneLogggedOut
        }
       
        const response = await fetch(phoneApi,{
            method: 'GET',     
            headers:{
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
            }
        })
       
        //if no token or token is expire logout the apps..
        if (response.status === 403){
            store.dispatch('autoLogout')
        }        
       
        if(!response.ok ){
            const error =  Error('Error in Fetching PhoneUser Status')
            throw  error
        }
        const data = await response.json()
        console.log(data)
        //data array to payload object
        payload.data  = data.map(d => {
            d.loginlogout = d.loginlogout.split('?')[1]
            return d
        })
        context.commit('getPhoneStatus', payload)

    },
    async agentPhoneLogsDetails(context, payload){
        const querystring = payload.querystring
        console.log(querystring)
        const token = store.getters.getJwtToken
        const response = await fetch(`${API.agents.phoneLogsDetails}?${querystring}`,{
            method: 'GET',     
            headers:{
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
            }       
         })
       
        //if no token or token is expire logout the apps..
        if (response.status === 403){
            store.dispatch('autoLogout')
        }

        if(!response.ok){
            const error = new Error('Error in Accessing Agent Phone Logs Details')
            throw error
        }else{
           
            const data = await response.json()
            console.log(data)
            context.commit('mutagentPhoneLogsDetails', data)
        }
    }
   
}