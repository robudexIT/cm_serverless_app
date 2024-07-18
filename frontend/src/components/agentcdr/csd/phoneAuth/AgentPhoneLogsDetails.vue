<template>
    <base-dialog :show="!!error" @close="handleError">
     <p>{{error}}</p>
   </base-dialog>
    <base-container v-if="isLoading"> 
        <base-dialog :show="isLoading">
            <base-spinner>
                 <p>Fetching Data From the Database Please Wait....</p>
            </base-spinner>    
        </base-dialog>
    </base-container>
     <base-container v-else>
        <base-table theader="phoneloginheaderdetails" tableclass='cdr'>
            <agent-phone-logs-details-data-list :trimStart="trimStart" :tdata="agentPhoneLogsDetails"></agent-phone-logs-details-data-list>
        </base-table>
        <the-pagination :numberOfPages="getTotalPages()" @emittedData="getCurrentPage"></the-pagination> 
     </base-container>
    
</template>


<script>
import AgentPhoneLogsDetailsDataList from '../../data/AgentPhoneLogsDetailsDataList.vue'
import ThePagination from '../../../layout/ThePagination.vue'
export default {
    
    components: {
        AgentPhoneLogsDetailsDataList,
        ThePagination,
    },
    data(){
        return {
            isLoading: false,
            error: null,
            numberPerPage:10,
            currentItemList: null,
            currentPage: 1,
            currentTags: [],
            trimStart: 0,
            trimEnd:10,

        }
    },
    methods: {
        async fetchAgentPhoneLogsDetails(){
            let querystring = window.location.search.substring(1)
            this.isLoading = true
            try{
              await  this.$store.dispatch('csdphone/agentPhoneLogsDetails',{querystring})
              this.isLoading = false
            }catch(e){
                this.error = e.message
            }
        },
         getCurrentPage(currentPage){ 
            currentPage = parseInt(currentPage)
            this.currentPage = currentPage 
            this.trimStart = (this.currentPage-1)* this.numberPerPage
            this.trimEnd = this.trimStart + this.numberPerPage
        
         },
         getTotalPages(){
             let agentPhoneLogs = this.$store.getters['csdphone/getAgentPhoneLogsDetails']
             return  Math.ceil(agentPhoneLogs.length/this.numberPerPage)
         },
        handleError(){
            this.error = null
        }
    },
    computed: {
        agentPhoneLogsDetails(){
            let agentPhoneLogs = this.$store.getters['csdphone/getAgentPhoneLogsDetails']
           return agentPhoneLogs.length == 0 ? [] : agentPhoneLogs.slice(this.trimStart, this.trimEnd)
           //return agentPhoneLogs
        },
        getAutoLogoutStatus(){
            return this.$store.getters['getAutoLogoutStatus']
        }
    },
    created(){
        this.$store.dispatch('checkIfCurrentLogin')
        this.fetchAgentPhoneLogsDetails()
    },
    watch: {
      getAutoLogoutStatus(currentstatus , oldstatus){
        if(currentstatus && currentstatus !== oldstatus){
            this.$router.replace('/login')
        }
      }
    }
}
</script>

