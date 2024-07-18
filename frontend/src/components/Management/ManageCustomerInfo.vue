<template>
    <base-dialog :show="!!error" @close="handleError">
     <p>{{error}}</p>
   </base-dialog>
    <base-container>
        <div v-if="isLoading">
            <base-dialoag :show="isLoading">
                <base-spinner>
                     <p>Fetching Data From the Database Please Wait....</p>
                </base-spinner>
            </base-dialoag>
        </div>
        <div v-else>
            <div>
                <p style="color: blue; font-weight: bold; font-size: 20px;">Total Customer Registered: <span style="color: red;">{{customerTotalCounts}}</span></p>
            </div>
            <base-table theader="customerinfo" tableclass='customerinfo'>
                <!-- <agents-data-list :tdata="allAgents" @click="deleteAgent" :agent="agent" @emittedData="updateAgent"></agents-data-list> -->
                <template v-slot:default  v-if="customerDetails.length !== 0">
                   <customer-data-list :tdata="customerDetails" @click="deleteCustomer"></customer-data-list>
                </template>
                <template v-slot:default  v-else>
                   <h1 style="color:green">No Search Result</h1>
               </template>
            </base-table>
            <customer-modal-form
                modalId="modalCustomerInfo"
                modalTitle="Search Customer"
                formId="searchCustomer"
                formMethod="GET"
                @emittedCustomerData="fetchCustomerDetails"
            
            > </customer-modal-form>
         
            <button type="button" class="btn btn-dark" data-bs-toggle="modal" :data-bs-target="dataBsTarget" dataset-backdrop="static" dataset-keyboard="false" id="add_tag">
                CUSTOMER SEARCH
        </button>
         
       </div>
    </base-container>

</template>

<script>

import CustomerDataList from '../../components/Management/data/CustomerDataList.vue'
import CustomerModalForm from './modal/CustomerModalForm.vue'

export default {
  emits:['emittedData'],
  data(){
      return {
          dataBsTarget: '#modalCustomerInfo',
          isLoading: false,
          error: null,
          appName: this.$store.getters.getAppName
      }
  },
  components:{
      CustomerDataList,
      CustomerModalForm
     
  },
  methods: {
    async fetchCustomerTotalCounts(){
            try{
             this.isLoading = true
             await  this.$store.dispatch('customer/fetchCustomerTotalCount',{})
             this.isLoading = false
             
          }catch(e){
              this.error = e.message
          }
     },
     async fetchCustomerDetails(data){
        try {
            this.isLoading = true

            await  this.$store.dispatch('customer/searchcustomer',data)
            this.isLoading = false
        }catch(e){
            this.error = e.message
        }
     },
     async deleteCustomer(data){
        try{
            this.isLoading = true
            await this.$store.dispatch('customer/deleteCustomer',data)
            this.isLoading = false
        }catch(e){
            this.error = e.message
        }
     }
  },
  computed: {
     customerTotalCounts(){
        let customer_count = this.$store.getters['customer/getCustomerTotalCount']
         return customer_count
     }, 
     customerDetails(){
        let customer_details = this.$store.getters['customer/getCustomerDetails']
        console.log(customer_details)
        return customer_details
     }
      
  },
  created(){
     this.fetchCustomerTotalCounts()
      
  },
 
  watch:{
      
  }
}
</script>