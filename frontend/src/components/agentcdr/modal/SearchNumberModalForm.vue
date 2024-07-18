<template>
     <div class="modal fade" id="searchnumber" role="dialog">
    <div class="modal-dialog">

      <!-- Modal content-->
      <div class="modal-content">
        <div class="modal-header">

          <h4 class="modal-title">Search Number</h4>
        </div>
        <div class="modal-body">
              <form  @submit.prevent="submitFromData">
                    <div >
                        <!-- <p class="errorP"  >Please Make Sure That Dont Leave Blank on the Input Fields</p> -->
                      <div class="mb-3">
                        <label for="searchnumber"  class="mb-3">Search Number</label>
                        <input type="text" id="searchnumber" class="form-control" aria-describedby="tag" v-model="inputNumber">
                      
                      </div>

                    </div> 
                  <hr>
                  <div class="row justify-content-end">
                    <div class="col-5 ">
                        <button type="button " class="btn btn-primary ml-auto m-1" data-bs-dismiss="modal"  >Submit</button>
                        <button type="button" class="btn btn-danger ml-auto "  data-bs-dismiss="modal">Close</button>
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
   props:['calltype'],
    data(){
        return {
            inputNumber: null,
             formIsValid: true,

        }
    },
    methods: {
       
       formValidation(){
        
         this.formIsValid = true
         if(this.inputNumber == '' || this.inputNumber == null){
           this.formIsValid = false
           return
         }
         return this.formIsValid
       },
       submitFromData(){
         if(!this.formValidation()){
           return
         }
         const calltype = this.calltype +'details'
        //  this.$router.replace({path: '/sbtph_app/searchnumber/'+calltype, query: {number:this.inputNumber}})
         this.$emit('emittedDataSearchNumber', {customer_number:this.inputNumber,searchpath:'/sbtph_app/searchnumber/'+calltype})
       }
    },

    

}
</script>