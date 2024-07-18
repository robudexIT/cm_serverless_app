<template>
    <!-- <div>{{details}}</div> -->
    <div class="modal fade"  id="modalCustomerInfo" role="dialog">
    <div class="modal-dialog">

      <!-- Modal content-->
      <div class="modal-content">
        <div class="modal-header">

          <h4 class="modal-title">Customer Details</h4>
        </div>
        <div class="modal-body">
          <form method="POST"  id="customer_form_id" @submit.prevent="submitFromData">
               
                <div class="form-group">
                  <label for="customerNumber">Customer Number:</label>
                  <input type="text" class="form-control" id="customerNumber" placeholder="Enter Customer Number" v-model="customer_number">
                </div>
                <!-- <div class="form-group">
                  <label for="customerID">Customer ID:</label>
                  <input type="text" class="form-control" id="customerID" placeholder="Enter Customer ID" v-model="new_customer_id" > 
                </div>
                <div class="form-group">
                  <label for="customerName">Customer Name:</label>
                 
                  <input  type="text" class="form-control" id="customerName" placeholder="Enter Customer Name"  v-model="new_customer_name" >
                </div> -->
                <hr>
              <div class="row justify-content-end">
                 
                 <div  class="col-5 ">
                    <button type="button " class="btn btn-primary ml-auto m-1" data-bs-dismiss="modal" id="addbtn" >Search</button>
                    <button type="button" class="btn btn-danger ml-auto "  data-bs-dismiss="modal" >Close</button>
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
    // props:['modalId','modalTitle', 'formId', 'formMethod', 'mode','tags','currentComment','currentTag', 'callDetails']
  

    data: function(){
        return{
           customer_number: null,
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
           
            if((this.customer_number == null )) {
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
               const data = {}
               data.customer_number = this.customer_number
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