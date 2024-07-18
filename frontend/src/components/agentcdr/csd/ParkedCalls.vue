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

    <template v-if="parkedCalls.length !== 0">
      <base-table theader="parkedcalls" tableclass='cdr' >
         <template v-slot:default>
             <parked-calls-data-list :tdata="parkedCalls"></parked-calls-data-list>
          </template>
      </base-table>
   </template>
     <div v-else>
    
      <base-container>
      <h1>No Parked Calls</h1>
      </base-container>
    </div> 
  </div>
</template>

<script>

import ParkedCallsDataList from '../data/ParkedCAllsDataList.vue'
export default {
    emits:['emittedData'],
    components: {
      ParkedCallsDataList
    },
    data(){
      return {
        error: null,
        isLoading: false,
        appName: this.$store.getters.getAppName
      }
    },  
    methods: {
      async fetchParkedCalls(){
         try {
           setInterval(()=>{
              
              this.$store.dispatch('agentcdr/fetchParkedCalls')
              this.isLoading = false
           }, 3000);
           this.isLoading = true
         }catch(e){
           this.error = e.message
           this.isLoading = false
         }
      },

      handleError(){
        this.error = null
      }
    },
    computed:{
         getAutoLogoutStatus(){
            return this.$store.getters['getAutoLogoutStatus']
        },
        parkedCalls(){
           return this.$store.getters['agentcdr/getParkedCalls']
        }
    },
    created(){
         this.$store.dispatch('checkIfCurrentLogin')
         this.fetchParkedCalls()
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