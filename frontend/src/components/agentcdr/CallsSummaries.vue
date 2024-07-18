<template>

  <base-dialog :show="!!error" @close="handleError">
     <p>{{error}}</p>
   </base-dialog>
   <base-container>
   
     <button class="btn btn-primary h-25 p-1 w-100 export_btn " @click="exportfetchSummries">
         Export 
    </button>
   
    <base-table  :calltype="calltype" :theader="calltype" tableclass='cdr' :tags="callSummaries[1]" @emittedData="searchResult" @emittedDataSearchNumber="searchResultNumber">
        <base-dialog v-if="isLoading" :show="isLoading">
           <base-spinner>
             <p>Fetching Data From the Database Please Wait....</p>
           </base-spinner>
        </base-dialog>
        <call-summary-data-list v-else :tdata="callSummaries[0]" :tags="callSummaries[1]" ></call-summary-data-list>
    </base-table>
   </base-container>

</template>


<script>
import CallSummaryDataList from './data/CallSummaryDataList.vue'
export default {
    components: {
       CallSummaryDataList
    },
    props: ['calltype'],
    data(){
        return {
            error: null,
            ctype: null,
            querystring: null,
            isLoading: false,
            appName: this.$store.getters.getAppName
        }
    },
    methods:{
        async searchResult(from,to,tag,duration,direction){
            await this.$router.push({path:this.$route.path, query:{startdate:from ,enddate:to,tagname:tag,duration,direction}})
                      
        },
        searchResultNumber(data){
           
            this.$router.replace({path: data.searchpath, query: {customer_number:data.customer_number}})
        },
        async fetchSummaries(){
            this.querystring = window.location.search.substring(1)
            this.ctype = this.calltype
            try{
               this.isLoading = true
               await this.$store.dispatch('agentcdr/fetchCallsSummaries',{querystring:this.querystring,calltype:this.calltype})
               this.isLoading = false
              
              
            }catch(e){
                this.error = e.message || 'Error fetch call summary'
            }

        },
          exportfetchSummries(){
            let dataToBeExported
              dataToBeExported = this.$store.getters['agentcdr/getSummariesExportData']
        //    console.log(dataToBeExported)  
            //  window.Jhxlsx.export(dataToBeExported.tableData, dataToBeExported.options);

       if (window.Jhxlsx && window.Jhxlsx.export) {
        console.log('Its loaded!!')
        window.Jhxlsx.export(dataToBeExported.tableData, dataToBeExported.options);
        } else {
        console.error('Jhxlsx or its export method is not defined.');
        }
        
        },
        handleError(){
            this.error = null
        }
    },
    computed:{
        callSummaries(){
           let callsummary 
           if(this.calltype == 'csdinbound'){
                callsummary = this.$store.getters['agentcdr/getCsdInBoundSummaries']
                 
           }else if(this.calltype == 'csdoutbound'){
               callsummary =  this.$store.getters['agentcdr/getCsdOutBoundSummaries']
           }else if(this.calltype == "collection"){
               callsummary =  this.$store.getters['agentcdr/getCollectionOutBoundSummaries']
           }else if(this.calltype == "sales"){
               callsummary =  this.$store.getters['agentcdr/getSalesOutBoundSummaries']
           }
           
           return callsummary
          
        },
       getAutoLogoutStatus(){
           return this.$store.getters['getAutoLogoutStatus']
       }
    },
    created(){
        this.$store.dispatch('checkIfCurrentLogin')
        this.fetchSummaries()
        
    },
    watch:{
        calltype(){
            this.callSummaries = []
            this.fetchSummaries()
        },
       $route(){
          this.callSummaries = []
           this.fetchSummaries()
       },
       getAutoLogoutStatus(currentstatus , oldstatus){
         if(currentstatus && currentstatus !== oldstatus){
           this.$router.replace('/'+this.appName+'/login')
        }
      }
    }
}
</script>

<style scoped>
    .export_btn {
        border-radius: 5px;
    }
</style>