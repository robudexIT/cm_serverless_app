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
            <base-table theader="agent" tableclass='agent'>
                <agents-data-list :tdata="allAgents" @click="deleteAgent" :agent="agent" @emittedData="updateAgent"></agents-data-list>
            </base-table>
            <management-modal-form
                modalId="modalAgent"
                modalTitle="Add Agent"
                formId="addAgent"
                formMethod="POST"
                :agent="agent"
                @emittedData="addAgent"
            
            > </management-modal-form>
         
            <button type="button" class="btn btn-dark" data-bs-toggle="modal" :data-bs-target="dataBsTarget" dataset-backdrop="static" dataset-keyboard="false" id="add_tag">
                ADD AGENT
        </button>
         
       </div>
    </base-container>

</template>

<script>
import AgentsDataList from '../../components/Management/data/AgentsDataList.vue'
import ManagementModalForm from './modal/ManagementModalForm.vue'
export default {
  props: ['agent'],
  emits:['emittedData'],
  data(){
      return {
          dataBsTarget: '#modalAgent',
          isLoading: false,
          error: null,
          appName: this.$store.getters.getAppName
      }
  },
  components:{
      AgentsDataList,
      ManagementModalForm,
     
  },
  methods: {
     async fetchAllAgents(){
          try{
             this.isLoading = true
             await  this.$store.dispatch('agentinfo/fetchAllAgents',{agent:this.agent})
             this.isLoading = false
             
          }catch(e){
              this.error = e.message
          }
           
      },
      async addAgent(data){
         
          try{
           await  this.$store.dispatch('agentinfo/createAgent',{data: data, agent: this.agent})
           alert(this.agent.toUpperCase() + 'Agent was successfully added')     
          }catch(e){
              this.error = e.message
             alert(this.error + ' Please Check if the extension was already used')
          }
      },
     async updateAgent(data){
         try {
            await this.$store.dispatch('agentinfo/updateAgent',{data:data, agent:this.agent})
            alert(this.agent.toUpperCase() + 'Agent was successfully updateAgent')
         }catch(e){
             this.error = e.message
             
         }
      },
      deleteAgent(extension){

         let confirmAnswer = confirm(`Are you sure you want delete ${extension} Agent? Deleting Agent will automatically delete Agent Records as well`) 
         if(confirmAnswer) {
             try{
             this.$store.dispatch('agentinfo/deleteAgent',{extension: extension, agent: this.agent})
             alert('Selected  ' + this.agent.toUpperCase() + ' agent with ' +extension+ ' was successfully deleted')   
            }catch(e){
                this.error = e.message
            }
         }else{
             return
         }
         
      },
      handleError(){
          this.error = null
      }
  },
  computed: {
      allAgents(){
          let agents 
          if(this.agent == 'csd'){
             agents = this.$store.getters['agentinfo/getCsdAgents']
            
          }else if(this.agent == 'collection'){
              agents = this.$store.getters['agentinfo/getCollectionAgents']
          }else if(this.agent == 'sales'){
               agents = this.$store.getters['agentinfo/getSalesAgents']
          }else{
              agents = 'No Agent Found'
          }
        
          return agents
      },
       getAutoLogoutStatus(){
        return this.$store.getters['getAutoLogoutStatus']
      }
      
  },
  created(){
     this.$store.dispatch('checkIfCurrentLogin')
      this.fetchAllAgents()
      
  },
 
  watch:{
      agent(){
          this.fetchAllAgents()
      },
       getAutoLogoutStatus(currentstatus , oldstatus){
        if(currentstatus && currentstatus !== oldstatus){
           this.$router.replace('/'+this.appName+'/login')
        }
      }
  }
}
</script>