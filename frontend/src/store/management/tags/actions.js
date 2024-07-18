//import API from '../../../api.js'
import store from '../../index.js'
import API from '../../../api_awssam.js'

export default {
    async fetchAllTags(context){
        const token = store.getters.getJwtToken
        const response = await fetch(API.tags, {
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
            const error = new Error('Cannot Fetch Tags')
            throw error
        }else{
            const data = await response.json()
            context.commit('mutAllTags', data)
        }
    },
    async createTag(context, payload){
        const token = store.getters.getJwtToken
        console.log(payload)
        const response = await fetch(`${API.tags}/${payload.tagtype.toLowerCase()}`,{
            method: 'POST',
            headers:{
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
               } ,            
            body: JSON.stringify(payload)
        })
        console.log('test')
        const data = response.json()
        console.log(data)

        //if no token or token is expire logout the apps..
        if (response.status === 403){
            store.dispatch('autoLogout')
        }        

        if(!response.ok){
            const error = new Error('Unable to create new Tag. Please Check if Tag was already exists')
            throw error
        }else{
            context.dispatch('fetchAllTags')
            alert('New Tag Added..')
            
        }
    },
    async deleteTag(context,payload){
        const token = store.getters.getJwtToken
        console.log(payload)
        const response = await fetch(API.tags,{
            method:'DELETE',
            headers:{
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
               } ,                
            body: JSON.stringify(payload)
        })

        //if no token or token is expire logout the apps..
        if (response.status === 403){
            store.dispatch('autoLogout')
        }

        if(!response.ok){
            const error = new Error('Unable to delete tag')
            throw error
        }else{
            context.dispatch('fetchAllTags')
        }
    }
}