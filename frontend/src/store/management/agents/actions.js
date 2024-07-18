// import API from '../../../api.js'
import API from '../../../api_awssam.js'
import store from '../../index.js'


export default {
    async fetchAllAgents(context,payload){
        const agent = payload.agent
        const token = store.getters.getJwtToken
        const response = await fetch(`${API.agents.agent}/${agent}`,{
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
            const error = new Error('Cannot fetch ' + agent + ' data')
            throw error
        }else{
            
            const data = await response.json()
            payload.data = data
            context.commit('mutAgents', payload)
        }


    },
    async createAgent(context,payload){
        const agent = payload.agent
        const token = store.getters.getJwtToken
        console.log(agent)
        const response = await fetch(`${API.agents.agent}/${agent}`,{
            method: 'POST',
            headers:{
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            
            },
            body: JSON.stringify(payload.data)
        })
        //if no token or token is expire logout the apps..
        if (response.status === 403){
            store.dispatch('autoLogout')
        }

        if(!response.ok){
           
            const error = new Error('Error in creating new '  + agent + ' Agent')
            throw error
        }else{
            context.dispatch('fetchAllAgents',payload)
     
        }
    },
    async updateAgent(context, payload){
        const agent = payload.agent
        const token = store.getters.getJwtToken
        console.log(payload)
        const response = await fetch(`${API.agents.agent}/${agent}`,{
            method: 'PUT',
            headers:{
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            
            },
            body: JSON.stringify({'email': payload.data.email, 'extension': payload.data.extension,'name':payload.data.name})

        })
        //if no token or token is expire logout the apps..
        if (response.status === 403){
            store.dispatch('autoLogout')
        }
        
        if(!response.ok){
            const error = new Error('Error updating '+ agent+ ' agent  info')
            throw error
        }else{
          
           context.dispatch('fetchAllAgents',payload)
        }
    },
    async deleteAgent(context, payload){
        const agent = payload.agent
        const token = store.getters.getJwtToken
        const extension = payload.extension
        console.log(payload)
        const response = await fetch(`${API.agents.agent}/${agent}/${extension}`,{
            method: 'DELETE',
            headers:{
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            
            },            
            body: JSON.stringify(payload)
        })

        //if no token or token is expire logout the apps..
        if (response.status === 403){
            store.dispatch('autoLogout')
        }
        

        if(!response.ok){
            const error = new Error('Error in deleting ' +agent + 'Agent')
            throw error
        }else{
            // const data = await response.json()
            
            // payload.extension = data[0].extension
            // payload.method = 'delete'
           // context.commit('mutSingleAgent',payload)

            context.dispatch('fetchAllAgents',payload)
        }
    },
   async fetchAgentBelongsTo(context){
       const extension = context.rootGetters.getLoggedinUserData.extension
       const response = await fetch(`${API.getAgentBelongsTo}?extension=${extension}`)

        //if no token or token is expire logout the apps..
        if (response.status === 403){
            store.dispatch('autoLogout')
        }
       
       if(!response.ok){
           const error = new Error('Cannot info where is agent is belong')
           throw error
       }
       const data = await response.json()
       
       context.commit('mutAgentBelongsTo', data[0])
    },
  async udpateAgentBelongsTo(context, payload){
    const extension = context.rootGetters.getLoggedinUserData.extension
    const calltype = payload.calltype
    const body = {
        extension,
        calltype
    }
    console.log(body)
    const response  = await fetch(API.updateAgentBelongsTo, {
        method: 'POST',
        body: JSON.stringify(body)
    })

    //if no token or token is expire logout the apps..
    if (response.status === 403){
            store.dispatch('autoLogout')
     }
    
    if(!response.ok){
        const error = new Error('Cannot update agent calltype at this moment please try again later')
        throw error
    }

    const data = await response.json()

    console.log(data)
  }
}//
