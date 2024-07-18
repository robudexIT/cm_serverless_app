<template>

    <div>
      <base-dialog :show="!!error" @close="handleError">
             <p>{{error}}</p>
     </base-dialog>  
     <base-container>
        <base-table theader="missedcalls"  tableclass='cdr'  @emittedData="searchResult" >
            <template v-slot:default  v-if="missedCallsSummaries.length !== 0">
                <missed-calls-summaries-data-list :tdata="missedCallsSummaries"  ></missed-calls-summaries-data-list>
            </template>
            <template v-slot:default  v-else>
                <p>Rusult Not Found!</p>
            </template>
        </base-table>
   </base-container>
  
  </div>
</template>


<script>
import MissedCallsSummariesDataList from '../data/MissedCallsSummariesDataList.vue'
 export default {
     emits: ['searchResult'],
     data(){
         return {
             error: null,
            appName: this.$store.getters.getAppName
         }
     },
     components:{
         MissedCallsSummariesDataList,
     },
     methods:{
          searchResult(from,to,tag){
            this.$router.push({path:this.$route.path, query:{startdate:from ,enddate:to,tagname:tag}})
            
        },
        async fetchMissedCallsSummaries(){
              let querystring = window.location.search.substring(1)
              
              if(querystring !== ''){
                  querystring = querystring + '&option=summary'
              }
            //   }else{
            //       querystring = 'startdate=2021-08-01&enddate=2021-08-23&tagname=all&option=summary'
            //   }
            //   console.log(querystring)
             try{
                await this.$store.dispatch('agentcdr/fetchMissedCallsSummaries', {querystring})//short hand for querystring:querystring
             }catch(e){
                 this.error = e.message
             }
         },
         handleError(){
             this.error = null 
         }
     },
     computed:{
         missedCallsSummaries(){
             return this.$store.getters['agentcdr/getMissedCallsSummaries']
         },
          getAutoLogoutStatus(){
            return this.$store.getters['getAutoLogoutStatus']
        }
     },
     created(){
         this.$store.dispatch('checkIfCurrentLogin')
         this.fetchMissedCallsSummaries()
     },
     watch:{
         $route(){
             this.fetchMissedCallsSummaries()
         },
         getAutoLogoutStatus(currentstatus , oldstatus){
          if(currentstatus && currentstatus !== oldstatus){
             this.$router.replace('/'+this.appName+'/login')
          }
        }
     }
 }
</script>