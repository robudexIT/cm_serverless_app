<template>
  <base-dialog :show="!!error" @close="handleError">
     <p>{{error}}</p>
   </base-dialog>
   <template v-if="isLoading">
       <base-dialog :show="isLoading">
            <base-spinner>
             <p>Fetching Data From the Database Please Wait....</p>
            </base-spinner>
       </base-dialog>
   </template>
   <template v-else>
    <base-container>
            <h2 class="text-center font-weight-bold text-primary"><span class='text-danger'> MISSED-CALLS DETAILS </span><button class="btn btn-secondary btn-sm" @click="exportMissedCallsDetails"> EXPORT </button></h2>
    </base-container>
        <base-table theader="detailedmissedcalls"  tableclass='cdr' @emittedData="searchResult">
            <missed-calls-details-data-list v-if="missedCallsDetais.length !==0" :tdata="missedCallsDetais" @emittedData="putCommentTag" @emittedCustomerData="setCustomerinfo"></missed-calls-details-data-list>
            <p v-else>Result Not Found</p>
        </base-table> 
         <the-pagination v-if="missedCallsDetais.length !==0" :numberOfPages="getTotalPages()" @emittedData="getCurrentPage"></the-pagination> 
    </template>
  
</template>


<script>
 import MissedCallsDetailsDataList from '../data/MissedCallsDetailsDataList.vue'
 import ThePagination from '../../layout/ThePagination.vue'

export default {
    emits:['emittedData'],
    components:{
        MissedCallsDetailsDataList,
        ThePagination
    },
    data(){
        return {
            error: null,
            isLoading : false,
            numberPerPage:5,
            currentItemList: null,
            currentPage: 1,
            currentTags: [],
            trimStart: 0,
            trimEnd:5,
            appName: this.$store.getters.getAppName
        }
    },
    methods:{
         searchResult(from,to,tag){
            this.$router.push({path:this.$route.path, query:{startdate:from ,enddate:to,tagname:tag}})
        },
       async fetcthMissedCallsDetails(){
            try{
            
               let option = '&option=details'
               let querystring = window.location.search.substring(1) + option
               this.isLoading = true
               await this.$store.dispatch('agentcdr/fetchMissedCallsDetails',{querystring})
               this.isLoading = false
            }catch(e){
                this.error = e.message
                this.isLoading = false
            }
            
        },
        putCommentTag(data){
          try {
           this.$store.dispatch('agentcdr/putCommentTag',{data:data,calltype:'missedcalls'})
          }catch(e){
              this.error = e.message
          }
        },
        getTotalPages(){
            let  missedCallsDetais =  this.$store.getters['agentcdr/getMissedCallsDetails']

            return  Math.ceil(missedCallsDetais.length/this.numberPerPage)
        },
        getCurrentPage(currentPage){ 
         currentPage = parseInt(currentPage)
         this.currentPage = currentPage 
         this.trimStart = (this.currentPage-1)* this.numberPerPage
         this.trimEnd = this.trimStart + this.numberPerPage
       
        },
         exportMissedCallsDetails(){
            let dataToBeExported
              dataToBeExported = this.$store.getters['agentcdr/getMissedCallsDetailsExport']
        //    console.log(dataToBeExported)  
             window.Jhxlsx.export(dataToBeExported.tableData, dataToBeExported.options);
         },
        setCustomerinfo(data){   
            console.log("from calldetails")
            console.log(data)
            try {
            if(data.customer_id_old_state == "" || data.customer_name_old_state == "") {
                this.$store.dispatch('agentcdr/insertCustomerInfo',{data})
                 this.fetcthMissedCallsDetails()
            }else{
                this.$store.dispatch('agentcdr/updateCustomerInfo',{data})
                 this.fetcthMissedCallsDetails()
            }
            
            }catch(e){
            alert(e.message)
            }
       
        },
         handleError(){
             this.error = null
         }     
    },
    computed:{
        missedCallsDetais(){
            // return  this.$store.getters['agentcdr/getMissedCallsDetails']
            let missedCallsDetais =  this.$store.getters['agentcdr/getMissedCallsDetails']
           
            return missedCallsDetais.length == 0 ? [] : missedCallsDetais.slice(this.trimStart, this.trimEnd)
        },
         getAutoLogoutStatus(){
            return this.$store.getters['getAutoLogoutStatus']
        }

    },
    created(){
        this.$store.dispatch('checkIfCurrentLogin')
       
         this.fetcthMissedCallsDetails()
    },
    watch:{
        $route(){
            this.fetcthMissedCallsDetails()
        },
        getAutoLogoutStatus(currentstatus , oldstatus){
         if(currentstatus && currentstatus !== oldstatus){
           this.$router.replace('/'+this.appName+'/login')
        }
      }
    }

}
</script>