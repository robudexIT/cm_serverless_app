<template>

  <div>
     <base-dialog :show="!!error" @close="handleError">
     <p>{{error}}</p>
   </base-dialog>
    <base-dialog v-if="isLoading" :show="isLoading">
        <p>{{error}}</p>
        <base-spinner >
           <p>Fetching Data From the Database Please Wait....</p>
        </base-spinner>
    </base-dialog>

    <template v-if="voiceMails.length !== 0">
      <base-table theader="voicemails" tableclass='cdr' >
         <template v-slot:default>
             <voice-mails-data-list :tdata="voiceMails" @emittedData="deleteVoiceMail"></voice-mails-data-list>
          </template>
      </base-table>
   </template>
     <div v-else>
    
      <base-container>
      <h1>No Result Found</h1>
      </base-container>
    </div> 
  </div>
</template>

<script>

import VoiceMailsDataList from '../data/VoiceMailsDataList.vue'
export default {
    emits:['emittedData'],
    components: {
      VoiceMailsDataList
    },
    data(){
      return {
        error: null,
        isLoading: false,
        appName: this.$store.getters.getAppName
        
      }
    },  
    methods: {
      async fetchVoiceMails(){
         try {
           this.isLoading = true
           await this.$store.dispatch('agentcdr/fetchVoiceMails')
           this.isLoading = false
         }catch(e){
           this.error = e.message
           this.isLoading = false
         }
      },
      deleteVoiceMail(timestamp){
        this.$store.dispatch('agentcdr/deleteVoiceMails',{timestamp})
      },
      handleError(){
        this.error = null
      }
    },
    computed:{
         getAutoLogoutStatus(){
            return this.$store.getters['getAutoLogoutStatus']
        },
        voiceMails(){
           return this.$store.getters['agentcdr/getVoiceMails']
        }
    },
    created(){
         this.$store.dispatch('checkIfCurrentLogin')
         this.fetchVoiceMails()
    },
    watch:{
        getAutoLogoutStatus(currentstatus , oldstatus){
          if(currentstatus && currentstatus !== oldstatus){
            this.$router.replace('/'+this.appName+'/login')
          }
        }       
    }
}
</script>