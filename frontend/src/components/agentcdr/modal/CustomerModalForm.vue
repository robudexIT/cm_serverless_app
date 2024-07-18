<template>
    <!-- <div>{{details}}</div> -->
    <div class="modal fade"  id="customerModalFormId" role="dialog">
    <div class="modal-dialog">

      <!-- Modal content-->
      <div class="modal-content">
        <div class="modal-header">

          <h4 class="modal-title">Customer Details</h4>
        </div>
        <div class="modal-body">
          <form method="POST"  id="customer_form_id" @submit.prevent="submitFromData">
              <div :class="errorDiv">
                <p class="errorP"  v-if="!formIsValid">Please Make Sure That Dont Leave Blank on the Input Fields</p>  
                <p v-if="customer_id != '' &&  customer_name != ''" >Updated By: <span style="font-weight: bold; color: blue;">{{updated_by}}</span></p>
                <div class="form-group">
                  <label for="customerNumber">Customer Number:</label>
                  <input  v-if="calltype=='csdinbounddetails' || calltype=='missedcallsdetails' || calltype=='csdoutbounddetails' || calltype=='collectiondetails' "  type="text" class="form-control" id="customerNumber" placeholder="Enter Customer Number" :value="customer_number" disabled>
                  <input  v-else type="text" class="form-control" id="customerNumber" placeholder="NOT YET REGISTER" :value="customer_number" disabled>
                </div>
                <div class="form-group">
                  <label for="customerID">Customer ID:</label>
                  <!-- :value="customer_id" @change="setNewCustomerId" -->
                  <input v-if="calltype=='csdinbounddetails' || calltype=='missedcallsdetails' || calltype=='csdoutbounddetails' || calltype=='collectiondetails'" type="text" class="form-control" id="customerID" placeholder="Enter Customer ID" v-model="new_customer_id"  > 
                  <input v-else type="text" class="form-control" id="customerID" placeholder="NOT YET REGISTER" v-model="new_customer_id" disabled > 
                </div>
                <div class="form-group">
                  <label for="customerName">Customer Name:</label>
                  <!-- :value ="customer_name" @change="setNewCustomerName" -->
                  <input v-if="calltype=='csdinbounddetails' || calltype=='missedcallsdetails' || calltype=='csdoutbounddetails' || calltype=='collectiondetails'"  type="text" class="form-control" id="customerName" placeholder="Enter Customer Name"  v-model="new_customer_name">
                  <input v-else  type="text" class="form-control" id="customerName" placeholder="NOT YET REGISTER"  v-model="new_customer_name" disabled>
                </div>
                <hr>
              <div class="row justify-content-end">
                  <div v-if="calltype=='csdinbounddetails' || calltype=='missedcallsdetails' || calltype=='csdoutbounddetails' || calltype=='collectiondetails'" class="col-5 ">
                      <button type="button " class="btn btn-primary ml-auto m-1" data-bs-dismiss="modal" id="addbtn" >Submit</button>
                    <button type="button" class="btn btn-danger ml-auto "  data-bs-dismiss="modal" >Close</button>
                  </div>
              </div>
           </div>
        </form>
        </div>
       

      </div>

    </div>
  </div>

</template>

<script>
export default {
    // props:['modalId','modalTitle', 'formId', 'formMethod', 'mode','tags','currentComment','currentTag', 'callDetails'],
     props: ['customer_id', 'customer_number', 'customer_name', "updated_by", "calltype"],
  

    data: function(){
        return{
   
          new_customer_id: null,
          new_customer_name: null,

           formIsValid: true,
           
        }
      }, 
    
    methods:{

        setNewCustomerName(e){
            this.new_customer_name = e.target.value
        },
        setNewCustomerId(e){
            this.new_customer_id = e.target.value
        },
        formValidation(){
          //  this.new_customer_id = this.customer_id 
          //  this.new_customer_name = this.customer_name
           
            if((this.new_customer_id == null || this.new_customer_name == null) || (this.new_customer_id == '' || this.new_customer_name == '')) {
             alert('Blank Fields are not allowed') 
             this.formIsValid = false
            }
           
           
      
           return this.formIsValid 
        },
        submitFromData(){
           
            if(!this.formValidation()){
                this.formIsValid = true
                
                return 
            }
            
            const loggedInUserName = this.$store.getters['getLoggedinUserData'].name
      
            const data = {}
           
                data.updated_by = loggedInUserName
                data.customer_number = this.customer_number
                data.customer_id =  this.new_customer_id
                data.customer_name =  this.new_customer_name
               
                //This is use to check if the previous state is null or has a value
                //If there are a value, we just run and update the customerinfo if 
                //If the value are null , we need to inset the new customerinf
              
                data.customer_id_old_state = this.customer_id
                data.customer_name_old_state = this.customer_name
               
  
               this.$emit('emittedCustomerData', data)
        }

    },
    computed: {
          errorDiv(){
           return !this.formIsValid ? 'errorDiv' : ''
          },


    },
    created(){
     
    },
    mounted(){
      
    },
    watch: {
      customer_id() {
        this.new_customer_id = this.customer_id  
      },
      customer_name() {
        this.new_customer_name = this.customer_name
      }
    }
}
</script>

<style scoped>
  .errorDiv {
    border: 5px solid red;
    padding: 10px;
   
  }
  .errorP{
    color:red;
  }
</style>