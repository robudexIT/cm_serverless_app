export default {
  mutCustomerCount(state, payload){
    state.CustomerTotalCount = payload.data.customer_registered_count
    },
    mutCustomerSearch(state, payload){

      state.customerDetails = payload.data
    }  
    
}