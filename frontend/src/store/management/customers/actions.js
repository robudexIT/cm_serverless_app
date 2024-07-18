// import API from '../../../api.js'
import API from '../../../api_awssam.js'
import store from '../../index.js'

export default {
    async fetchCustomerTotalCount(context,payload){
        const token = store.getters.getJwtToken
        const response = await fetch(API.getcustomerregisteredcount,{
          headers:{
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        
           },
           method: 'GET'
        })

        //if no token or token is expire logout the apps..
        if (response.status === 403){
          store.dispatch('autoLogout')
        }

        if(!response.ok){
            const error = new Error('Cannot fetch customer data')
            throw error
        }else{
            
            const data = await response.json()
            console.log('the  data is ')
            console.log(data)
            payload.data = data
            context.commit('mutCustomerCount', payload)
        }

    },

    async searchcustomer(context,payload){
      const token = store.getters.getJwtToken
      const response = await fetch(`${API.searchNumber.customerdetails}?customer_number=${payload.customer_number}`,{
        headers:{
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
      
         },
         method: 'GET'
      })

        //if no token or token is expire logout the apps..
        if (response.status === 403){
          store.dispatch('autoLogout')
        }

      if (!response.ok){
        const error = new Error('Cannot fetch customer data')
        throw error
      }else{
        const data = await response.json()

        if (typeof data === 'object' && Object.prototype.hasOwnProperty.call(data, 'message')) {
          // The variable is an object and has a property named 'message'
          // You can access the 'message' property like this:
          payload.data = []
       } else {
          // The variable is not an object or does not have a 'message' property
          payload.data = data
       }
      
  
        context.commit('mutCustomerSearch', payload)
      }
    },
    async deleteCustomer(context, payload){
      const token = store.getters.getJwtToken
      console.log('The payload is:')
      console.log(payload)
      const response = await fetch(API.deletecustomer,{
          method: 'DELETE',
          body: JSON.stringify(payload),
          headers:{
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        
           },
      })

        //if no token or token is expire logout the apps..
        if (response.status === 403){
          store.dispatch('autoLogout')
      }

      if(!response.ok){
          const error = new Error('Error in deleting customer')
          throw error
      }
      else{
      

          context.dispatch('searchcustomer',payload)
          context.dispatch('fetchCustomerTotalCount',{})
      }
  },
    
}
//INSERT INTO `customer_info`(`cid`, `customer_number`, `customer_name`, `updated_by`) VALUES ("2566","1234567890","James Bond","Rogmer Bulaclac"),("2577","1234567890","James Bond","Rogmer Bulaclac"),("2588","1234567890","James Bond","Rogmer Bulaclac"),("2599","1234567890","James Bond","Rogmer Bulaclac")
