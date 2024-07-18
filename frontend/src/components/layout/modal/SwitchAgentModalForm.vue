<template>
   <base-dialog :show="!!error" @close="handleError">
     <p>{{error}}</p>
   </base-dialog>
    <base-dialog v-if="isLoading" :show="isLoading">
        <base-spinner >
           <p>Updating Agent CallType Settings Please Wait....</p>
        </base-spinner>
    </base-dialog>
    <div class="modal fade" id="switchAgent" role="dialog">
    <div class="modal-dialog">

      <!-- Modal content-->
      <div class="modal-content">
        <div class="modal-header">

          <h4 class="modal-title">SwitchAgent CallType:</h4>
        </div>
        <div class="modal-body">
                 <form @submit.prevent="submitFormata">
                     <div class="mb-3">
                      <label for="TagType">Select Calltype:</label>
                       <select class="form-select" required :value="belongsTo" @change="setNewBelongsTo">
                             <option  value="csd">CSD</option>
                             <option  value="collection">COLLECTION</option>
                      </select>
                    
                    </div>
                    <hr>
                    <div class="text-right mb-3">
                          <button type="submit " class="btn btn-primary ml-auto m-1" data-bs-dismiss="modal" id="updateCalltype" >Update</button>
                         <button type="button" class="btn btn-danger ml-auto "  data-bs-dismiss="modal" >Close</button>
                    </div>

                </form> 
                
        </div>


      </div>

    </div>
  </div>
</template>

<script>
export default {
 props: ['belongsTo'],

 data(){
   return {
     newBelongsTo: null,
     isLoading: false,
     error: null,
     appName: this.$store.getters.getAppName
   }
 },
 methods: {
    setNewBelongsTo(e){
            this.newBelongsTo = e.target.value
            
        },
    submitFormata(){
      if(this.newBelongsTo === null || this.newBelongsTo == this.belongsTo){
        alert('You already belongs to ' + this.belongsTo)
        return
      }try{
         this.$store.dispatch('agentinfo/udpateAgentBelongsTo',{calltype: this.newBelongsTo})
          setTimeout(()=>{
            this.isLoading = false
            alert('Changing Agent CallType are Completed.The APPS will automatically logout for the change to take effect..')
            this.$store.dispatch('logoutUser')
            this.$router.replace(`/${this.appName}/login`)
          },10000)

          this.isLoading = true
      }catch(e){
        this.error = e.message
      }
      
    },
    handleError(){
      this.error = null
    }
   
 }
}
</script>