<template>
<div>
  <!-- {{callsDetails}} -->
   <base-dialog :show="!!error" @close="handleError">
     <p>{{error}}</p>
   </base-dialog>
    <base-dialog v-if="isLoading" :show="isLoading">
        <p>{{error}}</p>
        <base-spinner >
           <p>Fetching Data From the Database Please Wait....</p>
        </base-spinner>
    </base-dialog>
    
    <template v-else-if="callsDetails.length != 0" >
     
      <base-container> 
        
        <h2  v-if="activeRoutePath==='calldetails'" class="text-center font-weight-bold text-primary">{{callsDetails[0].name}}-<span class='text-danger'> CALLS DETAILS </span><button class="btn btn-secondary btn-sm" @click=" exportfetchDetails"> EXPORT </button></h2>  
      </base-container>
      
      <base-table v-if="activeRoutePath==='calldetails'" :theader="calltype" tableclass='cdr' :tags="callsDetailsTag" @emittedData="searchResult"  >
          
          <calls-details-data-list activeRoutePath="calldetails" :tdata="callsDetails" :trimStart="trimStart" :tags="callsDetailsTag" :calltype="calltype" @emittedData="putCommentTag" @emittedCustomerData="setCustomerinfo"></calls-details-data-list>
           <!-- <calls-details-data-list :tdata="callsDetails[0]" :tags="callsDetails[1]" :calltype="calltype" @emittedData="putCommentTag"></calls-details-data-list> -->
        </base-table>

        <base-table v-else-if="activeRoutePath==='searchnumberIn'" theader="searchnumberIn" tableclass='cdr' :tags="callsDetailsTag">
          
          <calls-details-data-list activeRoutePath="searchnumberIn" :tdata="callsDetails" :trimStart="trimStart" :tags="callsDetailsTag" :calltype="calltype" @emittedData="putCommentTag"   @emittedCustomerData="setCustomerinfo"></calls-details-data-list>
           <!-- <calls-details-data-list :tdata="callsDetails[0]" :tags="callsDetails[1]" :calltype="calltype" @emittedData="putCommentTag"></calls-details-data-list> -->
        </base-table>

        <base-table v-else-if="activeRoutePath==='searchnumberOut'" theader="searchnumberOut" tableclass='cdr' :tags="callsDetailsTag" @emittedData="searchResult" >
          
          <calls-details-data-list activeRoutePath="searchnumberOut" :tdata="callsDetails" :trimStart="trimStart" :tags="callsDetailsTag" :calltype="calltype" @emittedData="putCommentTag"></calls-details-data-list>
           <!-- <calls-details-data-list :tdata="callsDetails[0]" :tags="callsDetails[1]" :calltype="calltype" @emittedData="putCommentTag"></calls-details-data-list> -->
        </base-table>
        
      <the-pagination :numberOfPages="getTotalPages()" @emittedData="getCurrentPage"></the-pagination> 
    </template> 
   <div v-else>
    
      <base-container>
      <h1>No Result Found</h1>
      </base-container>
    </div> 
   
</div>
</template>

<script>
import BaseContainer from '../layout/BaseContainer.vue'
import CallsDetailsDataList from './data/CallsDetailsDataList.vue'
import ThePagination from '../layout/ThePagination.vue'

export default {
  emits:['emittedData','emittedCustomerData'],
  components: {
    CallsDetailsDataList,
    BaseContainer,
    ThePagination,
   
  },
  props:['calltype'],
  data(){
    return {
      isLoading: false,
      numberPerPage:5,
      currentItemList: null,
      currentPage: 1,
      currentTags: [],
      trimStart: 0,
      trimEnd:5,
      error: null,
      activeRoutePath:'calldetails',
      appName: this.$store.getters.getAppName
    }
  },
  
  methods:{
  async searchResult(from,to,tag,duration,direction){
            let querystring = window.location.search.substring(1)
            let extension = querystring.split('&')[0].split("=")[1]
            let name = querystring.split('&')[1].split("=")[1]
            await this.$router.push({path:this.$route.path, query:{ extension: extension, name:name,startdate:from ,enddate:to,tagname:tag,duration,direction}})
   }, 
  
   async fetchCallDetials(){
     
      let querystring = window.location.search.substring(1)
      if(this.$route.path.includes('searchnumber') && this.$route.path.includes('csdinbounddetails')){
        this.activeRoutePath = 'searchnumberIn'
      }else if(this.$route.path.includes('searchnumber')){
        this.activeRoutePath = 'searchnumberOut'
      }else{
        this.activeRoutePath = 'calldetails'
      }
     try {
       this.isLoading = true
       if(!querystring.includes('number')){
        
         await this.$store.dispatch('agentcdr/fetchCallsDetails',{querystring, calltype:this.calltype})
        
       }else{
          await this.$store.dispatch('agentcdr/fetchSearchedNumber',{querystring, calltype:this.calltype})
        
       }
      
       this.isLoading = false
     }catch(e){
     
       this.error = e.message
       this.isLoading = false
       
      
     }
    },
    exportfetchDetails(){
            let dataToBeExported
              dataToBeExported = this.$store.getters['agentcdr/getDetailsExportData']
        //    console.log(dataToBeExported)  
             window.Jhxlsx.export(dataToBeExported.tableData, dataToBeExported.options);
        
    },
    putCommentTag(data){
      let querystring = window.location.search.substring(1)
      console.log(data)
       
       this.$store.dispatch('agentcdr/putCommentTag',{querystring,data:data,calltype:this.calltype})
      //  this.buildPage(this.currentPage)
      
    },
   async setCustomerinfo(data){
        console.log("from calldetails")
       
        try {
          if (data.customer_id_old_state == data.customer_id  && data.customer_name_old_state == data.customer_name){
            return
          }
          if(data.customer_id_old_state == "" || data.customer_name_old_state == "") {
          await   this.$store.dispatch('agentcdr/insertCustomerInfo',{customer_id: data.customer_id, customer_name: data.customer_name, customer_number: data.customer_number, updated_by: data.updated_by})
          await  this.fetchCallDetials()
          }else{
           await this.$store.dispatch('agentcdr/updateCustomerInfo',{customer_id: data.customer_id, customer_name: data.customer_name, customer_number: data.customer_number, updated_by: data.updated_by})
           await this.fetchCallDetials()
          }
          
        }catch(e){
          alert(e.message)
        }
       
    },
    getTotalPages(){
       //return  Math.ceil(this.callsDetails[0].length/this.numberPerPage)
        let calldetails 
      
       if(this.calltype == 'csdinbounddetails'){
          calldetails =  this.$store.getters['agentcdr/getCsdInBoundAgentDetails']
      }else if(this.calltype == 'csdoutbounddetails'){
          calldetails = this.$store.getters['agentcdr/getCsdOutBoundAgentDetails']
      }else if(this.calltype == 'collectiondetails'){
           calldetails =  this.$store.getters['agentcdr/getCollectionOutBoundAgentDetails']
      }else if(this.calltype == 'salesdetails'){
          calldetails = this.$store.getters['agentcdr/getSalesOutBoundAgentDetails']
      }else {
          calldetails = 'no data'
      }
       return  Math.ceil(calldetails[0].length/this.numberPerPage)
    },
    getCurrentPage(currentPage){ 
         currentPage = parseInt(currentPage)
         this.currentPage = currentPage 
         this.trimStart = (this.currentPage-1)* this.numberPerPage
         this.trimEnd = this.trimStart + this.numberPerPage
       
    },
    handleError(){
      this.error = null
    }
  },
  computed: {
    callsDetails(){
       let calldetails
      //  let trimStart = (this.currentPage-1)* this.numberPerPage
      //  let  trimEnd = trimStart + this.numberPerPage
       
      if(this.calltype == 'csdinbounddetails'){
          calldetails =  this.$store.getters['agentcdr/getCsdInBoundAgentDetails']
      }else if(this.calltype == 'csdoutbounddetails'){
          calldetails = this.$store.getters['agentcdr/getCsdOutBoundAgentDetails']
      }else if(this.calltype == 'collectiondetails'){
           calldetails =  this.$store.getters['agentcdr/getCollectionOutBoundAgentDetails']
      }else if(this.calltype == 'salesdetails'){
          calldetails = this.$store.getters['agentcdr/getSalesOutBoundAgentDetails']
      }else {
          calldetails = 'no data'
      }

      return calldetails.length == 0 ? [] : calldetails[0].slice(this.trimStart, this.trimEnd)
    },
    callsDetailsTag(){
       let calldetailsTag
       
      if(this.calltype == 'csdinbounddetails'){
          calldetailsTag =  this.$store.getters['agentcdr/getCsdInBoundAgentDetails'][1]
      }else if(this.calltype == 'csdoutbounddetails'){
          calldetailsTag = this.$store.getters['agentcdr/getCsdOutBoundAgentDetails'][1]
      }else if(this.calltype == 'collectiondetails'){
           calldetailsTag =  this.$store.getters['agentcdr/getCollectionOutBoundAgentDetails'][1]
      }else if(this.calltype == 'salesdetails'){
          calldetailsTag = this.$store.getters['agentcdr/getSalesOutBoundAgentDetails'][1]
      }else {
          calldetailsTag = 'no data'
      }

      return calldetailsTag
    },
    getAutoLogoutStatus(){
      return this.$store.getters['getAutoLogoutStatus']
    }
  },
  
  created(){
    this.$store.dispatch('checkIfCurrentLogin')
    this.fetchCallDetials()
     
   
  },
  watch:{
      calltype(){
          this.fetchCallDetials()
      },
      $route(){
        this.fetchCallDetials()
      },
       getAutoLogoutStatus(currentstatus , oldstatus){
            if(currentstatus && currentstatus !== oldstatus){
             this.$router.replace('/'+this.appName+'/login')
        }
      }
  }
    
}
  

</script>